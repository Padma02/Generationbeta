import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Generation Beta & Post-2020 Kids Parenting Bot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input
user_input = st.chat_input("Ask anything about parenting kids born after 2020...")

# Function to check if the query is relevant to Generation Beta kids and parenting
def is_relevant_query(query):
    relevant_keywords = [
        "Generation Beta", "Gen Beta", "future generation", "youth trends", "technology impact", 
        "education trends", "Gen Beta lifestyle", "parenting Gen Beta", "raising Gen Beta kids", "child development Gen Beta", 
        "kids born after 2020", "post-2020 kids", "new generation parenting", "modern child development", 
        "childcare", "toddler behavior", "discipline techniques", "parenting tips", "educational tools", "screen time management"
    ]
    return any(keyword.lower() in query.lower() for keyword in relevant_keywords)

# Function to get related topics for parenting guidance
def get_related_topics():
    return [
        "Effective discipline strategies for post-2020 kids",
        "How technology is shaping Generation Beta’s learning habits",
        "Balancing screen time and outdoor activities",
        "Emotional intelligence development in young children",
        "Parenting techniques for digital-age children",
        "Best educational toys and tools for young learners"
    ]

# Function to get a response from OpenAI with parenting topics for Gen Beta and post-2020 kids
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an AI assistant that strictly focuses on parenting topics for Generation Beta and kids born after 2020. "
                "You must only provide responses about these children, including parenting strategies, education trends, psychological development, "
                "social behaviors, technology influence, and future challenges of raising kids in the digital age. "
                "If a user asks anything unrelated to parenting post-2020 children, refuse to answer and guide them back to relevant topics."
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
            f"User has asked: {user_input}. Provide a response strictly related to parenting kids born after 2020. "
            "If the question is unrelated, refuse and redirect to a relevant topic."
        )
        assistant_response = get_response(assistant_prompt)
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
            
        # Display related topics
        st.markdown("**Related Topics You Might Find Helpful:**")
        for topic in get_related_topics():
            st.markdown(f"- {topic}")
    else:
        with st.chat_message("assistant"):
            st.markdown("I'm sorry, but I can only discuss parenting topics for kids born after 2020. Please ask something relevant!")
