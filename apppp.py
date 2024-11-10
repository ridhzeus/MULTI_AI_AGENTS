import streamlit as st
from main import main  # Import your combined agent from main.py

# Initialize the combined agent
agent = main()

# Streamlit UI
st.title("Your Multi-Agent System")

# Input field for user query
user_input = st.text_input("Enter your query:")

# Button to trigger the agent
if st.button("Run"):
    # Run the agent with the user input
    try:
        response = agent.run(user_input)  # Ensure this matches your method in main.py
        st.write("Response:", response)
    except Exception as e:
        st.error(f"Error: {e}")