import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Cloudflare Global API Key and email from environment variables
CLOUDFLARE_GLOBAL_API_KEY = os.environ.get("CLOUDFLARE_GLOBAL_API_KEY")
if CLOUDFLARE_GLOBAL_API_KEY is None or CLOUDFLARE_GLOBAL_API_KEY.strip() == "":
    CLOUDFLARE_GLOBAL_API_KEY = input("Enter Cloudflare Global API Key: ")
    os.environ["CLOUDFLARE_GLOBAL_API_KEY"] = CLOUDFLARE_GLOBAL_API_KEY
    with open(".env", "a") as env_file:
        env_file.write("CLOUDFLARE_GLOBAL_API_KEY={}\n".format(CLOUDFLARE_GLOBAL_API_KEY))

CLOUDFLARE_EMAIL = os.environ.get("CLOUDFLARE_EMAIL")
if CLOUDFLARE_EMAIL is None or CLOUDFLARE_EMAIL.strip() == "":
    CLOUDFLARE_EMAIL = input("Enter Cloudflare Email: ")
    os.environ["CLOUDFLARE_EMAIL"] = CLOUDFLARE_EMAIL
    with open(".env", "a") as env_file:
        env_file.write("CLOUDFLARE_EMAIL={}\n".format(CLOUDFLARE_EMAIL))

# Specify the keywords to match in the API tokens
KEYWORDS = os.environ.get("KEYWORDS")
if KEYWORDS is None or KEYWORDS.strip() == "":
    KEYWORDS = input("Enter keywords (comma-separated): ")
    keywords = [keyword.strip() for keyword in KEYWORDS.split(",")]
    os.environ["KEYWORDS"] = ",".join(keywords)
    with open(".env", "a") as env_file:
        env_file.write("KEYWORDS={}\n".format(",".join(keywords)))
else:
    keywords = KEYWORDS.split(",")

def display_keywords(keywords):
    print(" ")
    print("Current Keywords:")
    for i, keyword in enumerate(keywords, start=1):
        print(f"{i}. {keyword}")
    print()
    print(" ")

def add_keywords(keywords):
    new_keywords = input("Enter new keywords (comma-separated): ")
    new_keywords_list = [keyword.strip() for keyword in new_keywords.split(",")]
    keywords.extend(new_keywords_list)
    print("Keywords added successfully.")

def remove_keywords(keywords):
    while True:
        display_keywords(keywords)
        choice = input("Select a keyword number to remove (c to cancel): ")
        if choice.lower() == "c":
            break
        try:
            index = int(choice) - 1
            if index >= 0 and index < len(keywords):
                removed_keyword = keywords.pop(index)
                print(f"Keyword '{removed_keyword}' removed successfully.")
            else:
                print("Invalid keyword number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid keyword number or 'c' to cancel.")

def manage_keywords(keywords):
    while True:
        print(" ")
        print("Manage Keywords:")
        print("1. Display Current Keywords")
        print("2. Add Keywords")
        print("3. Remove Keywords")
        print("4. Done")
        print(" ")

        choice = input("Select an option: ")
        if choice == "1":
            display_keywords(keywords)
        elif choice == "2":
            add_keywords(keywords)
        elif choice == "3":
            remove_keywords(keywords)
        elif choice == "4":
            break
        else:
            print("Invalid input. Please select a valid option.")
            print(" ")

def remove_api_tokens(CLOUDFLARE_GLOBAL_API_KEY, CLOUDFLARE_EMAIL, keywords):
    headers = {
        'X-Auth-Key': CLOUDFLARE_GLOBAL_API_KEY,
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'Content-Type': 'application/json'
    }

    url = 'https://api.cloudflare.com/client/v4/user/tokens'

    # Fetch all API tokens
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        api_tokens = response.json()['result']
        token_count = len(api_tokens)
        if token_count == 0:
            print('No API tokens found.')
            return

        # Filter API tokens based on keywords
        filtered_tokens = []
        for token in api_tokens:
            for keyword in keywords:
                if keyword in token['name']:
                    filtered_tokens.append(token)

        # Remove API tokens
        if len(filtered_tokens) == 0:
            print('No API tokens matching the keywords found.')
        else:
            print(f'Removing {len(filtered_tokens)} API tokens...')
            for token in filtered_tokens:
                delete_url = f'https://api.cloudflare.com/client/v4/user/tokens/{token["id"]}'
                delete_response = requests.delete(delete_url, headers=headers)
                if delete_response.status_code == 200:
                    print(f'Successfully removed API token: {token["id"]}')
                else:
                    print(f'Failed to remove API token: {token["id"]}')

# Manage Keywords
manage_keywords(keywords)

# Remove API Tokens
remove_api_tokens(CLOUDFLARE_GLOBAL_API_KEY, CLOUDFLARE_EMAIL, keywords)
