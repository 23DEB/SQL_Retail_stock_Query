# main.py

# Ensure langchain_helper.py is in the same directory or adjust the import path accordingly
from langchain_helper import get_sql_chain


def main():
    """
    Main function to run the interactive SQL query assistant.
    """
    # Initialize the LangChain SQL agent
    chain = get_sql_chain()

    print("👕 Welcome to the T-Shirt SQL Assistant! 👕")
    print("Ask questions about the t-shirt inventory in plain English.")
    print("Type 'exit' or 'quit' to end the session.")

    while True:
        try:
            question = input("\nYour question: ")

            if question.lower() in ["exit", "quit"]:
                print("\nGoodbye! 👋")
                break

            # The 'invoke' method is the standard way to run chainsHow many Adidas t-shirts do you have in total?
            result = chain.invoke(question)

            # The result is a dictionary, and the final answer is in the 'result' key
            print("\n✅ Answer:", result.get("result", "Could not process the answer."))

        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try rephrasing your question.")


if __name__ == "__main__":
    main()
