import os
import sys
from jira import JIRA, Issue
from dotenv import load_dotenv
from colorama import Fore, Style, init
from datetime import datetime

# Initialize colorama
init(autoreset=True)

load_dotenv()

def get_jira_connection():
    """Establishes a connection to Jira using credentials from .env."""
    server = os.getenv("JIRA_SERVER")
    user = os.getenv("JIRA_USER")
    api_token = os.getenv("JIRA_API_TOKEN")

    if not all([server, user, api_token]):
        print("Error: Missing Jira credentials in .env file.")
        print("Please ensure JIRA_SERVER, JIRA_USER, and JIRA_API_TOKEN are set.")
        sys.exit(1)

    try:
        jira = JIRA(server=server, basic_auth=(user, api_token))
        print(f"Successfully connected to Jira at {server} as {user}")
        return jira
    except Exception as e:
        print(f"Error connecting to Jira: {e}")
        sys.exit(1)

def display_issue_info(issue):
    """Displays relevant information about a Jira issue."""
    print("-" * 40)
    
    _last_update_string = ""
    if issue.fields.updated:
        updated_date = datetime.strptime(issue.fields.updated.split(".")[0], "%Y-%m-%dT%H:%M:%S")
        _last_update_string = f"last changed {updated_date.strftime('%B %d')}"

    issue_type_colored = f"{Fore.LIGHTBLUE_EX}{issue.fields.issuetype.name}{Style.RESET_ALL}"
    print(f"Issue Type: {issue_type_colored} {_last_update_string}")
    
    # Highlight the key and summary
    key_summary_colored = f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{issue.key} - {issue.fields.summary}{Style.RESET_ALL}"
    print(f"Key: {key_summary_colored}")

    # Check if parent is available before accessing its attributes
    if hasattr(issue.fields, 'parent') and issue.fields.parent:
        print(f"  Parent: {issue.fields.parent.key} - {issue.fields.parent.fields.summary}")
    else:
        print("  Parent: None")
    print(f"Assignee: {issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned'}")

    # Color the status based on its name
    status_name = issue.fields.status.name
    if status_name in ("Done", "QA Verified"):
        status_colored = f"{Fore.GREEN}{status_name}{Style.RESET_ALL}"
    elif status_name == "Cancelled":
        status_colored = f"{Fore.RED}{status_name}{Style.RESET_ALL}"
    else:
        status_colored = status_name
    print(f"Status: {status_colored}  {issue.fields.resolution.name if issue.fields.resolution else 'Unresolved'}")
    print(f"Story Points: {issue.fields.customfield_10008 if hasattr(issue.fields, 'customfield_10008') else 'Not Set'}")

    print(f"Labels: {', '.join(issue.fields.labels) if issue.fields.labels else 'None'}")
    print("-" * 40)

def set_work_category(jira, issue: Issue):
    """Prompts the user to set the Work Category field and updates the issue."""
    while True:
        try:
            choice = input(
                "Set Work Category (f)eature Engineering, (e)ngineering Excellence, (o)perational Excellence, (s)kip? (f/e/o/s): "
            ).lower()
            if choice == "f":
                work_category = "Feature Engineering (FE)"
                break
            elif choice == "e":
                work_category = "Engineering Excellence (EE)"
                break
            elif choice == "o":
                work_category = "Operational Excellence (OE)"
                break
            elif choice == "s":
                print("Skipping issue.")
                return
            else:
                print("Invalid choice. Please enter f, e, o, or s.")
        except KeyboardInterrupt:
            print("\nExiting program.")
            sys.exit(0)

    try:
        issue.update(fields={"customfield_12088": {"value": work_category}})

        print(f"Work Category set to '{work_category}' for issue {issue.key}")
    except Exception as e:
        print(f"Error updating issue {issue.key}: {e}")
        

def main():
    """Main function to run the Jira issue update process."""
    jira = get_jira_connection()

    jql_query = os.getenv("JIRA_JQL_QUERY")

    if not jql_query:
        print("Error: JIRA_JQL_QUERY is not set")
        sys.exit(1)
    
    try:
        issues = jira.search_issues(jql_query, maxResults=100)
    except Exception as e:
        print(f"Error searching for issues: {e}")
        sys.exit(1)

    total_issues = len(issues)
    print(f"Found {total_issues} issues matching the query.")

    for i, issue in enumerate(issues):
        print(f"\nProcessing issue {i+1} of {total_issues}...")
        display_issue_info(issue)
        set_work_category(jira, issue)

    print("\nAll issues processed. Exiting.")

if __name__ == "__main__":
    main()
