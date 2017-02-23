from dicttoxml import dicttoxml
import json


class Converter:
    def __init__(self, format, dict):
        self.dict = dict
        self.format = format
        func = getattr(self, self.format, func_not_found)
        func()

    def func_not_found(self):
        print "No Function " + self.format + " Found!"

    def xml(self):
        return dicttoxml(self.dict)

    def json(self):
	return json.dumps(self.dict)

    def csv(self):
	csv = "\n\r".join([k+','+",".join(v) for k,v in self.dict.items()]) 
	return csv
