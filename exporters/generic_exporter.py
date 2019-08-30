class GenericExporter:
    __slots__ = ['milestones_file', 'output_file', 'out_encoding']

    def __init__(self, out_file, milestones, encoding):
        self.output_file = out_file
        self.milestones_file = milestones
        self.out_encoding = encoding

    def _export_to_output_file(self, tickets, milestones):
        """the actual method for exporting milestones"""
        pass

    def _read_milestones(self):
        with open(self.milestones_file, "r") as mls:
            milestones = mls.readlines()
        return milestones

    def export(self, tickets):
        if not tickets:
            print("No tickets to export please check the FILTER settings in config_local.py")
            exit(-1)
        return self._export_to_output_file(tickets, self._read_milestones())
