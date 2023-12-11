#!/usr/bin/env python3

import os
import subprocess
from dotenv import load_dotenv

def execute_shell_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Command Output:\n{result.stdout.strip()}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{' '.join(command)}': {e}\nOutput:\n{e.output}")
        return None


python_executable = execute_shell_command(['which', 'python3'])
python_execute = "python3"

if not python_executable:
    print("Python 3 is not installed. Exiting...")
    exit(1)

def run_pip_install():
    print("\nRunning PIP install...\n")

    distro_commands = {
        'apt': ['apt-get', 'update', '-y', '&&', 'apt-get', 'install', 'python3-pip', '-y'],
        'dnf': ['dnf', 'install', 'python3', '-y'],
        'pacman': ['pacman', '-S', 'python-pip', '--noconfirm']
    }

    for cmd, install_cmd in distro_commands.items():
        if execute_shell_command(['command', '-v', cmd]):
            execute_shell_command(install_cmd.split())
            break
    else:
        print("Unsupported Linux distribution. Please install pip manually.")
        return

    execute_shell_command([python_execute, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def run_python_script(script_name):
    print(f"Running {script_name}...")
    output = execute_shell_command([python_execute, script_name])
    if output:
        print(output)

def validate_variables():
    print("\nValidating Environment Variables...\n")
    
    missing_variables = []
    load_dotenv(override=True)
    
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
    
    if missing_variables:
        print("Some environment variables are missing or have invalid values:")
        for var in missing_variables:
            print(f"- {var}")
        choice = input("Do you want to manage the variables? (yes/no): ")
        
        if choice.lower() == "yes":
            run_python_script('manage_variables.py')
            validate_variables()
        else:
            print("All Environment Variables must have a valid value to execute the Cleanup Process.")
            exit(1)
    else:
        print("All environment variables are valid.")

try:
    validate_variables()
    while True:    
        print("\nSelect an option:\n1. Run Cloudflare Bulk Deletion\n2. Run Cloudflare Delete API Tokens\n3. Run Cloudflare Tunnel Deletion\n4. Run Terraform Workspace Deletion and Creation\n5. Run Zerotier Network Deletion\n6. Install Python dependencies\n7. Manage Keywords\n8. Manage Environment Variables\n9. Validate Environment Variables\n10. Run All Scripts\n0. Exit\n")
        choice = input("Enter your choice: ")
        
        if choice == "0":
            break
        elif choice == "1":
            run_python_script('cloudflare_bulk_delete_dns.py')
        elif choice == "2":
            run_python_script('cloudflare_delete_api_tokens.py')
        elif choice == "3":
            run_python_script('cloudflare_delete_tunnel.py')
        elif choice == "4":
            run_python_script('terraform_workspace_delete_create.py')
        elif choice == "5":
            run_python_script('zerotier_delete_network.py')
        elif choice == "6":
            run_pip_install()
        elif choice == "7":
            run_python_script('manage_keywords.py')
        elif choice == "8":
            run_python_script('manage_variables.py')
        elif choice == "9":
            validate_variables()
        elif choice == "10":
            run_pip_install()
            run_python_script('cloudflare_bulk_delete_dns.py')
            run_python_script('cloudflare_delete_api_tokens.py')
            run_python_script('cloudflare_delete_tunnel.py')
            run_python_script('terraform_workspace_delete_create.py')
            run_python_script('zerotier_delete_network.py')
        else:
            print("Invalid choice")
except KeyboardInterrupt:
    print("\nExiting...")
