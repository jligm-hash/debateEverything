# debateEverything

Use agent framework to debate everything

<p align="center">
    <img src="src/pixlr-image-generator-ea0aad69-efbf-48ca-b796-61e5a633d34a.png"
    title="Agent debate"
    width="400" >
</p>


# To-do notes

- `debate_250416.py` now uses `ollama_api.py` for the local Ollama `/api/chat` request format.
- `ollama_api.py` keeps Ollama as the default API and can also call an OpenAI-compatible `/chat/completions` API.
- Keep `debate_dspy_250416.py` as the currently smooth-running DSPy reference version.
- Previous code snapshots are stored in `previous/` before the rewrite.


# Archive

Previous versions of the main Python files are stored in `previous/`.
These files are preserved before rewriting so old code is not deleted.


# Version control

- debate_dspy_250416 is to debate the claims

- debate_code is to debate the codes

# Files

After testing, only debate_dspy_250416.py could run smoothly

# How to run

Stable DSPy debate version:

`streamlit run debate_dspy_250416.py`

Rewritten Ollama API debate version:

`streamlit run debate_250416.py`

By default, the rewritten version calls Ollama. To use an OpenAI-compatible API instead, set `DEBATE_API_MODE=openai`, `OPENAI_BASE_URL`, and `OPENAI_MODEL` before running the app.

Code debate version:

`streamlit run debate_code_250417.py`


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