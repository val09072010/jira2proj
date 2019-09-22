"""Script for fast preparation of project plans (xml format) with pre-defined milestones,
mandatory tasks and check points from JIRA
Usage:
$ python ./jira2proj.py [-f <config file>] [-m <path to file with milestones>] -o <output_xml>
Output: xml file with tasks and resources
"""
import sys
import getopt
import config
from issue_trackers.jira_connector import JiraConnector
from exporters.xml_exporter import XmlExporter
from exporters.plain_text_exporter import PlainTextExporter


def main(argv):
    resulting_file = ""
    milestones_file = config.MILESTONES_FILES
    to_plain_text = False

    try:
        opts, _ = getopt.getopt(argv, "o:m:f:t:", ["output=", "ms=", "config=", "text="])
        for opt, arg in opts:
            if opt in ("-o", "--output"):
                resulting_file = arg
            elif opt in ("-f", "--config"):
                read_new_config(arg)
            elif opt in ("-m", "--ms"):
                milestones_file = arg
            elif opt in ("-t", "--text"):
                to_plain_text = True
            else:
                pass
    except getopt.GetoptError:
        print("Input params are wrong.\nUsage: $python ./jira2proj.py -o <output>")
        exit(1)

    # 1. connect to JIRA
    options = {'server': config.JIRA_SERVER, 'verify': False}
    jira_con = JiraConnector(options, config.JIRA_LOGIN, config.JIRA_PASS)
    # 2. get list of JIRA Stories, Epics, Features (i.e. subjects of delivery)
    items = jira_con.get_items(config.JIRA_FILTER, config.JIRA_FIELDS)
    # 3. generate XML file
    # 4. get milestones list and apply it to each item from (2)
    if to_plain_text:
        exporter = PlainTextExporter(resulting_file, milestones_file, config.ENCODING)
    else:
        exporter = XmlExporter(resulting_file, milestones_file, config.ENCODING)
    # 5. populate (3) with <tasks>
    exporter.export(items)


def read_new_config(new_config):
    raise NotImplementedError("Sorry, the feature is not yet implemented.")


if __name__ == "__main__":
    main(sys.argv[1:])
