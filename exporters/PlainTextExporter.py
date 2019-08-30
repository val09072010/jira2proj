from .GenericExporter import GenericExporter


class PlainTextExporter(GenericExporter):
    def _export_to_output_file(self, tickets, milestones):
        i = 1
        res = []
        for item in tickets:
            # TODO 1: make field configurable i.e. item.key or item.fields.summary etc.
            item_milestones = list(map(lambda x: x.format(item.fields.summary, i), milestones))
            # TODO 2: replace append with write
            with open(self.output_file, "at", encoding="cp1251") as out:
                out.writelines(item_milestones)
            res.append(item_milestones)
            i += 1
        return res
