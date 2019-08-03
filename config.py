"""
Config file for jira2proj.py script.
The file contains:
- path to milestones list
- JIRA connection details

Please put actual values here
"""

MILESTONES_FILES = "./assets/milestones.txt"

JIRA_SERVER = "https://test.jiraserver.com"
JIRA_LOGIN = "user"
JIRA_PASS = "userpass"
JIRA_FILTER = "project = someproject AND issuetype = Feature AND status != Closed AND fixVersion is not EMPTY ORDER BY Rank"
JIRA_SSL_CERT_PATH = "./ssl/jira.crt"
