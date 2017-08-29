import json
import sys
import os
from icaro.controller.main import Controller as controller
from icaro.core.utils as utils

class Interpreter():
    def __init__(self, controller, text):
        self.text = text
        self.controller = controller

    def _interpreter(self, *arg):
        sys.flags 

    def _converter_to_json(self):
        rows = text.split(";")
        for row in rows:
            commands = row.split(" ")
            _interpreter(commands)
