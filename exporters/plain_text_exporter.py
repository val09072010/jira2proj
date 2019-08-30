from exporters.generic_exporter import GenericExporter


class PlainTextExporter(GenericExporter):
    def _export_to_output_file(self, tickets, milestones):
        i = 1
        res = []
        for tck in tickets:
            # TODO 1: make field configurable i.e. tck.key or tck.fields.summary etc.
            tck_milestones = list(map(lambda x, it=tck: x.format(it.fields.summary, i), milestones))
            # TODO 2: replace append with write
            with open(self.output_file, "at", encoding=self.out_encoding) as out:
                out.writelines(tck_milestones)
            res.append(tck_milestones)
            i += 1
        return res
