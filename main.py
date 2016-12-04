import os

import json
import settings

def runApis(rubyfile):
    os.system("ruby "+rubyfile+" "+settings.project_name)

def setApiOnEnv():
    i=0
    variable = settings.project_name+"_API"
    os.environ[variable]=""
    for api in settings.apis:
         os.environ[variable]+=api["name"]+";"
    print os.environ[variable]

setApiOnEnv()
runApis("run_apis.rb")
