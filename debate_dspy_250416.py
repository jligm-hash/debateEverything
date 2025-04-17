
import streamlit as st
import dspy

# Configure dspy to use your local Ollama model.
lm = dspy.LM('ollama_chat/deepseek-r1:7b', api_base='http://localhost:11434', api_key='')
dspy.configure(lm=lm)

def get_dspy_response(prompt, role, temperature=0.7):
    """
    Combines a system instruction with the user prompt and queries the local deepseek model via dspy.
    
    Parameters:
      - prompt (str): The input prompt.
      - role (str): The agent role (e.g., "analytical agent", "critical agent", "summarizer agent").
      - temperature (float): Controls randomness in the output.
    
    Returns:
      - A string with the generated response.
    """
    # Create a system instruction based on the role.
    system_message = f"You are a {role} in a structured debate workflow. Act accordingly."
    # Combine the system instruction with the user prompt.
    full_prompt = system_message + "\n\n" + prompt
    # Get the model response using dspy
    response = lm(full_prompt, temperature=temperature)
    
    # If the response is a list, join its elements or select the first one.
    if isinstance(response, list):
        # Option 1: Join all items assuming they are strings.
        return " ".join(response).strip()
        # Option 2: Alternatively, if you expect one-string responses, you could use:
        # return response[0].strip() if response else ""
    else:
        return response.strip()
        

# --- Streamlit UI ---


st.title("Multi-Agent Debate Workflow using dspy and Ollama API")

# Input for the debate prompt.
input_prompt = st.text_area("Enter your debate prompt:", placeholder="Type your prompt here...")

if st.button("Start Debate"):
    if input_prompt.strip():
        # Agent 1: Initial Analysis.
        st.markdown("## 🧠 Agent 1: Initial Analysis")
        agent1_analysis = get_dspy_response(input_prompt, "analytical agent")
        st.write(agent1_analysis)
        st.markdown("---")

        # Agent 2: Critique of Agent 1's Analysis.
        st.markdown("## 🧐 Agent 2: Critique of Agent 1")
        agent2_critique_prompt = f"Critically evaluate the following analysis:\n\n{agent1_analysis}"
        agent2_critique = get_dspy_response(agent2_critique_prompt, "critical agent")
        st.write(agent2_critique)
        st.markdown("---")

        # Agent 1: Feedback to Agent 2's Critique.
        st.markdown("## 🧠 Agent 1: Feedback to Agent 2")
        agent1_feedback_prompt = (
            "Based on the following critique, refine your original analysis and respond to the concerns raised.\n\n"
            f"Critique: {agent2_critique}\n\n"
            f"Original Analysis: {agent1_analysis}"
        )
        agent1_feedback = get_dspy_response(agent1_feedback_prompt, "analytical agent")
        st.write(agent1_feedback)
        st.markdown("---")

        # Agent 2: Further Critique.
        st.markdown("## 🧐 Agent 2: Further Critique")
        agent2_feedback_prompt = (
            "Taking into account the updated analysis and your previous critique, further refine your evaluation.\n\n"
            f"Agent 1's Feedback: {agent1_feedback}\n\n"
            f"Initial Critique: {agent2_critique}"
        )
        agent2_feedback = get_dspy_response(agent2_feedback_prompt, "critical agent")
        st.write(agent2_feedback)
        st.markdown("---")

        # Agent 3: Summary and Conclusion.
        st.markdown("## 💡 Agent 3: Summary and Conclusion")
        summary_prompt = (
            "Summarize the entire debate by extracting key points, insights, and conclusions from the discussion. "
            "Include the initial analysis, the critiques, and the iterative feedback.\n\n"
            f"Agent 1 Analysis: {agent1_analysis}\n\n"
            f"Agent 2 Initial Critique: {agent2_critique}\n\n"
            f"Agent 1 Feedback: {agent1_feedback}\n\n"
            f"Agent 2 Further Critique: {agent2_feedback}"
        )
        agent3_summary = get_dspy_response(summary_prompt, "summarizer agent")
        st.write(agent3_summary)
    else:
        st.error("Please provide a debate prompt!")



# st.title("Multi-Agent Debate Workflow using dspy and Ollama API")

# # User input for a debate prompt.
# input_prompt = st.text_area("Enter your debate prompt:", placeholder="Type your prompt here...")

# if st.button("Start Debate"):
#     if input_prompt.strip():
#         # Agent 1: Initial Analysis.
#         st.markdown("## Agent 1: Initial Analysis")
#         agent1_analysis = get_dspy_response(input_prompt, "analytical agent")
#         st.write(agent1_analysis)

#         # Agent 2: Critique of Agent 1's Analysis.
#         st.markdown("## Agent 2: Critique of Agent 1")
#         agent2_critique_prompt = f"Critically evaluate the following analysis:\n\n{agent1_analysis}"
#         agent2_critique = get_dspy_response(agent2_critique_prompt, "critical agent")
#         st.write(agent2_critique)

#         # Agent 1: Feedback to Agent 2's Critique.
#         st.markdown("## Agent 1: Feedback to Agent 2")
#         agent1_feedback_prompt = (
#             "Based on the following critique, refine your initial analysis and respond to the concerns raised.\n\n"
#             f"Critique: {agent2_critique}\n\n"
#             f"Original Analysis: {agent1_analysis}"
#         )
#         agent1_feedback = get_dspy_response(agent1_feedback_prompt, "analytical agent")
#         st.write(agent1_feedback)

#         # Agent 2: Further Critique.
#         st.markdown("## Agent 2: Further Critique")
#         agent2_feedback_prompt = (
#             "Taking into account the updated analysis and your previous critique, further refine your evaluation.\n\n"
#             f"Agent 1's Feedback: {agent1_feedback}\n\n"
#             f"Initial Critique: {agent2_critique}"
#         )
#         agent2_feedback = get_dspy_response(agent2_feedback_prompt, "critical agent")
#         st.write(agent2_feedback)

#         # Agent 3: Summary and Conclusion.
#         st.markdown("## Agent 3: Summary and Conclusion")
#         summary_prompt = (
#             "Summarize the entire debate by extracting the key points, insights, and conclusions from the discussion. "
#             "Include the initial analysis, the critiques, and the iterative feedback.\n\n"
#             f"Agent 1 Analysis: {agent1_analysis}\n\n"
#             f"Agent 2 Initial Critique: {agent2_critique}\n\n"
#             f"Agent 1 Feedback: {agent1_feedback}\n\n"
#             f"Agent 2 Further Critique: {agent2_feedback}"
#         )
#         agent3_summary = get_dspy_response(summary_prompt, "summarizer agent")
#         st.write(agent3_summary)
#     else:
#         st.error("Please provide a debate prompt!")
