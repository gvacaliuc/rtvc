import os
import json
from dotenv import load_dotenv, set_key
from bcrypt import hashpw, gensalt
from getpass import getpass

# Load the .env file
ENV_FILE = ".env"
load_dotenv(ENV_FILE)


# Function to add a user to the AUTHN_DATABASE
def add_user_to_authn_database(username, plaintext_password):
    authn_database = os.getenv("AUTHN_DATABASE", "{}")  # Default to empty JSON

    # Parse the existing AUTHN_DATABASE
    try:
        user_db = json.loads(authn_database)
        if not isinstance(user_db, dict):
            raise ValueError("AUTHN_DATABASE must be a JSON object.")
    except json.JSONDecodeError:
        print("Error: AUTHN_DATABASE is not valid JSON.")
        return

    # Check if the username already exists
    if username in user_db:
        print(f"User '{username}' already exists in AUTHN_DATABASE.")
        return

    # Hash the password using bcrypt
    hashed_password = hashpw(plaintext_password.encode(), gensalt()).decode()

    # Add the new user
    user_db[username] = hashed_password

    # Convert the updated database back to JSON
    updated_database = json.dumps(user_db)

    # Update the .env file
    set_key(ENV_FILE, "AUTHN_DATABASE", updated_database)
    print(f"User '{username}' added successfully.")


# Example usage
if __name__ == "__main__":
    username = input("Enter username: ")
    plaintext_password = getpass("Enter password: ")
    add_user_to_authn_database(username, plaintext_password)
