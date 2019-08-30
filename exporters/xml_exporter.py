import lxml
from exporters.generic_exporter import GenericExporter


class XmlExporter(GenericExporter):
    def _export_to_output_file(self, tickets, milestones):
        i = 1
        res = []
        for item in tickets:
            item_milestones = list(map(lambda x: x.format(item.fields.summary, i), milestones))

            with open(self.output_file, "at", encoding="cp1251") as out:
                out.writelines(item_milestones)
            res.append(item_milestones)
            i += 1
        return res
