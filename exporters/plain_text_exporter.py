from exporters.generic_exporter import GenericExporter


class PlainTextExporter(GenericExporter):
    def _export_to_output_file(self, project_tasks):
        with open(self.output_file, "wt", encoding=self.out_encoding) as out:
            doc_len = out.writelines(project_tasks)
        return doc_len
