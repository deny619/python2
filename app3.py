import streamlit as st
import openai

# Set your OpenAI API key here
openai.api_type = "azure"
openai.api_key = "892e9ea60b554ab3a29ca5c0663ac42a"
openai.api_base = "https://openai-ddungrani.openai.azure.com/"
openai.api_version = "2023-05-15"

# Streamlit UI
st.title("Conversational AI with OpenAI")
conversation = []

# Define the available OpenAI engines
engines = {
    "text-davinci-003": "Text Davinci",
    "gpt-35-turbo": "GPT-3.5 Turbo"
}

# Allow the user to select the engine using checkboxes
selected_engine = st.selectbox("Select an OpenAI Engine:", list(engines.values()))

# Function to generate AI response
def generate_response(input_text, engine):
    user_prompt = f"You: {input_text}"
    conversation.append(user_prompt)
    response = openai.Completion.create(
        engine=engine,  # Use the selected engine
        prompt="\n".join(conversation),
        max_tokens=50  # Adjust as needed
    )
    ai_response = response.choices[0].text
    conversation.append(f"AI: {ai_response}")
    return user_prompt, ai_response

user_input = st.text_input("You:", "")
if st.button("Ask") and user_input:
    selected_engine_key = [key for key, value in engines.items() if value == selected_engine][0]
    user_prompt, ai_response = generate_response(user_input, selected_engine_key)
    st.text(user_prompt)
    st.text(ai_response)
