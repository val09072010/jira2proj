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
        # TODO 1: make field configurable i.e. tck.key or tck.fields.summary etc.
        # TODO 2: IMPLICIT dependency! Decouple code and assets/milestones.txt
        return list(map(lambda s: s.fields.summary, items))
