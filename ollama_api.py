import os

import requests


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")

# Keep Ollama as the default API mode, but allow an OpenAI-compatible API.
# Example for an OpenAI-compatible server:
#   DEBATE_API_MODE=openai
#   OPENAI_BASE_URL=http://localhost:1234/v1
#   OPENAI_API_KEY=your-key-if-needed
#   OPENAI_MODEL=deepseek-r1:7b
API_MODE = os.getenv("DEBATE_API_MODE", "ollama").lower()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", OLLAMA_MODEL)


# Previous versions of this helper are preserved in previous/ollama_api_previous.py.
# This file keeps the same public function name used by the Streamlit app:
# get_ollama_response(prompt, role, temperature=0.7)


def build_agent_messages(prompt, role):
    """Build system/user messages for chat-style LLM APIs."""
    system_message = f"You are a {role} in a structured debate workflow. Act accordingly."

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]


def get_ollama_response(prompt, role, temperature=0.7):
    """
    Send a role-based prompt and return the assistant response.

    Ollama remains the default backend. If DEBATE_API_MODE=openai is set, the
    same messages are sent to an OpenAI-compatible /chat/completions endpoint.
    """
    messages = build_agent_messages(prompt, role)

    if API_MODE in {"openai", "openai-compatible", "compatible"}:
        return get_openai_compatible_response(messages, temperature)

    return get_ollama_chat_response(messages, temperature)


def get_ollama_chat_response(messages, temperature=0.7):
    """Call Ollama's native /api/chat endpoint."""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        return (
            "Error: Could not connect to Ollama. "
            f"Please make sure Ollama is running at {OLLAMA_BASE_URL}."
        )
    except requests.exceptions.Timeout:
        return "Error: Ollama request timed out. The local model may still be loading."
    except requests.exceptions.RequestException as exc:
        return f"Error: Ollama API request failed: {exc}"
    except ValueError:
        return "Error: Ollama returned a response that was not valid JSON."

    try:
        return data["message"]["content"].strip()
    except (KeyError, TypeError):
        return f"Error: Unexpected Ollama response format: {data}"


def get_openai_compatible_response(messages, temperature=0.7):
    """Call an OpenAI-compatible /chat/completions endpoint."""
    url = f"{OPENAI_BASE_URL.rstrip('/')}/chat/completions"
    headers = {"Content-Type": "application/json"}

    if OPENAI_API_KEY:
        headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"

    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": False,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        return (
            "Error: Could not connect to the OpenAI-compatible API. "
            f"Please check OPENAI_BASE_URL={OPENAI_BASE_URL}."
        )
    except requests.exceptions.Timeout:
        return "Error: OpenAI-compatible API request timed out."
    except requests.exceptions.RequestException as exc:
        return f"Error: OpenAI-compatible API request failed: {exc}"
    except ValueError:
        return "Error: OpenAI-compatible API returned a response that was not valid JSON."

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        return f"Error: Unexpected OpenAI-compatible response format: {data}"
