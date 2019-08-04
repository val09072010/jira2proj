"""Script for fast preparation of project plans (xml format) with pre-defined milestones, mandatory tasks and
check points from JIRA
Usage: $ python ./jira2proj.py [-f <config file>] [-m <path to file with milestones>] -o <output_xml>
Output: xml file with tasks and resources
"""
import sys
import getopt
import config
from jira.client import JIRA
import urllib3

def main(argv):
    resulting_xml_file = ""
    milestones_file = config.MILESTONES_FILES

    try:
        opts, args = getopt.getopt(argv, "o:m:f:", ["output=", "ms=" "config="])
        for opt, arg in opts:
            if opt in ("-o", "--output"):
                resulting_xml_file = arg
            elif opt in ("-f", "--config"):
                read_new_config(arg)
            elif opt in ("-m", "--ms"):
                milestones_file = arg
            else:
                pass
    except getopt.GetoptError:
        print("Input params are wrong.\nUsage: $ python ./jira2proj.py [-f <config file>] -o <output_xml>")
        exit(1)

    # 1. connect to JIRA
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    options = {'server': config.JIRA_SERVER, 'verify': False}
    jira_con = JIRA(options, basic_auth=(config.JIRA_LOGIN, config.JIRA_PASS))
    # 2. get list of JIRA Stories, Epics, Features (i.e. subjects of delivery)
    # TODO 3: make field set configurable
    items = jira_con.search_issues(config.JIRA_FILTER, fields="summary,fixVersions,assignee,customfield_10705")
    jira_con.close()
    # 3. generate XML file
    # 4. get milestones list and apply it to each item from (2)
    with open(milestones_file, "r") as mls:
        milestones = mls.readlines()

    # TODO 1: add JIRA res verification
    i = 1
    for item in items:
        # TODO 2: make field configurable i.e. item.key or item.fields.summary etc.
        print(list(map(lambda x: x.format(item.fields.summary, i), milestones)))
        i += 1
    # 5. populate (3) with <tasks>

def read_new_config(new_config):
    pass


if __name__ == "__main__":
    main(sys.argv[1:])
