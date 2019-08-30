class GenericExporter:
    __slots__ = ['milestones_file', 'output_file']

    def __init__(self, out_file, milestones):
        self.output_file = out_file
        self.milestones_file = milestones

    def _export_to_output_file(self, tickets):
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
        return self._export_to_output_file(tickets)
