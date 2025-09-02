# Save this code in a file named check_api_key.py

import google.generativeai as genai
import getpass
from google.api_core import exceptions


def verify_api_key():
    """
    Prompts the user for a Gemini API key and checks its validity by
    making a simple API call.
    """
    print("🔑 Please enter your Google Gemini API key to verify it.")
    print("   (Your input will be hidden for security)")

    # Securely get the API key from the user
    api_key = getpass.getpass("Enter your API key: ")

    if not api_key:
        print("\nNo API key entered. Exiting.")
        return

    try:
        # Configure the genai library with the provided key
        genai.configure(api_key=api_key)

        # Make a lightweight, free API call to list models to test the key
        genai.list_models()

        # If the above line doesn't raise an exception, the key is valid
        print("\n✅ Success! Your API key is valid and working correctly.")

    except exceptions.PermissionDenied:
        # This specific error is raised for invalid API keys
        print("\n❌ Failure! The API key you entered is not valid.")
        print("   Please generate a new key from Google AI Studio and try again.")
    except Exception as e:
        # Catch any other potential errors (e.g., network issues)
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    verify_api_key()
