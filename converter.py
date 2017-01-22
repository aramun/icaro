from dicttoxml import dicttoxml
import json

def xml(my_dict):
	return dicttoxml(my_dict)

def json(my_dict):
	return json.dumps(my_dict)

def csv(my_dict):
	csv = "\n\r".join([k+','+",".join(v) for k,v in my_dict.items()]) 
	return csv