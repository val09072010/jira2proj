"""Script for fast preparation of project plans (xml format) with pre-defined milestones,
mandatory tasks and check points from JIRA
Usage:
$ python ./jira2proj.py [-m <milestones file>] [-t 1] [-n <tasks file>] -o <output>
Output: xml file with tasks and resources
"""
import sys
import getopt
from lxml import etree as et
from jira.client import JIRA
import urllib3


ENCODING = "utf-8"
MILESTONES_FILES = "./assets/milestones.txt"
# JIRA_FIELDS is property to specify the fields which you need to populate the future ms proj plan
# please check your JIRA instance to use correct names for custom fields:
# e.g. field customfield_10705 corresponds to custom filed 'Sprint' added by Agile plugin
JIRA_FIELDS = "summary,fixVersions,assignee,customfield_10705"
NO_JIRA_PARAMS = False

try:
    import config_local
except ModuleNotFoundError:
    print("Please create ./config_local.py file with the following properties inside:")
    print("JIRA_SSL_CERT_PATH = <path to crt file with JIRA server ssl certificate>")
    print("JIRA_SERVER = JIRA server URL, e.g. https://jira.company.com")
    print("JIRA_LOGIN = JIRA account name")
    print("JIRA_PASS = JIRA account password")
    print("JIRA_FILTER = JIRA filter in JQL language that will be run to take tasks")
    NO_JIRA_PARAMS = True

TEMPLATE_PROJ_XML = 'assets/template.xml'
TASKS_TAG = '{http://schemas.microsoft.com/project}Tasks'
CALENDAR_TAG = '{http://schemas.microsoft.com/project}Calendars'
TASKS_TAG_NO_NAMESPACE = "Tasks"

PROJ_TAGS_MAP = {'Name': 'Template', 'Title': 'Template', 'Manager': 'PM',
                 'ScheduleFromStart': '1', 'StartDate': '2019-09-30T08:00:00',
                 'FinishDate': '2019-10-01T17:00:00', 'FYStartDate': '1',
                 'CriticalSlackLimit': '0', 'CurrencyDigits': '2', 'CurrencySymbol': '$',
                 'CurrencySymbolPosition': '0', 'CalendarUID': '1', 'DefaultStartTime': '11:00:00',
                 'DefaultFinishTime': '20:00:00', 'MinutesPerDay': '480', 'MinutesPerWeek': '2400',
                 'DaysPerMonth': '20', 'DefaultTaskType': '0', 'DefaultFixedCostAccrual': '2',
                 'DefaultStandardRate': '10', 'DefaultOvertimeRate': '15', 'DurationFormat': '7',
                 'WorkFormat': '2', 'EditableActualCosts': '0', 'HonorConstraints': '0',
                 'EarnedValueMethod': '0', 'InsertedProjectsLikeSummary': '0',
                 'MultipleCriticalPaths': '0', 'NewTasksEffortDriven': '0', 'NewTasksEstimated': '1',
                 'SplitsInProgressTasks': '0', 'SpreadActualCost': '0', 'SpreadPercentComplete': '0',
                 'TaskUpdatesResource': '1', 'FiscalYearStart': '0', 'WeekStartDay': '1',
                 'MoveCompletedEndsBack': '0', 'MoveRemainingStartsBack': '0',
                 'MoveRemainingStartsForward': '0', 'MoveCompletedEndsForward': '0',
                 'BaselineForEarnedValue': '0', 'AutoAddNewResourcesAndTasks': '1',
                 'CurrentDate': '2019-09-29T11:05:00', 'MicrosoftProjectServerURL': '1',
                 'Autolink': '1', 'NewTaskStartDate': '0', 'DefaultTaskEVMethod': '0',
                 'ProjectExternallyEdited': '0', 'ActualsInSync': '0', 'RemoveFileProperties': '0',
                 'AdminProject': '0'}

TASK_TAGS = {'Priority': '500', 'Start': '2019-10-02T08:00:00',
             'Finish': '2019-10-03T17:00:00', 'Duration': 'PT8H0M0S', 'DurationFormat': '7',
             'Work': 'PT08H0M0S', 'EffortDriven': '1', 'Estimated': '1', 'FixedCostAccrual': '2',
             'ConstraintType': '0', 'CalendarUID': '-1', 'ConstraintDate': '1970-01-01T00:00:00',
             'IgnoreResourceCalendar': '0'}

DEF_TASK_ID = 1
DEF_TASK_UID = 1


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


class GenericExporter:
    __slots__ = ['milestones_file', 'output_file', 'out_encoding']

    def __init__(self, out_file, milestones, encoding):
        self.output_file = out_file
        self.milestones_file = milestones
        self.out_encoding = encoding

    def _export_to_output_file(self, project_tasks):
        """the actual method for exporting milestones"""
        raise NotImplementedError("Please use concrete child class")

    def _read_milestones(self):
        with open(self.milestones_file, "r", encoding=ENCODING) as mls:
            milestones = mls.readlines()
        return milestones

    def export(self, tickets):
        if not tickets:
            print("No tickets to export please check the FILTER settings in config_local.py")
            exit(-1)

        milestones = self._read_milestones()
        i = 1
        project_tasks = []
        for tck in tickets:
            tck_milestones = list(map(lambda x, it=tck: x.format(it.strip(), i), milestones))
            project_tasks.extend(tck_milestones)
            i += 1
        return self._export_to_output_file(list(map(lambda x: x.strip(), project_tasks)))


class PlainTextExporter(GenericExporter):
    def _export_to_output_file(self, project_tasks):
        with open(self.output_file, "wt", encoding=self.out_encoding) as out:
            doc_len = out.writelines(project_tasks)
        return doc_len


class XmlExporter(GenericExporter):
    def _export_to_output_file(self, project_tasks):

        root = self.__generate_xml_template()
        tasks = root.find(TASKS_TAG)

        if tasks is None:
            tasks = et.SubElement(root, TASKS_TAG_NO_NAMESPACE)

        task_uid = DEF_TASK_UID
        task_id = DEF_TASK_ID

        for raw_task in project_tasks:
            task = et.SubElement(tasks, "Task")
            self.__insert_sub_element(task, "Name", raw_task)
            self.__insert_sub_element(task, "UID", str(task_uid))
            self.__insert_sub_element(task, "ID", str(task_id))
            for k in TASK_TAGS:
                self.__insert_sub_element(task, k, TASK_TAGS[k])
            task_id += 1
            task_uid += 1

        et.SubElement(root, "Resources")
        et.SubElement(root, "Assignments")

        with open(self.output_file, "w", encoding=self.out_encoding) as out:
            out_str = str(et.tostring(root, pretty_print=True, encoding=self.out_encoding), encoding=self.out_encoding)
            doc_len = out.write(out_str)

        return doc_len

    def __generate_xml_template(self):
        # Step 1: add <Project>
        root = et.Element("Project", xmlns="http://schemas.microsoft.com/project")
        # Step 2: add mandatory tags
        for k in PROJ_TAGS_MAP:
            self.__insert_sub_element(root, k, PROJ_TAGS_MAP[k])
        return root

    @staticmethod
    def __insert_sub_element(root, tag, value):
        sub_element = et.SubElement(root, tag)
        if value:
            sub_element.text = value
        return sub_element


def main(argv):
    resulting_file = ""
    milestones_file = MILESTONES_FILES
    to_plain_text = False
    with_jira = True
    tasks_from_text_file = ""

    try:
        opts, _ = getopt.getopt(argv, "o:m:t:n:", ["output=", "milestones=", "text=", "no-jira="])
        for opt, arg in opts:
            if opt in ("-o", "--output"):
                resulting_file = arg
            elif opt in ("-m", "--milestones"):
                milestones_file = arg
            elif opt in ("-t", "--text"):
                to_plain_text = True
            elif opt in ("-n", "--no-jira"):
                with_jira = False
                tasks_from_text_file = arg
            else:
                pass
    except getopt.GetoptError:
        print("Input params are wrong.\nUsage: $python ./jira2proj.py -o <output>")
        exit(1)

    if with_jira:
        if NO_JIRA_PARAMS:
            print("Script stopped: JIRA params are not specified in ./config_local.py.")
            print("Use -n option to build Project without JIRA or create ./config_local.py")
            exit(-1)
        # 1. connect to JIRA
        options = {'server': config_local.JIRA_SERVER, 'verify': False}
        jira_con = JiraConnector(options, config_local.JIRA_LOGIN, config_local.JIRA_PASS)
        # 2. get list of JIRA Stories, Epics, Features (i.e. subjects of delivery)
        items = jira_con.get_items(config_local.JIRA_FILTER, JIRA_FIELDS)
    else:
        if tasks_from_text_file:
            with open(tasks_from_text_file, "r", encoding=ENCODING) as tasks_file:
                items = tasks_file.readlines()
        else:
            items = []
    # 3. generate XML file
    # 4. get milestones list and apply it to each item from (2)
    if to_plain_text:
        exporter = PlainTextExporter(resulting_file, milestones_file, ENCODING)
    else:
        exporter = XmlExporter(resulting_file, milestones_file, ENCODING)
    # 5. populate (3) with <tasks>
    exporter.export(items)


if __name__ == "__main__":
    main(sys.argv[1:])
