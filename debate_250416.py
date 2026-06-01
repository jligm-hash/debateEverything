import streamlit as st

from ollama_api import API_MODE, get_ollama_response


# Rewritten debate workflow.
# Previous versions of this file are preserved in previous/debate_250416_previous.py.
# This file handles the Streamlit UI and debate sequence.
# Ollama/OpenAI-compatible API details live in ollama_api.py.

st.title("Multi-Agent Debate Workflow using Ollama API")
st.caption(f"Current API mode: {API_MODE}")

# Input area for the debate prompt.
input_prompt = st.text_area("Enter your debate prompt:", placeholder="Type your prompt here...")

if st.button("Start Debate"):
    if input_prompt.strip():
        with st.spinner("Running the multi-agent debate..."):
            # Agent 1: create the first analysis from the user's debate prompt.
            st.markdown("## Agent 1: Initial Analysis")
            agent1_analysis = get_ollama_response(input_prompt, "analytical agent")
            st.write(agent1_analysis)

            # Agent 2: challenge Agent 1's analysis and identify weak points.
            st.markdown("## Agent 2: Critique of Agent 1")
            agent2_critique_prompt = f"Critically evaluate the following analysis:\n\n{agent1_analysis}"
            agent2_critique = get_ollama_response(agent2_critique_prompt, "critical agent")
            st.write(agent2_critique)

            # Agent 1: respond to the critique and refine the original analysis.
            st.markdown("## Agent 1: Feedback to Agent 2")
            agent1_feedback_prompt = (
                "Based on the following critique, refine your initial analysis and respond to the concerns raised.\n\n"
                f"Critique: {agent2_critique}\n\n"
                f"Original Analysis: {agent1_analysis}"
            )
            agent1_feedback = get_ollama_response(agent1_feedback_prompt, "analytical agent")
            st.write(agent1_feedback)

            # Agent 2: critique again after Agent 1's refined response.
            st.markdown("## Agent 2: Further Critique")
            agent2_feedback_prompt = (
                "Taking into account the updated analysis and Agent 1's response, further refine your critique.\n\n"
                f"Agent 1's Feedback: {agent1_feedback}\n\n"
                f"Initial Critique: {agent2_critique}"
            )
            agent2_feedback = get_ollama_response(agent2_feedback_prompt, "critical agent")
            st.write(agent2_feedback)

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
            agent3_summary = get_ollama_response(summary_prompt, "summarizer agent")
            st.write(agent3_summary)
    else:
        st.error("Please provide a debate prompt!")
