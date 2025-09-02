# app.py

import streamlit as st
from langchain_helper import get_sql_chain

# --- Page Configuration ---
st.set_page_config(page_title="T-Shirt SQL Query Assistant", page_icon="👕")

# --- Header ---
st.title("👕 T-Shirt Stock SQL Q&A")
st.write(
    "Ask questions about the t-shirt inventory in plain English, and the AI will "
    "generate the SQL query and provide the answer."
)


# --- Caching the LangChain Chain ---
# This is crucial for performance. It prevents the expensive re-initialization
# of the AI model and database connection on every user interaction.
@st.cache_resource
def load_chain():
    """Loads and caches the LangChain SQL chain to ensure it's created only once."""
    return get_sql_chain()


# Load the chain using the cached function
try:
    chain = load_chain()
except Exception as e:
    st.error("❌ Failed to initialize the application.")
    st.error(f"Error: {e}")
    st.stop()


# --- User Input ---
question = st.text_input(
    "**Ask your question here:**",
    placeholder="e.g., How many Nike t-shirts do we have in total?",
)

# --- Process and Display Output ---
if question:
    try:
        # Show a spinner while processing the query
        with st.spinner("🤖 Thinking..."):
            # The 'invoke' method runs the chain
            result = chain.invoke(question)

            # Display the final answer
            st.success("**Answer:**")
            st.write(result.get("result", "Could not process the answer."))

            # Display the generated SQL query in an expander for transparency
            with st.expander("Show Generated SQL Query"):
                # The generated SQL is often in the 'intermediate_steps'
                # This part might need adjustment based on the exact chain output structure
                try:
                    query = result["intermediate_steps"][0]["input"].split("\n\n")[1]
                    st.code(query, language="sql")
                except (KeyError, IndexError):
                    st.warning("Could not extract the SQL query from the result.")

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
        st.warning("Please try rephrasing your question or check the application logs.")
