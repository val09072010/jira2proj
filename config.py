"""
Config file for jira2proj.py script.
The file contains:
- path to milestones list
- JIRA connection details

Please create config_local.py in the same dir to put actual connection values
"""

from config_local import JIRA_SERVER as JSS
from config_local import JIRA_LOGIN as JLL
from config_local import JIRA_PASS as JPP
from config_local import JIRA_FILTER as JFF

MILESTONES_FILES = "./assets/milestones.txt"

JIRA_SERVER = JSS
JIRA_LOGIN = JLL
JIRA_PASS = JPP
JIRA_FILTER = JFF

# JIRA_FIELDS is property to specify the fields which you really need to populate the future ms proj plan
# please note that JIRA has custom fields named as customfield_10705 - please check your JIRA instance for correct name
# in example below the field customfield_10705 corresponds to 'Sprint' custom filed(Agile plugin)
JIRA_FIELDS = "summary,fixVersions,assignee,customfield_10705"

JIRA_SSL_CERT_PATH = "./ssl/jira.crt"

ENCODING = "utf-8"
