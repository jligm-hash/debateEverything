import streamlit as st
from langchain_community.chat_models.ollama import ChatOllama

def get_ollama_response(prompt, role, temperature=0.7):
    """
    Combines a system-defined role with the user's prompt and queries the local Ollama model.
    
    Parameters:
      - prompt (str): The debate or critique prompt.
      - role (str): The designated role (e.g., "analytical agent", "critical agent", "summarizer agent").
      - temperature (float): Controls randomness in the model's output.
      
    Returns:
      - The generated response as a string.
    """
    # Create a system message that communicates the agent's role.
    system_message = f"You are a {role} in a structured debate workflow. Act accordingly."
    # Combine the system instruction with the provided prompt.
    full_prompt = f"{system_message}\n\n{prompt}"
    
    # Instantiate and call the ChatOllama model.
    ollama = ChatOllama(model="deepseek-r1:7b", temperature=temperature)
    response = ollama(full_prompt)
    
    return response.content.strip()

# --- Streamlit UI for Multi-Agent Debate Workflow ---

st.title("Multi-Agent Debate Workflow using Ollama API")

# Input area for the debate prompt.
input_prompt = st.text_area("Enter your debate prompt:", placeholder="Type your prompt here...")

if st.button("Start Debate"):
    if input_prompt.strip():
        # Agent 1: Initial Analysis.
        st.markdown("## Agent 1: Initial Analysis")
        agent1_analysis = get_ollama_response(input_prompt, "analytical agent")
        st.write(agent1_analysis)

        # Agent 2: Critique of Agent 1's Analysis.
        st.markdown("## Agent 2: Critique of Agent 1")
        agent2_critique_prompt = f"Critically evaluate the following analysis:\n\n{agent1_analysis}"
        agent2_critique = get_ollama_response(agent2_critique_prompt, "critical agent")
        st.write(agent2_critique)

        # Agent 1: Feedback to Agent 2's Critique.
        st.markdown("## Agent 1: Feedback to Agent 2")
        agent1_feedback_prompt = (
            "Based on the following critique, refine your initial analysis and respond to the concerns raised.\n\n"
            f"Critique: {agent2_critique}\n\n"
            f"Original Analysis: {agent1_analysis}"
        )
        agent1_feedback = get_ollama_response(agent1_feedback_prompt, "analytical agent")
        st.write(agent1_feedback)

        # Agent 2: Further Critique After Feedback.
        st.markdown("## Agent 2: Further Critique")
        agent2_feedback_prompt = (
            "Taking into account the updated analysis and Agent 1's response, further refine your critique.\n\n"
            f"Agent 1's Feedback: {agent1_feedback}\n\n"
            f"Initial Critique: {agent2_critique}"
        )
        agent2_feedback = get_ollama_response(agent2_feedback_prompt, "critical agent")
        st.write(agent2_feedback)

        # Agent 3: Summary and Conclusion.
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




# import streamlit as st
# from ollama_api import get_ollama_response

# st.title("Multi-Agent Debate Workflow using Ollama API")

# # Input for the debate prompt
# input_prompt = st.text_area("Enter your debate prompt:", placeholder="Type your prompt here...")

# if st.button("Start Debate"):
#     if input_prompt:
#         # Agent 1: Initial Analysis
#         st.markdown("## Agent 1: Initial Analysis")
#         agent1_analysis = get_ollama_response(input_prompt, "analytical agent")
#         st.write(agent1_analysis)

#         # Agent 2: Critique of Agent 1's Analysis
#         st.markdown("## Agent 2: Critique of Agent 1")
#         agent2_critique_prompt = f"Critically evaluate the following analysis:\n\n{agent1_analysis}"
#         agent2_critique = get_ollama_response(agent2_critique_prompt, "critical agent")
#         st.write(agent2_critique)

#         # Agent 1: Feedback to Agent 2's Critique
#         st.markdown("## Agent 1: Feedback to Agent 2")
#         agent1_feedback_prompt = (
#             "Based on the following critique, refine your initial analysis and respond to the concerns raised.\n\n"
#             f"Critique: {agent2_critique}\n\n"
#             f"Original Analysis: {agent1_analysis}"
#         )
#         agent1_feedback = get_ollama_response(agent1_feedback_prompt, "analytical agent")
#         st.write(agent1_feedback)

#         # Agent 2: Further Critique After Feedback
#         st.markdown("## Agent 2: Further Critique")
#         agent2_feedback_prompt = (
#             "Taking into account the updated analysis and Agent 1's response, further refine your critique.\n\n"
#             f"Agent 1's Feedback: {agent1_feedback}\n\n"
#             f"Initial Critique: {agent2_critique}"
#         )
#         agent2_feedback = get_ollama_response(agent2_feedback_prompt, "critical agent")
#         st.write(agent2_feedback)

#         # Agent 3: Summary and Conclusion
#         st.markdown("## Agent 3: Summary and Conclusion")
#         summary_prompt = (
#             "Summarize the entire debate by extracting key points, insights, and conclusions from the discussion. "
#             "Include the initial analysis, the critiques, and the iterative feedback.\n\n"
#             f"Agent 1 Analysis: {agent1_analysis}\n\n"
#             f"Agent 2 Initial Critique: {agent2_critique}\n\n"
#             f"Agent 1 Feedback: {agent1_feedback}\n\n"
#             f"Agent 2 Further Critique: {agent2_feedback}"
#         )
#         agent3_summary = get_ollama_response(summary_prompt, "summarizer agent")
#         st.write(agent3_summary)
#     else:
#         st.error("Please provide a debate prompt!")
