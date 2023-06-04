#!/usr/bin/env python3

import os
import subprocess
from dotenv import load_dotenv


# Find the Python interpreter
python_executable = subprocess.run(['which', 'python3'], capture_output=True, text=True).stdout.strip()

if not python_executable:
    print("Python 3 is not installed. Exiting...")
    exit(1)


# Function to run pip install command
def run_pip_install():
    print(" ")
    print("Running PIP install...")
    print(" ")
    
    # Check the Linux distribution
    if os.system('command -v apt &> /dev/null') == 0:
        # Ubuntu, Debian, Linux Mint
        os.system('apt update -y')
        os.system('apt install python3-pip')
    elif os.system('command -v dnf &> /dev/null') == 0:
        # CentOS 8 (and newer), Fedora, Red Hat
        os.system('dnf install python3')
    elif os.system('command -v pacman &> /dev/null') == 0:
        # Arch Linux and Manjaro
        os.system('pacman -S python-pip')
    else:
        print("Unsupported Linux distribution. Please install pip manually.")
        exit(1)

    print(" ")
    print("Installing Dependencies via PIP Requirements file...")
    print(" ")

    os.system(f'{python_executable} -m pip install -r requirements.txt')

    print(" ")


# Function to run cloudflare_bulk_delete_dns.py
def run_cloudflare_bulk_delete_dns():
    print("Running Cloudflare Bulk DNS Cleanup...")
    os.system(f'{python_executable} cloudflare_bulk_delete_dns.py')


# Function to run cloudflare_delete_api_tokens.py
def run_cloudflare_delete_api_tokens():
    print("Running Cloudflare Delete API Tokens...")
    os.system(f'{python_executable} cloudflare_delete_api_tokens.py')


# Function to run cloudflare_delete_tunnel.py
def run_cloudflare_delete_tunnel():
    print("Running Cloudflare Tunnel Deletion...")
    os.system(f'{python_executable} cloudflare_delete_tunnel.py')


# Function to run terraform_workspace_delete_create.py
def run_terraform_workspace_delete_create():
    print("Running Terraform Workspace Deletion and Creation...")
    os.system(f'{python_executable} terraform_workspace_delete_create.py')


# Function to run zerotier_delete_network.py
def run_zerotier_delete_network():
    print("Running Zerotier Network Deletion...")
    os.system(f'{python_executable} zerotier_delete_network.py')

# Function to run manage_keywords.py
def run_manage_keywords():
    print("Managing Keywords...")
    os.system(f'{python_executable} manage_keywords.py')

# Function to run manage_variables.py
def run_manage_variables():
    print("Managing Environment Variables...")
    os.system(f'{python_executable} manage_variables.py')

# Function to run all scripts in the specified order
def run_all_scripts():
    run_pip_install()
    run_cloudflare_bulk_delete_dns()
    run_cloudflare_delete_api_tokens()
    run_cloudflare_delete_tunnel()
    run_terraform_workspace_delete_create()
    run_zerotier_delete_network()


# Function to validate environment variables
def validate_variables():
    print(" ")
    print("***********************************")
    print("Validating Environment Variables...")
    print("***********************************")
    
    missing_variables = []
    
    # Load variables from .env file
    load_dotenv(override=True)
    
    # Check if variables have valid values
    variables = [
        'CLOUDFLARE_GLOBAL_API_KEY',
        'CLOUDFLARE_EMAIL',
        'CLOUDFLARE_ACCOUNT_ID',
        'CLOUDFLARE_ZONE_ID',
        'ZEROTIER_API_TOKEN',
        'TERRAFORM_IO_API_TOKEN',
        'TERRAFORM_OAUTH_TOKEN_ID',
        'VCS_IDENTIFIER',
        'REPO_TOKEN',
        'ORGANIZATION',
        'KEYWORDS'
    ]
    
    for var in variables:
        if not os.getenv(var) or os.getenv(var) == "<<NULL>>":
            missing_variables.append(var)
    
    # Prompt to manage variables if any are missing or have invalid values
    if missing_variables:
        print("")
        print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
        print("Some environment variables are missing or have invalid values:")
        for var in missing_variables:
            print(f"- {var}")
        print("<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>")
        print("")
        choice = input("Do you want to manage the variables? (yes/no): ")
        
        if choice.lower() == "yes":
            manage_variables()
            validate_variables()
        else:
            print("")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("All Environment Variables must have a valid value to properly execute the Cleanup Process.")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("")
            print("Starting Over...")
            validate_variables()
    else:
        print("")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("All environment variables are present and have valid values.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("")



# Validate environment variables before displaying the main menu
validate_variables()

# Main menu
while True:    
    print(" ")
    print("<><><><><><><><><><><><><><><><><><><><><><><><>")
    print("Select an option:")
    print("1. Run Cloudflare Bulk Deletion")
    print("2. Run Cloudflare Delete API Tokens")
    print("3. Run Cloudflare Tunnel Deletion")
    print("4. Run Terraform Workspace Deletion and Creation")
    print("5. Run Zerotier Network Deletion")
    print("6. Install Python dependencies")
    print("7. Manage Keywords")
    print("8. Manage Environment Variables")
    print("9. Validate Environment Variables")
    print("10. Do all the things")
    print("0. Exit")
    print("<><><><><><><><><><><><><><><><><><><><><><><><>")
    print(" ")
    choice = input("Enter your choice: ")
    
    if choice == "0":
        exit()
    elif choice == "1":
        run_cloudflare_bulk_delete_dns()
    elif choice == "2":
        run_cloudflare_delete_api_tokens()
    elif choice == "3":
        run_cloudflare_delete_tunnel()
    elif choice == "4":
        run_terraform_workspace_delete_create()
    elif choice == "5":
        run_zerotier_delete_network()
    elif choice == "6":
        run_pip_install()
    elif choice == "7":
        run_manage_keywords()
    elif choice == "8":
        run_manage_variables()
    elif choice == "9":
        validate_variables()
    elif choice == "10":
        run_all_scripts()
    else:
        print("Invalid choice")
    
    print()
