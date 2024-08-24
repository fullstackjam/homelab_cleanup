import os
import subprocess
import sys

def run_script(script_name):
    """Run a script using subprocess."""
    try:
        subprocess.run(['python3', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")

def full_setup():
    """Run all scripts in the specified order for full reset."""
    scripts = [
        'cloudflare_bulk_delete_dns.py',
        'cloudflare_delete_api_tokens.py',
        'cloudflare_delete_tunnel.py',
        'terraform_workspace_delete_create.py'
    ]
    for script in scripts:
        print(f"Running {script}...")
        run_script(script)
        print(f"Finished {script}.\n")

def main_menu():
    """Display the main menu and handle user input."""
    menu_options = {
        '1': ('Cloudflare Bulk Record Removal', 'cloudflare_bulk_delete_dns.py'),
        '2': ('Cloudflare API Removal', 'cloudflare_delete_api_tokens.py'),
        '3': ('Cloudflare Tunnel Removal', 'cloudflare_delete_tunnel.py'),
        '4': ('Terraform Workspace Rebuild', 'terraform_workspace_delete_create.py'),
        '5': ('Manage Variables', 'manage_variables.py'),
        '6': ('Manage Keywords', 'manage_keywords.py'),
        '7': ('Full Reset (Prerequisite: Validate Variables and Keywords)', full_setup),
        '8': ('Exit', sys.exit)
    }

    while True:
        print("Main Menu:")
        for key in sorted(menu_options.keys()):
            print(f"{key}. {menu_options[key][0]}")

        choice = input("Enter your choice: ").strip()

        if choice in menu_options:
            action = menu_options[choice]
            if callable(action[1]):
                action[1]()
            else:
                run_script(action[1])
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
