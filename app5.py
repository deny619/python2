import streamlit as st
import openai
import sqlite3
import bcrypt

# Initialize SQLite database
conn = sqlite3.connect("conversation_history.db")
cursor = conn.cursor()

# Create a table to store user credentials if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, hashed_password TEXT)")

# Initialize the logged_in variable
logged_in = False

# Streamlit UI
st.title("Conversational AI with OpenAI")

# Add a login section
st.sidebar.subheader("Login")
username = st.sidebar.text_input("Username:")
password = st.sidebar.text_input("Password:", type="password")

# Check if the login button is clicked
if st.sidebar.button("Login"):
    # Fetch the hashed password for the entered username from the database
    cursor.execute("SELECT hashed_password FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    
    if user_data:
        hashed_password_from_db = user_data[0]
        
        # Verify the entered password against the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db.encode('utf-8')):
            st.sidebar.success("Login Successful")
            logged_in = True
        else:
            st.sidebar.error("Login Failed. Please check your credentials.")

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
            engine=engine,
            prompt="\n".join(conversation),
            max_tokens=50
        )
        ai_response = response.choices[0].text
        conversation.append(f"AI: {ai_response}")
        
        # Store the conversation history in the database
        cursor.execute("INSERT INTO conversation (user_input, ai_response) VALUES (?, ?)", (user_prompt, ai_response))
        conn.commit()
        
        return user_prompt, ai_response

    # ...

    # Display previous conversation history from the database
    st.subheader("Conversation History:")
    for row in cursor.execute("SELECT * FROM conversation"):
        st.text(row[0])
        st.text(row[1])

# ...
