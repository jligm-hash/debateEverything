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

By default, this version calls local Ollama at:

```text
http://localhost:11434/api/chat
```

Default model:

```text
deepseek-r1:7b
```

You can override the default Ollama settings with environment variables:

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

Set these environment variables before running the app:

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


# Current API behavior

`debate_250416.py` calls:

```python
get_ollama_response(prompt, role, temperature=0.7)
```

from `ollama_api.py`.

`ollama_api.py` then chooses the backend:

- default: Ollama native `/api/chat`
- optional: OpenAI-compatible `/chat/completions`

The active app keeps the debate workflow separate from API details.


# UI optimization plan

The current UI is a simple Streamlit page with one text input and sequential output sections. It works for early testing, but the next improvement should make the app feel more like a real chat/debate product.

Recommended plan:

1. **Create a new UI version instead of replacing the current one first**
   - Add a new file such as `debate_ui_v2.py`.
   - Keep `debate_250416.py` as the stable rewritten baseline.
   - Reuse `ollama_api.py` so the new UI does not duplicate API code.

2. **Use a chat-style layout**
   - Use Streamlit chat components such as `st.chat_input()` and `st.chat_message()`.
   - Display each agent as a separate chat participant:
     - User
     - Agent 1 / Analyst
     - Agent 2 / Critic
     - Agent 3 / Summarizer
   - Use avatars or labels to make the debate easier to follow.

3. **Improve user controls**
   - Add a sidebar for:
     - API mode: Ollama or OpenAI-compatible
     - model name
     - temperature
     - number of debate rounds
   - Add a clear button to reset the conversation.

4. **Improve output quality**
   - Stream or progressively show each agent response if possible.
   - Save the debate history in `st.session_state`.
   - Allow the user to download the debate result as Markdown.

5. **Possible popular UI directions**
   - Short term: Streamlit chat UI, because the project already uses Streamlit.
   - Later: Gradio ChatInterface for a simple public demo.
   - Later: React/Next.js chat frontend if the project needs a more polished web app.

The recommended next implementation is `debate_ui_v2.py` using Streamlit chat components, while keeping all current files unchanged as references.


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
