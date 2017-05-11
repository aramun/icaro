import requests
import json
import icaro.core.utils as utils
import os
import glob

class LibsController:
    def __init__(self, virtualarea):
        self.virtualarea = virtualarea
        self.api_url = "https://api.github.com/search/repositories"
        self.formats = ["css", "js"]
        self.accepted_dirs = ["dist", "vendors"]

    def __search(self, repository, firstElement=False):
        resp = requests.get(self.api_url+"?q="+repository)
        resp = json.loads(resp.text)["items"]
        if firstElement:
            return resp[0]
        else:
            return resp

    def __check_staging(self):
        for accepted in self.accepted_dirs:
            if accepted in os.listdir(".staging"):
                return accepted
        return False

    def __distribute(self, dir):
        for format in self.formats:
            for file in glob.glob(".staging/"+dir+"/*."+format):
                if os.path.isfile(file):
                    utils.importer(file, "pages/libraries/"+format+"/"+os.path.basename(file))

    def install(self, repository):
        utils.mkDir(".staging")
        clone_url = self.__search(repository, firstElement=True)["clone_url"]
        print("Downloading...")
        os.system("git clone "+clone_url+" .staging")
        dir = self.__check_staging()
        if dir:
            self.__distribute(dir)
        else:
            utils.rmdir(".staging")
            return repository + " is not an integrable library"
        utils.rmdir(".staging")
        return repository + " install success!!"

    def search(self, repository): 
        resp = self.__search(repository)
        result = ""
        for item in resp:
            result += """
                        Name: %s
                        Full Name: %s
                        Repository URL: %s
                        Description: %s
                        -------------------------------------
                    """ % (item["name"], item["full_name"], item["html_url"], item["description"])
        return result
