from html import escape

import streamlit as st

from ollama_api import get_default_api_settings, get_ollama_response


# Rewritten debate workflow.
# Previous versions of this file are preserved in previous/debate_250416_previous.py.
# This file handles the Streamlit UI and debate sequence.
# Ollama/OpenAI-compatible API details live in ollama_api.py.


def initialize_api_settings():
    """Initialize session-only API settings from environment defaults."""
    defaults = get_default_api_settings()

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)

    st.session_state.setdefault("temperature", 0.7)
    st.session_state.setdefault("api_test_result", "")
    st.session_state.setdefault("debate_prompt", "")
    st.session_state.setdefault("debate_results", [])


def render_api_settings():
    """Render current-session settings in the sidebar without saving secrets."""
    initialize_api_settings()

    with st.sidebar:
        st.header("Debate controls")
        st.caption("Configure, test, run, and export from here.")

        with st.expander("API settings for this session", expanded=False):
            st.caption(
                "These settings are kept only in the current Streamlit session. "
                "They are not written to files or committed to git."
            )

            api_mode = st.selectbox(
                "API mode",
                options=["ollama", "openai-compatible"],
                key="api_mode",
                help="Ollama is the default. OpenAI-compatible mode calls /chat/completions.",
            )

            if api_mode == "ollama":
                st.text_input(
                    "Ollama API link",
                    key="ollama_base_url",
                    help="Base URL for Ollama. The app adds /api/chat or /api/generate automatically.",
                )
                st.text_input("Ollama model name", key="ollama_model")
                st.selectbox(
                    "Ollama format",
                    options=["chat", "generate"],
                    key="ollama_format",
                    help="Use chat for /api/chat. Use generate for /api/generate.",
                )
            else:
                st.text_input(
                    "OpenAI-compatible API link",
                    key="openai_base_url",
                    help="Base URL that contains /chat/completions, such as http://localhost:1234/v1.",
                )
                st.text_input("OpenAI-compatible model name", key="openai_model")
                st.text_input(
                    "API key / token",
                    key="openai_api_key",
                    type="password",
                    help="Optional for local servers that do not require authentication.",
                )

            st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=float(st.session_state.get("temperature", 0.7)),
                step=0.1,
                key="temperature",
            )

            if st.button("Reset API settings", use_container_width=True):
                for key in [
                    "api_mode",
                    "ollama_base_url",
                    "ollama_model",
                    "ollama_format",
                    "openai_base_url",
                    "openai_model",
                    "openai_api_key",
                    "temperature",
                ]:
                    st.session_state.pop(key, None)
                st.rerun()

    return {
        "api_mode": st.session_state["api_mode"],
        "ollama_base_url": st.session_state["ollama_base_url"],
        "ollama_model": st.session_state["ollama_model"],
        "ollama_format": st.session_state["ollama_format"],
        "openai_base_url": st.session_state["openai_base_url"],
        "openai_model": st.session_state["openai_model"],
        "openai_api_key": st.session_state["openai_api_key"],
    }, st.session_state["temperature"]


def get_active_model(api_settings):
    """Return the visible model name for the selected backend."""
    if api_settings["api_mode"] == "ollama":
        return api_settings["ollama_model"]

    return api_settings["openai_model"]


def validate_api_settings(api_settings):
    """Validate only API settings, without requiring a debate prompt."""
    if api_settings["api_mode"] == "ollama":
        if not api_settings["ollama_base_url"].strip():
            return "Please provide an Ollama API link."
        if not api_settings["ollama_model"].strip():
            return "Please provide an Ollama model name."
        return None

    if not api_settings["openai_base_url"].strip():
        return "Please provide an OpenAI-compatible API link."
    if not api_settings["openai_model"].strip():
        return "Please provide an OpenAI-compatible model name."

    return None


def validate_settings(api_settings, input_prompt):
    """Validate prompt and session settings before running the debate."""
    if not input_prompt.strip():
        return "Please provide a debate prompt!"

    return validate_api_settings(api_settings)


def run_agent(prompt, role, temperature, api_settings):
    """Run one debate agent with the current session API settings."""
    return get_ollama_response(
        prompt,
        role,
        temperature=temperature,
        api_settings=api_settings,
    )


def add_result(title, role, content):
    """Store one debate result for rerendering and export."""
    st.session_state["debate_results"].append(
        {
            "title": title,
            "role": role,
            "content": content,
        }
    )


def render_debate_results(results):
    """Render stored debate results after Streamlit reruns."""
    for result in results:
        st.markdown(f"## {result['title']}")
        st.write(result["content"])


def build_markdown_export(prompt, results, api_settings, temperature):
    """Build a Markdown export without including API secrets."""
    active_model = get_active_model(api_settings)
    lines = [
        "# Multi-Agent Debate Result",
        "",
        "## Prompt",
        "",
        prompt,
        "",
        "## API Session",
        "",
        f"- Mode: {api_settings['api_mode']}",
        f"- Model: {active_model}",
        f"- Temperature: {temperature}",
    ]

    if api_settings["api_mode"] == "ollama":
        lines.append(f"- Ollama format: {api_settings['ollama_format']}")

    lines.extend(["", "## Debate", ""])

    for result in results:
        lines.extend(
            [
                f"### {result['title']}",
                "",
                result["content"],
                "",
            ]
        )

    return "\n".join(lines)


def build_html_export(prompt, results, api_settings, temperature):
    """Build a self-contained HTML export without including API secrets."""
    active_model = get_active_model(api_settings)
    format_line = ""

    if api_settings["api_mode"] == "ollama":
        format_line = f"<li>Ollama format: {escape(api_settings['ollama_format'])}</li>"

    result_sections = []
    for result in results:
        result_sections.append(
            f"""
            <section class="agent-result">
                <h3>{escape(result['title'])}</h3>
                <p class="role">Role: {escape(result['role'])}</p>
                <pre>{escape(result['content'])}</pre>
            </section>
            """
        )

    return f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Multi-Agent Debate Result</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.5; margin: 2rem; }}
        .prompt, .agent-result {{ border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin: 1rem 0; }}
        .role {{ color: #666; font-size: 0.9rem; }}
        pre {{ white-space: pre-wrap; font-family: inherit; }}
    </style>
</head>
<body>
    <h1>Multi-Agent Debate Result</h1>
    <section class="prompt">
        <h2>Prompt</h2>
        <pre>{escape(prompt)}</pre>
    </section>
    <section>
        <h2>API Session</h2>
        <ul>
            <li>Mode: {escape(api_settings['api_mode'])}</li>
            <li>Model: {escape(active_model)}</li>
            <li>Temperature: {temperature}</li>
            {format_line}
        </ul>
    </section>
    <section>
        <h2>Debate</h2>
        {''.join(result_sections)}
    </section>
</body>
</html>"""


def render_api_summary(api_settings, temperature):
    """Show a short sidebar summary without displaying secrets."""
    active_model = get_active_model(api_settings)

    with st.sidebar:
        st.subheader("Current session")
        st.caption(f"Mode: {api_settings['api_mode']}")
        st.caption(f"Model: {active_model}")
        st.caption(f"Temperature: {temperature}")

        if api_settings["api_mode"] == "ollama":
            st.caption(f"Ollama format: {api_settings['ollama_format']}")


def render_api_test_panel(api_settings, temperature):
    """Render a sidebar panel for testing the selected API settings."""
    with st.sidebar:
        with st.expander("Test API connection", expanded=True):
            st.caption("Send a short test prompt before starting a debate.")

            if st.button("Test API", use_container_width=True):
                validation_error = validate_api_settings(api_settings)

                if validation_error:
                    st.session_state["api_test_result"] = validation_error
                else:
                    with st.spinner("Testing API connection..."):
                        st.session_state["api_test_result"] = run_agent(
                            "Reply with one short sentence confirming the API works.",
                            "API connection tester",
                            temperature,
                            api_settings,
                        )

            result = st.session_state.get("api_test_result")
            if result:
                if result.startswith("Error:") or result.startswith("Please "):
                    st.error(result)
                else:
                    st.success("API test completed.")
                    st.caption(result)


def render_export_panel(api_settings, temperature):
    """Render sidebar controls for clearing and exporting current debate results."""
    results = st.session_state.get("debate_results", [])
    prompt = st.session_state.get("debate_prompt", "")
    has_results = bool(results)

    with st.sidebar:
        with st.expander("Export session", expanded=has_results):
            if not has_results:
                st.caption("Run a debate to enable Markdown and HTML downloads.")
            else:
                markdown_data = build_markdown_export(prompt, results, api_settings, temperature)
                html_data = build_html_export(prompt, results, api_settings, temperature)

                st.download_button(
                    "Download Markdown",
                    data=markdown_data,
                    file_name="debate_session.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
                st.download_button(
                    "Download HTML",
                    data=html_data,
                    file_name="debate_session.html",
                    mime="text/html",
                    use_container_width=True,
                )

            if st.button("Clear debate session", use_container_width=True):
                st.session_state["debate_prompt"] = ""
                st.session_state["debate_results"] = []
                st.rerun()


def run_debate(input_prompt, temperature, api_settings):
    """Run the full multi-agent debate and store results for export."""
    st.session_state["debate_prompt"] = input_prompt
    st.session_state["debate_results"] = []

    with st.spinner("Running the multi-agent debate..."):
        # Agent 1: create the first analysis from the user's debate prompt.
        st.markdown("## Agent 1: Initial Analysis")
        agent1_analysis = run_agent(input_prompt, "analytical agent", temperature, api_settings)
        st.write(agent1_analysis)
        add_result("Agent 1: Initial Analysis", "analytical agent", agent1_analysis)

        # Agent 2: challenge Agent 1's analysis and identify weak points.
        st.markdown("## Agent 2: Critique of Agent 1")
        agent2_critique_prompt = f"Critically evaluate the following analysis:\n\n{agent1_analysis}"
        agent2_critique = run_agent(agent2_critique_prompt, "critical agent", temperature, api_settings)
        st.write(agent2_critique)
        add_result("Agent 2: Critique of Agent 1", "critical agent", agent2_critique)

        # Agent 1: respond to the critique and refine the original analysis.
        st.markdown("## Agent 1: Feedback to Agent 2")
        agent1_feedback_prompt = (
            "Based on the following critique, refine your initial analysis and respond to the concerns raised.\n\n"
            f"Critique: {agent2_critique}\n\n"
            f"Original Analysis: {agent1_analysis}"
        )
        agent1_feedback = run_agent(agent1_feedback_prompt, "analytical agent", temperature, api_settings)
        st.write(agent1_feedback)
        add_result("Agent 1: Feedback to Agent 2", "analytical agent", agent1_feedback)

        # Agent 2: critique again after Agent 1's refined response.
        st.markdown("## Agent 2: Further Critique")
        agent2_feedback_prompt = (
            "Taking into account the updated analysis and Agent 1's response, further refine your critique.\n\n"
            f"Agent 1's Feedback: {agent1_feedback}\n\n"
            f"Initial Critique: {agent2_critique}"
        )
        agent2_feedback = run_agent(agent2_feedback_prompt, "critical agent", temperature, api_settings)
        st.write(agent2_feedback)
        add_result("Agent 2: Further Critique", "critical agent", agent2_feedback)

        # Agent 3: summarize the full debate into final takeaways.
        st.markdown("## Agent 3: Summary and Conclusion")
        summary_prompt = (
            "Summarize the entire debate by extracting key points, insights, and conclusions from the discussion. "
            "Include the initial analysis, the critiques, and the iterative feedback.\n\n"
            f"Agent 1 Analysis: {agent1_analysis}\n\n"
            f"Agent 2 Initial Critique: {agent2_critique}\n\n"
            f"Agent 1 Feedback: {agent1_feedback}\n\n"
            f"Agent 2 Further Critique: {agent2_feedback}"
        )
        agent3_summary = run_agent(summary_prompt, "summarizer agent", temperature, api_settings)
        st.write(agent3_summary)
        add_result("Agent 3: Summary and Conclusion", "summarizer agent", agent3_summary)


st.set_page_config(page_title="Multi-Agent Debate Workflow", layout="wide")
st.title("Multi-Agent Debate Workflow")
st.caption("Configure API settings in the sidebar, test the connection, then run the debate.")

api_settings, temperature = render_api_settings()
render_api_summary(api_settings, temperature)
render_api_test_panel(api_settings, temperature)
render_export_panel(api_settings, temperature)

# Input area for the debate prompt.
input_prompt = st.text_area("Enter your debate prompt:", placeholder="Type your prompt here...")
debate_started = st.button("Start Debate", type="primary")

if debate_started:
    validation_error = validate_settings(api_settings, input_prompt)

    if validation_error:
        st.error(validation_error)
    else:
        run_debate(input_prompt, temperature, api_settings)
elif st.session_state.get("debate_results"):
    st.markdown("## Latest debate session")
    render_debate_results(st.session_state["debate_results"])
