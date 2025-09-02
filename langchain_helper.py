# langchain_helper.py

import os
from urllib.parse import quote_plus
import streamlit as st

# LangChain imports
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI

# --- CHANGE 1: Updated import for the new embeddings package ---
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import (
    SemanticSimilarityExampleSelector,
    FewShotPromptTemplate,
    PromptTemplate,
)
from langchain_experimental.sql import SQLDatabaseChain
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX

# Import few-shot examples
from few_shots import few_shots


class SQLChainGenerator:
    """A class to encapsulate the creation of a LangChain SQLDatabaseChain."""

    MYSQL_PROMPT = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
    Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use CURDATE() function to get the current date, if the question involves "today".

    Use the following format:

    Question: Question here
    SQLQuery: SQL Query to run
    SQLResult: Result of the SQLQuery
    Answer: Final answer here
    """

    # --- CHANGE 2: Fixed the typo in the template from {Result of the SQLQuery} to {SQLResult} ---
    EXAMPLE_PROMPT_TEMPLATE = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    LLM_MODEL_NAME = "gemini-2.5-flash"

    def __init__(self):
        """Initializes the generator by loading credentials."""
        # Use Streamlit secrets for deployment, fallback to hardcoded for local dev
        try:
            self.db_user = st.secrets["database"]["DB_USER"]
            self.db_password = st.secrets["database"]["DB_PASSWORD"]
            self.db_host = st.secrets["database"]["DB_HOST"]
            self.db_name = st.secrets["database"]["DB_NAME"]
            self.google_api_key = st.secrets["api"]["GOOGLE_API_KEY"]
        except:
            # Fallback to hardcoded values for local development
            self.db_user = "root"
            self.db_password = "Debaditya@2003"
            self.db_host = "localhost"
            self.db_name = "atliq_tshirts"
            self.google_api_key = "AIzaSyDk57eucDz0BxADE23ZXs7Oue6C2GWD8ZI"

    def _get_database_connection(self):
        """Creates and returns a SQLDatabase connection object."""
        # The password is now coming directly from the hardcoded value
        encoded_password = quote_plus(self.db_password)
        db_uri = f"mysql+pymysql://{self.db_user}:{encoded_password}@{self.db_host}/{self.db_name}"
        return SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=3)

    def _initialize_llm(self):
        """Initializes and returns the ChatGoogleGenerativeAI model."""
        return ChatGoogleGenerativeAI(
            google_api_key=self.google_api_key,
            temperature=0.2,
            model=self.LLM_MODEL_NAME,
        )

    def _create_few_shot_prompt(self):
        """Builds and returns a few-shot prompt template for SQL generation."""
        # Using the updated, non-deprecated class
        embeddings = HuggingFaceEmbeddings(model_name=self.EMBEDDING_MODEL_NAME)

        example_selector = SemanticSimilarityExampleSelector.from_examples(
            few_shots,
            embeddings,
            Chroma,
            k=2,
        )

        return FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=self.EXAMPLE_PROMPT_TEMPLATE,
            prefix=self.MYSQL_PROMPT,
            suffix=PROMPT_SUFFIX,
            input_variables=["input", "table_info", "top_k"],
        )

    def get_chain(self):
        """Builds and returns the fully configured SQLDatabaseChain."""
        db = self._get_database_connection()
        print("✅ 1. Database connection successful.")

        llm = self._initialize_llm()
        print("✅ 2. LLM initialized successfully.")

        prompt = self._create_few_shot_prompt()
        print("✅ 3. Few-shot prompt and embeddings ready.")

        chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=prompt)
        print(
            "✅ 4. SQLDatabaseChain created successfully. Ready to receive questions."
        )

        return chain


def get_sql_chain():
    """Initializes and returns a LangChain SQLDatabaseChain."""
    generator = SQLChainGenerator()
    return generator.get_chain()


def main():
    """A simple main function to test the SQLChainGenerator directly from this file."""
    print("\n--- Running a direct test of langchain_helper.py ---")
    try:
        sql_chain = get_sql_chain()
        question = "How many t-shirts are there in total?"
        print(f"\nAsking a test question: '{question}'")

        result = sql_chain.invoke(question)

        print("\n--- TEST COMPLETE ---")
        print("Final Answer:", result.get("result", "Could not process the answer."))

    except Exception as e:
        print(f"\n--- An error occurred during the test: {e} ---")
        print("Please check your API Key and database connection details.")


if __name__ == "__main__":
    main()
