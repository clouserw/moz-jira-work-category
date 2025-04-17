# Jira Work Category Updater

This script connects to a Jira instance, finds issues matching specific criteria, displays relevant information about each issue, and interactively prompts the user to set the 'Work Category' field.  This script uses fields specific to Mozilla's Jira instance, so, you'll have to change it if you want to use it elsewhere.

![image](https://github.com/user-attachments/assets/1b103200-7db2-4226-949c-e257f2a67ea5)


## Setup
1. **Get the code**
    ```bash
    git clone https://github.com/clouserw/moz-jira-work-category
    cd moz-jira-work-category
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt    
    ```

2.  **Configure**
    Create a file named `.env` in the same directory as `process.py` and add some variables:

    ```dotenv
    # .env file
    JIRA_SERVER=https://your-domain.atlassian.net
    JIRA_USER=your_email@example.com
    JIRA_API_TOKEN=your_jira_api_token_here

    # Make sure you quote this properly.  This is the query used for Accounts
    JIRA_JQL_QUERY='project = fxa AND "Work Category[Dropdown]" IS EMPTY AND (Component is empty or component not in ("Subscription Platform")) ORDER BY updatedDate DESC'
    ```
    
## Usage

```bash
python process.py
```

Enter `f`, `e`, `o`, or `s` and press Enter.
*   `f`: Sets category to "Feature Engineering (FE)"
*   `e`: Sets category to "Engineering Excellence (EE)"
*   `o`: Sets category to "Operational Excellence (OE)"
*   `s`: Skips the current issue without making changes.

You can exit the script at any time by pressing `Ctrl+C`.
