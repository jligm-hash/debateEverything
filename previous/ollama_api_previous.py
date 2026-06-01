
from langchain_community.chat_models.ollama import ChatOllama

def get_ollama_response(prompt, role, temperature=0.7):
    """
    Sends a prompt to your local Ollama instance using ChatOllama.
    The API endpoint used internally should match the tested one:
    http://127.0.0.1:11434/api/generate
    """
    # Prepare a system message to introduce the agent's role.
    system_message = f"You are a {role} in a structured debate workflow. Act accordingly."
    
    # Build the messages list for the chat model.
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user",   "content": prompt}
    ]
    
    # Instantiate the ChatOllama model.
    # If needed, pass a custom endpoint argument (uncomment the next line if supported).
    # ollama = ChatOllama(model="deepseek-r1:7b", temperature=temperature, endpoint="http://127.0.0.1:11434/api/generate")
    ollama = ChatOllama(model="deepseek-r1:7b", temperature=temperature)
    
    # Get the response from the model.
    response = ollama(messages)
    return response.content.strip()


# from langchain_community.chat_models.ollama import ChatOllama

# def get_ollama_response(prompt, role, temperature=0.7):
#     """
#     Sends a prompt with role instructions to a local Ollama model using langchain_community.chat_models.

#     Parameters:
#       - prompt (str): The content prompt.
#       - role (str): The role for the agent (e.g., "analytical agent", "critical agent", "summarizer agent").
#       - temperature (float): Controls randomness in the response.

#     Returns:
#       - The generated response as a string.
#     """
#     # Define a system prompt that sets the desired role of the agent.
#     system_message = f"You are a {role} in a structured debate workflow. Act accordingly."

#     # Build the list of messages expected for a conversational model.
#     messages = [
#         {"role": "system", "content": system_message},
#         {"role": "user",   "content": prompt}
#     ]
    
#     # Initialize the ChatOllama model with desired parameters.
#     # Note: Replace "deepseek-r1:7b" with the appropriate model identifier if needed.
#     ollama = ChatOllama(model="deepseek-r1:7b", temperature=temperature)
    
#     # Generate the response by passing the messages list to the model.
#     response = ollama(messages)
    
#     # Return the chat response content (adjust extraction if your response format is different).
#     return response.content.strip()


# import requests

# def get_ollama_response(prompt, role, temperature=0.7):
#     """
#     Sends a prompt with role instructions to the local Ollama API.

#     Parameters:
#       - prompt (str): The content prompt.
#       - role (str): The specific role (e.g., "analytical agent", "critical agent", "summarizer agent").
#       - temperature (float): Controls randomness in the response.

#     Returns:
#       - The generated response as text.
#     """
#     # Prepend a system-like instruction to define the agent's role.
#     system_prompt = f"You are a {role} in a structured debate workflow. Act accordingly."
#     full_prompt = f"{system_prompt}\n\n{prompt}"

#     # Payload definition — adjust model or other parameters if needed.
#     payload = {
#         "model": "deepseek-r1:7b",  # Replace with the appropriate model identifier in your Ollama setup.
#         "prompt": full_prompt,
#         "parameters": {
#             "temperature": temperature
#         }
#     }

#     # Ollama API endpoint for local usage.
#     url = "http://localhost:11434/run"
#     headers = {"Content-Type": "application/json"}

#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         if response.status_code == 200:
#             data = response.json()
#             # Adjust the key if your response format is different.
#             return data.get("text", "").strip()
#         else:
#             return f"Error {response.status_code}: {response.text}"
#     except Exception as e:
#         return f"Exception occurred: {e}"
