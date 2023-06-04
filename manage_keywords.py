import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def display_keywords(keywords):
    print(" ")
    print("***********************")
    print("Current Keywords:")
    for i, keyword in enumerate(keywords, start=1):
        print(f"{i}. {keyword}")
    print("***********************")
    print(" ")

def add_keywords(keywords):
    while True:
        new_keywords = input("Enter new keywords (comma-separated) (Enter to skip): ")
        if new_keywords.lower() == "":
            break
        elif new_keywords.lower() == " ":
            break
        new_keywords_list = [keyword.strip() for keyword in new_keywords.split(",")]
        keywords.extend(new_keywords_list)
        print("Keywords added successfully.")

def remove_keywords(keywords):
    while True:
        display_keywords(keywords)
        choice = input("Select a keyword number to remove (Enter to skip): ")
        if choice.lower() == "":
            break
        try:
            index = int(choice) - 1
            if index >= 0 and index < len(keywords):
                removed_keyword = keywords.pop(index)
                print(f"Keyword '{removed_keyword}' removed successfully.")
            else:
                print("Invalid keyword number. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid keyword number or Enter to skip.")

def manage_keywords(keywords):
    while True:
        print(" ")
        print("###########################")
        print("Manage Keywords:")
        print("1. Display Current Keywords")
        print("2. Add Keywords")
        print("3. Remove Keywords")
        print("4. Done")
        print("###########################")
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

# Get KEYWORDS from environment variables
keywords = os.getenv("KEYWORDS", "").split(",")

# Manage Keywords
manage_keywords(keywords)