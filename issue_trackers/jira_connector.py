from jira.client import JIRA
import urllib3


class JiraConnector:
    __slots__ = ['options', 'login', 'password']

    def __init__(self, options, login, password):
        self.options = options
        self.login = login
        self.password = password

    def get_items(self, jira_jql_statemet, fields):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        jira_con = JIRA(self.options, basic_auth=(self.login, self.password))
        items = jira_con.search_issues(jira_jql_statemet, fields=fields)
        jira_con.close()
        return items
