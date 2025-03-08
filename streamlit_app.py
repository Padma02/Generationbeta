import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Generation Beta Knowledge Bot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input
user_input = st.chat_input("Ask anything about Generation Beta...")

# Function to check if the query is relevant to Generation Beta
def is_relevant_query(query):
    relevant_keywords = ["Generation Beta", "Gen Beta", "future generation", "youth trends", "technology impact", "education trends", "Gen Beta lifestyle"]
    return any(keyword.lower() in query.lower() for keyword in relevant_keywords)

# Function to get a response from OpenAI with Generation Beta-related topics
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an AI assistant that strictly focuses on Generation Beta-related topics. "
                "You must only provide responses about Generation Beta, including their characteristics, trends, behaviors, "
                "impact on society, future predictions, and technology influences. "
                "If a user asks anything unrelated to Generation Beta, refuse to answer and guide them back to relevant topics."
            )}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    if is_relevant_query(user_input):
        # Append user's message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate assistant's response
        assistant_prompt = (
            f"User has asked: {user_input}. Provide a response strictly related to Generation Beta. "
            "If the question is unrelated, refuse and redirect to a relevant topic."
        )
        assistant_response = get_response(assistant_prompt)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
    else:
        with st.chat_message("assistant"):
            st.markdown("I'm sorry, but I can only discuss Generation Beta-related topics. Please ask something relevant!")
