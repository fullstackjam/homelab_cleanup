import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

# Function to prompt the user for input and update the variable value
def prompt_user(variable, prompt):
    value = os.environ.get(variable)
    if value is None or value.strip() == "":
        value = input(prompt)
    else:
        print(f"Current value for {variable}: {value}")
        choice = input(f"Enter a new value for {variable} (or press Enter to keep the current value): ")
        if choice.strip() != "":
            value = choice.strip()

    os.environ[variable] = value
    update_env_file(variable, value)

    return value

# Function to update the .env file with the new variable value
def update_env_file(variable, value):
    with open(".env", "r") as env_file:
        lines = env_file.readlines()
    with open(".env", "w") as env_file:
        for line in lines:
            if not line.startswith(f"{variable}="):
                env_file.write(line)
        if value.strip() != "":
            env_file.write("{}={}\n".format(variable, value))

# Variables and prompts
variables = {
    "CLOUDFLARE_GLOBAL_API_KEY": "Enter Cloudflare Global API Key: ",
    "CLOUDFLARE_EMAIL": "Enter Cloudflare Email: ",
    "CLOUDFLARE_ACCOUNT_ID": "Enter Cloudflare Account ID: ",
    "CLOUDFLARE_ZONE_ID": "Enter Cloudflare Zone ID: ",
    "ZEROTIER_API_TOKEN": "Enter ZeroTier API Token: ",
    "TERRAFORM_IO_API_TOKEN": "Enter Terraform IO API Token: ",
    "TERRAFORM_OAUTH_TOKEN_ID": "Enter Terraform OAuth Token ID: ",
    "VCS_IDENTIFIER": "Enter VCS Identifier: ",
    "REPO_TOKEN": "Enter Repo Token: ",
    "ORGANIZATION": "Enter Organization: ",
    "KEYWORDS": "Enter keywords (comma-separated): ",
}

# Check if any variable has a value
has_values = any(os.environ.get(variable) is not None and os.environ.get(variable).strip() != "" for variable in variables.keys())

# If at least one variable has a value, display all variables and values, and prompt for editing
if has_values:
    while True:
        print("")
        print("<><><><><><><><><><><><><><><><><><><><>")
        print("Variables and Values:")
        for variable, prompt in variables.items():
            value = os.environ.get(variable)
            if value is None or value.strip() == "" or value.strip() == "<<NULL>>":
                value = "<<NULL>>"
                print(f"\033[91m- {variable}: <<NULL>>\033[0m")
            else:
                print(f"- {variable}: {value}")
        print("<><><><><><><><><><><><><><><><><><><><>")
        print(" ")

        print("Variables:")
        for i, variable in enumerate(variables.keys(), start=1):
            print(f"{i}. {variable}")
        print(" ")

        choice = input("Enter the number of the variable you want to edit (or press Enter to skip): ")
        if choice.strip() == "":
            break
        try:
            index = int(choice)
            if 1 <= index <= len(variables):
                variable = list(variables.keys())[index - 1]
                prompt = variables[variable]
                prompt_user(variable, prompt)
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid choice!")

# If no variables have values, ask for values without prompting for options
else:
    for variable, prompt in variables.items():
        prompt_user(variable, prompt)

# Print the final values
print("")
print("<><><><><><><><><><><><><><><><><><><><>")
print("Final values:")
for variable, _ in variables.items():
    value = os.environ.get(variable)
    if value is None or value.strip() == "" or value.strip == "<<NULL>>":
        value = "<<NULL>>"
        print(f"\033[91m- {variable}: <<NULL>>\033[0m")
    else:
        print(f"- {variable}: {value}")
print("<><><><><><><><><><><><><><><><><><><><>")
print("")
