import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Parenting & Child Development Bot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input
user_input = st.chat_input("Ask anything about parenting and child development...")

# Function to get related topics for parenting guidance
def get_related_topics():
    return [
        "Effective discipline strategies for kids",
        "How technology is shaping children’s learning habits",
        "Balancing screen time and outdoor activities",
        "Emotional intelligence development in young children",
        "Parenting techniques for digital-age children",
        "Best educational toys and tools for young learners"
    ]

# Function to get a response from OpenAI with parenting topics
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an AI assistant that focuses on parenting topics, child development, education trends, psychological growth, "
                "social behaviors, technology influence, and best practices for raising children. Provide expert guidance and tips on these subjects."
            )}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_prompt = f"User has asked: {user_input}. Provide a response strictly related to parenting and child development."
    assistant_response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        
    # Display related topics
    st.markdown("**Related Topics You Might Find Helpful:**")
    for topic in get_related_topics():
        st.markdown(f"- {topic}")
