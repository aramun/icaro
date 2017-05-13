import icaro.core.utils as utils
import json

class Lang:
    def __init__(self, lang):
        self.name = lang
        self.lang = json.loads(utils.readLines(utils.selfLocation()+"/langs_manager/lang-dict.json"))[lang]
        self.images = self.lang["docker_images"]
        self.lib_manager = self.lang["library_manager"]
        self.requirements_file = json.loads(utils.readLines(utils.selfLocation()+"/langs_manager/library_manager.json"))[self.lib_manager]["requirements_file"]

    def run_command(self, port, path, name):
        cmd = self.lang["run_command"]
        cmd.replace("{port}", port)
        cmd.replace("{path}", path)
        cmd.repalce("{name}", name)
        return cmd
