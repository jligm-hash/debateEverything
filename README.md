# debateEverything

Use agent framework to debate everything.

<p align="center">
    <img src="src/pixlr-image-generator-ea0aad69-efbf-48ca-b796-61e5a633d34a.png"
    title="Agent debate"
    width="400" >
</p>


# Project idea

This project explores a simple multi-agent debate workflow. A user gives a topic or task, then several agents respond in sequence:

1. Agent 1 gives an initial analysis or draft answer.
2. Agent 2 critiques Agent 1's response.
3. Agent 1 responds to the critique and improves the answer.
4. Agent 2 gives further feedback.
5. Agent 3 summarizes the whole discussion.

The goal is to use debate-style prompting to improve reasoning, critique, and final answers.


# To-do notes

- `debate_250416.py` now uses `ollama_api.py` for the local Ollama `/api/chat` request format.
- `ollama_api.py` keeps Ollama as the default API and can also call an OpenAI-compatible `/chat/completions` API.
- Keep `debate_dspy_250416.py` as the currently smooth-running DSPy reference version.
- Previous code snapshots are stored in `previous/` before the rewrite.
- Next: optimize the UI, either by creating a new version file or by using a more popular chat-style interface.


# Archive

Previous versions of the main Python files are stored in `previous/`.
These files are preserved before rewriting so old code is not deleted.


# Version control

- `debate_dspy_250416.py` is for debating claims with DSPy.
- `debate_code_250417.py` is for debating code generation tasks.
- `debate_250416.py` is the rewritten Ollama/OpenAI-compatible API version.
- `ollama_api.py` contains the API helper used by `debate_250416.py`.


# Files

- `debate_250416.py` — Streamlit UI for the rewritten debate workflow.
- `ollama_api.py` — API helper. Uses Ollama by default and can use an OpenAI-compatible API.
- `debate_dspy_250416.py` — DSPy + Ollama version. This has been the smooth-running reference version.
- `debate_code_250417.py` — code-generation debate workflow.
- `previous/` — archived snapshots of earlier Python files.
- `src/` — image assets used by the README.


# Python environment

The project was checked with the Python environment recorded in the Claude/session environment:

`D:\Users\niwakoki\miniconda3\envs\myenv\python.exe`

Relevant packages found in that environment:

- `streamlit`
- `requests`

The rewritten Ollama version uses `requests`, so it does not require LangChain.
The DSPy reference version requires `dspy` to be installed in the Python environment before running it.


# How to run

## 1. Run the rewritten Ollama API debate version

This is the main rewritten version:

```bash
streamlit run debate_250416.py
```

Or run it with the recorded Python environment:

```bash
"D:\Users\niwakoki\miniconda3\envs\myenv\python.exe" -m streamlit run debate_250416.py
```

By default, this version opens with a clean sidebar. Detailed API settings are folded by default, and the default backend is local Ollama at:

```text
http://localhost:11434/api/chat
```

Default model:

```text
deepseek-r1:7b
```

You can change the API link, model name, Ollama format, API key/token, and temperature in the sidebar for the current session only. The sidebar also includes a `Test API` panel so you can send a short connection test before running a debate.

You can also override the startup defaults with environment variables:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:7b
```

Before running, make sure Ollama is open and the model exists locally.
For example:

```bash
ollama list
ollama pull deepseek-r1:7b
```


## 2. Use an OpenAI-compatible API instead

`ollama_api.py` can also call an OpenAI-compatible `/chat/completions` API.
Use this mode when connecting to a compatible local server or third-party endpoint.

The easiest way is to choose `openai-compatible` in the API settings panel after the app opens. Fill in the API link, model name, and optional API key/token there.

You can also set these environment variables before running the app if you want startup defaults:

```bash
DEBATE_API_MODE=openai
OPENAI_BASE_URL=http://localhost:1234/v1
OPENAI_MODEL=deepseek-r1:7b
OPENAI_API_KEY=your-key-if-needed
```

Then run:

```bash
streamlit run debate_250416.py
```

Notes:

- `OPENAI_API_KEY` can be empty if the local compatible server does not require a key.
- `OPENAI_BASE_URL` should point to the API root that contains `/chat/completions`.


## 3. Run the stable DSPy debate version

```bash
streamlit run debate_dspy_250416.py
```

This version uses DSPy and Ollama. Install DSPy first if your environment does not have it.


## 4. Run the code debate version

```bash
streamlit run debate_code_250417.py
```

This version asks agents to generate, critique, revise, and summarize code.


# Saving debate results

After a debate finishes, the sidebar export panel provides download buttons for:

- Markdown (`debate_session.md`)
- HTML (`debate_session.html`)

The export includes the prompt, visible API mode/model information, temperature, and agent outputs. It does not include the API key/token.


# Current API behavior

`debate_250416.py` shows API controls in the sidebar. Detailed API settings are collapsed by default. The user can choose:

- API mode: Ollama or OpenAI-compatible
- API link / base URL
- model name
- Ollama format: `chat` for `/api/chat` or `generate` for `/api/generate`
- API key / token for OpenAI-compatible APIs
- temperature

These UI settings are current-session only. They are stored in Streamlit session state, not written to files, and not committed to git. The API key/token field is a password field. A separate sidebar panel can test the selected API before starting a debate.

`debate_250416.py` calls:

```python
get_ollama_response(prompt, role, temperature=0.7, api_settings=api_settings)
```

from `ollama_api.py`.

`ollama_api.py` then chooses the backend:

- default: Ollama native `/api/chat`
- optional: Ollama native `/api/generate`
- optional: OpenAI-compatible `/chat/completions`

Environment variables remain useful as startup defaults, but users can override them from the UI for the current session.

The active app keeps the debate workflow separate from API details.


# UI optimization plan

The current UI now uses a cleaner Streamlit sidebar layout:

- API settings are folded/collapsed by default.
- A separate `Test API connection` panel can check the selected backend before debate.
- The main page focuses on the user prompt and debate results.
- Results are stored in `st.session_state` during the browser session.
- Completed debate results can be downloaded as Markdown or HTML.

Recommended next UI improvements:

1. **Use a more chat-like result display**
   - Consider `st.chat_input()` and `st.chat_message()` for a familiar chat layout.
   - Display each agent as a separate participant:
     - User
     - Agent 1 / Analyst
     - Agent 2 / Critic
     - Agent 3 / Summarizer

2. **Improve debate controls**
   - Add a setting for the number of debate rounds.
   - Add a setting for custom agent names or roles.
   - Add optional streaming/progressive output if the backend supports it.

3. **Possible popular UI directions**
   - Short term: continue improving the current Streamlit app.
   - Later: Gradio ChatInterface for a simple public demo.
   - Later: React/Next.js chat frontend if the project needs a more polished web app.


# Contribution

Credit to o3 Mini

AI-coding assist: gpt-4o, o3 Mini


# References

[Multiagent debate by autoGen](https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/multi-agent-debate.html)

[MAD](https://github.com/Skytliang/Multi-Agents-Debate)

Tech stacks: streamlit, DSpy




<!--
# To-do notes

debate_250416.py + ollama_api.py

could be visulized in the UI

but will ocur errors when using ollama api

ERROR: format of api?
-->
