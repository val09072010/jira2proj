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
        with open(self.milestones_file, "r") as mls:
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
            # TODO 1: make field configurable i.e. tck.key or tck.fields.summary etc.
            tck_milestones = list(map(lambda x, it=tck: x.format(it.fields.summary, i), milestones))
            # TODO 2: replace append with write
            project_tasks.extend(tck_milestones)
            i += 1
        return self._export_to_output_file(project_tasks)
