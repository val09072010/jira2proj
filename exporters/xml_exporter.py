from lxml import etree as et
from exporters.generic_exporter import GenericExporter


TEMPLATE_PROJ_XML = 'assets/template.xml'
TASKS_TAG = '{http://schemas.microsoft.com/project}Tasks'
CALENDAR_TAG = '{http://schemas.microsoft.com/project}Calendars'
TASKS_TAG_NO_NAMESPACE = "Tasks"

PROJ_TAGS_MAP = {'Name': 'Template', 'Title': 'Template', 'Manager': 'PM', 'ScheduleFromStart': '1',
                 'StartDate': '2019-09-30T08:00:00', 'FinishDate': '2019-10-01T17:00:00', 'FYStartDate': '1',
                 'CriticalSlackLimit': '0', 'CurrencyDigits': '2', 'CurrencySymbol': '$', 'CurrencySymbolPosition': '0',
                 'CalendarUID': '1', 'DefaultStartTime': '11:00:00', 'DefaultFinishTime': '20:00:00',
                 'MinutesPerDay': '480', 'MinutesPerWeek': '2400', 'DaysPerMonth': '20', 'DefaultTaskType': '0',
                 'DefaultFixedCostAccrual': '2', 'DefaultStandardRate': '10', 'DefaultOvertimeRate': '15',
                 'DurationFormat': '7', 'WorkFormat': '2', 'EditableActualCosts': '0', 'HonorConstraints': '0',
                 'EarnedValueMethod': '0', 'InsertedProjectsLikeSummary': '0', 'MultipleCriticalPaths': '0',
                 'NewTasksEffortDriven': '0', 'NewTasksEstimated': '1', 'SplitsInProgressTasks': '0',
                 'SpreadActualCost': '0', 'SpreadPercentComplete': '0', 'TaskUpdatesResource': '1',
                 'FiscalYearStart': '0', 'WeekStartDay': '1', 'MoveCompletedEndsBack': '0',
                 'MoveRemainingStartsBack': '0', 'MoveRemainingStartsForward': '0', 'MoveCompletedEndsForward': '0',
                 'BaselineForEarnedValue': '0', 'AutoAddNewResourcesAndTasks': '1',
                 'CurrentDate': '2019-09-29T11:05:00', 'MicrosoftProjectServerURL': '1', 'Autolink': '1',
                 'NewTaskStartDate': '0', 'DefaultTaskEVMethod': '0', 'ProjectExternallyEdited': '0',
                 'ActualsInSync': '0', 'RemoveFileProperties': '0', 'AdminProject': '0'}

TASK_TAGS = {'Priority': '500', 'Start': '2019-10-02T08:00:00',
             'Finish': '2019-10-03T17:00:00', 'Duration': 'PT8H0M0S', 'DurationFormat': '7', 'Work': 'PT08H0M0S',
             'EffortDriven': '1', 'Estimated': '1', 'FixedCostAccrual': '2', 'ConstraintType': '0', 'CalendarUID': '-1',
             'ConstraintDate': '1970-01-01T00:00:00', 'IgnoreResourceCalendar': '0'}

DEF_TASK_ID = 1
DEF_TASK_UID = 1


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
            out_str =  str(et.tostring(root, pretty_print=True, encoding=self.out_encoding), encoding=self.out_encoding)
            doc_len = out.write(out_str)

        return doc_len

    def __generate_xml_template(self):
        # Step 1: add <Project>
        root = et.Element("Project", xmlns="http://schemas.microsoft.com/project")
        # Step 2: add mandatory tags
        for k in PROJ_TAGS_MAP:
            self.__insert_sub_element(root, k, PROJ_TAGS_MAP[k])
        # Step 3: add Calendar
        print(str(et.tostring(root, encoding=self.out_encoding, pretty_print=True), encoding=self.out_encoding))

        return root

    @staticmethod
    def __insert_sub_element(root, tag, value):
        sub_element = et.SubElement(root, tag)
        if value:
            sub_element.text = value
        return sub_element
