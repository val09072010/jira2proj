from lxml import etree as et
from exporters.generic_exporter import GenericExporter


TEMPLATE_PROJ_XML = 'assets/template.xml'
TASKS_TAG = '{http://schemas.microsoft.com/project}Tasks'
TASKS_TAG_NO_NAMESPACE = "Tasks"
TASK_STR = '''
        <Task>
            <UID>{1}</UID>
            <ID>{0}</ID>
            <Name>{2}</Name>
            <Priority>500</Priority>
            <Start>2019-10-02T08:00:00</Start>
            <Finish>2019-10-03T17:00:00</Finish>
            <Duration>PT8H0M0S</Duration>
            <DurationFormat>7</DurationFormat>
            <Work>PT08H0M0S</Work>
            <EffortDriven>1</EffortDriven>
            <Estimated>1</Estimated>
            <FixedCostAccrual>2</FixedCostAccrual>
            <ConstraintType>0</ConstraintType>
            <CalendarUID>-1</CalendarUID>
            <ConstraintDate>1970-01-01T00:00:00</ConstraintDate>
            <IgnoreResourceCalendar>0</IgnoreResourceCalendar>
        </Task>
'''

DEF_TASK_ID = 1
DEF_TASK_UID = 1


class XmlExporter(GenericExporter):
    def _export_to_output_file(self, project_tasks):

        parser = et.XMLParser(remove_blank_text=True)
        tree = et.parse(TEMPLATE_PROJ_XML, parser)
        root = tree.getroot()
        tasks = root.find(TASKS_TAG)

        if tasks is None:
            tasks = et.SubElement(root, TASKS_TAG_NO_NAMESPACE)

        task_uid = DEF_TASK_UID
        task_id = DEF_TASK_ID

        for raw_task in project_tasks:
            tasks.append(et.XML(TASK_STR.format(task_id, task_uid, raw_task)))
            task_id += 1
            task_uid += 1

        with open(self.output_file, "w", encoding=self.out_encoding) as out:
            out_str =  str(et.tostring(root, pretty_print=True, encoding=self.out_encoding), encoding=self.out_encoding)
            doc_len = out.write(out_str)

        return doc_len
