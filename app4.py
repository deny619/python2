import streamlit as st
import openai
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Initialize Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=testddungranistrg;AccountKey=0/OUNLoLs3cZnUtjZyJ7XX8w1NwsEbYjNrIatKkiTjrTrR/+raRssrNB+mncUQ7s5MhYumKBlLFj+ASt42evIA==;EndpointSuffix=core.windows.net")
container_name = "test"

# Function to check user credentials
def check_credentials(username, password):
    container_client = blob_service_client.get_container_client(container_name)
    blob_name = "user_credentials.txt"
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob()
    user_credentials = blob_data.readall().decode('utf-8')
    user_credentials = user_credentials.split('\n')
    for line in user_credentials:
        user, stored_password = line.split(',')
        if user.strip() == username and stored_password.strip() == password:
            return True
    return False

# Streamlit UI
st.title("Conversational AI with OpenAI")

# Add a login section
st.sidebar.subheader("Login")
username = st.sidebar.text_input("Username:")
password = st.sidebar.text_input("Password:", type="password")

# Check if the login button is clicked
if st.sidebar.button("Login"):
    if check_credentials(username, password):
        st.sidebar.success("Login Successful")
        logged_in = True
    else:
        st.sidebar.error("Login Failed. Please check your credentials.")
        logged_in = False
else:
    logged_in = False

if logged_in:
    # Set your OpenAI API key here
    openai.api_type = "azure"
    openai.api_key = "892e9ea60b554ab3a29ca5c0663ac42a"
    openai.api_base = "https://openai-ddungrani.openai.azure.com/"
    openai.api_version = "2023-05-15"

    conversation = []

    # Define the available OpenAI engines
    engines = {
        "text-davinci-003": "Text Davinci",
        "gpt-35-turbo": "GPT-3.5 Turbo",
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
else:
    st.warning("Please log in to use the Conversational AI.")
