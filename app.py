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

# Function to generate AI response
def generate_response(input_text):
    conversation.append(f"You: {input_text}")
    response = openai.Completion.create(
        engine="gpt-35-turbo",  # Use the engine of your choice
        prompt="\n".join(conversation),
        max_tokens=50  # Adjust as needed
    )
    conversation.append(f"AI: {response.choices[0].text}")
    return response.choices[0].text

user_input = st.text_input("You:", "")
if st.button("Ask") and user_input:
    ai_response = generate_response(user_input)
    st.text(ai_response)

