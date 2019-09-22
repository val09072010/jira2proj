from lxml import etree as et
from exporters.generic_exporter import GenericExporter


TEMPLATE_PROJ_XML = 'assets/template.xml'
TASKS_TAG = 'Tasks'
TASK_STR = '''
<Task>
    <ID>{0}</ID>
    <UID>{1}</UID>
    <Name>{2}</Name>
    <OutlineNumber>1</OutlineNumber>
    <OutlineLevel>1</OutlineLevel>
    <Active>1</Active>
    <Manual>0</Manual>
    <IsNull>0</IsNull>
    <Start>2011-01-03T00:00:00</Start>
    <Finish>2011-06-05T00:00:00</Finish>
    <ConstraintType>4</ConstraintType>
    <ConstraintDate>2011-01-03T00:00:00</ConstraintDate>
    <FixedCostAccrual>3</FixedCostAccrual>
    <CalendarUID>-1</CalendarUID>
    <IgnoreResourceCalendar>1</IgnoreResourceCalendar>
</Task>
'''
DEF_TASK_ID = 1
DEF_TASK_UID = 1

class XmlExporter(GenericExporter):
    def _export_to_output_file(self, project_tasks):

        tree = et.parse(TEMPLATE_PROJ_XML)
        root = tree.getroot()
        tasks = root.find(TASKS_TAG)

        if not len(tasks):
            tasks = et.SubElement(root, TASKS_TAG)

        task_uid = DEF_TASK_UID
        task_id = DEF_TASK_ID

        for raw_task in project_tasks:
            tasks.append(et.XML(TASK_STR.format(task_id, task_uid, raw_task)))
            task_id += 1
            task_uid += 1

        with open(self.output_file, "w", encoding=self.out_encoding) as out:
            doc_len = out.write(str(et.tostring(root, pretty_print=True, encoding=self.out_encoding),encoding=self.out_encoding))

        return doc_len
