import os

import requests


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")
OLLAMA_FORMAT = os.getenv("OLLAMA_FORMAT", "chat").lower()

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


def get_default_api_settings():
    """Return environment-based defaults for the current Streamlit session."""
    return {
        "api_mode": API_MODE,
        "ollama_base_url": OLLAMA_BASE_URL,
        "ollama_model": OLLAMA_MODEL,
        "ollama_format": OLLAMA_FORMAT,
        "openai_base_url": OPENAI_BASE_URL,
        "openai_model": OPENAI_MODEL,
        "openai_api_key": OPENAI_API_KEY,
    }


def resolve_api_settings(api_settings=None):
    """Merge current-session settings over environment defaults."""
    settings = get_default_api_settings()

    if api_settings:
        for key, value in api_settings.items():
            if value is not None:
                settings[key] = value

    settings["api_mode"] = settings["api_mode"].lower()
    settings["ollama_format"] = settings["ollama_format"].lower()
    return settings


def build_agent_messages(prompt, role):
    """Build system/user messages for chat-style LLM APIs."""
    system_message = f"You are a {role} in a structured debate workflow. Act accordingly."

    return [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]


def flatten_messages_for_prompt(messages):
    """Convert chat messages into one prompt for Ollama's /api/generate format."""
    prompt_parts = []

    for message in messages:
        role = message.get("role", "user").title()
        content = message.get("content", "")
        prompt_parts.append(f"{role}: {content}")

    prompt_parts.append("Assistant:")
    return "\n\n".join(prompt_parts)


def get_ollama_response(prompt, role, temperature=0.7, api_settings=None):
    """
    Send a role-based prompt and return the assistant response.

    Ollama remains the default backend. Runtime API settings can be passed from
    Streamlit session state without writing tokens or model settings to disk.
    """
    settings = resolve_api_settings(api_settings)
    messages = build_agent_messages(prompt, role)

    if settings["api_mode"] in {"openai", "openai-compatible", "compatible"}:
        return get_openai_compatible_response(messages, temperature, settings)

    return get_ollama_response_by_format(messages, temperature, settings)


def get_ollama_response_by_format(messages, temperature=0.7, api_settings=None):
    """Route Ollama requests to the selected native Ollama format."""
    settings = resolve_api_settings(api_settings)

    if settings["ollama_format"] == "generate":
        return get_ollama_generate_response(messages, temperature, settings)

    return get_ollama_chat_response(messages, temperature, settings)


def get_ollama_chat_response(messages, temperature=0.7, api_settings=None):
    """Call Ollama's native /api/chat endpoint."""
    settings = resolve_api_settings(api_settings)
    base_url = settings["ollama_base_url"].rstrip("/")
    model = settings["ollama_model"]
    url = f"{base_url}/api/chat"
    payload = {
        "model": model,
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
            f"Please make sure Ollama is running at {base_url}."
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


def get_ollama_generate_response(messages, temperature=0.7, api_settings=None):
    """Call Ollama's native /api/generate endpoint."""
    settings = resolve_api_settings(api_settings)
    base_url = settings["ollama_base_url"].rstrip("/")
    model = settings["ollama_model"]
    url = f"{base_url}/api/generate"
    payload = {
        "model": model,
        "prompt": flatten_messages_for_prompt(messages),
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
            f"Please make sure Ollama is running at {base_url}."
        )
    except requests.exceptions.Timeout:
        return "Error: Ollama request timed out. The local model may still be loading."
    except requests.exceptions.RequestException as exc:
        return f"Error: Ollama API request failed: {exc}"
    except ValueError:
        return "Error: Ollama returned a response that was not valid JSON."

    try:
        return data["response"].strip()
    except (KeyError, TypeError):
        return f"Error: Unexpected Ollama response format: {data}"


def get_openai_compatible_response(messages, temperature=0.7, api_settings=None):
    """Call an OpenAI-compatible /chat/completions endpoint."""
    settings = resolve_api_settings(api_settings)
    base_url = settings["openai_base_url"].rstrip("/")
    model = settings["openai_model"]
    api_key = settings["openai_api_key"]
    url = f"{base_url}/chat/completions"
    headers = {"Content-Type": "application/json"}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
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
            f"Please check OPENAI_BASE_URL={base_url}."
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
