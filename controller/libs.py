import requests
import json
import icaro.core.utils as utils
import os

class LibsController:
    def __init__(self, virtualarea):
        self.virtualarea = virtualarea
        self.api_url = "https://api.github.com/search/repositories"

    def __search(self, repository, firstElement=False):
        resp = requests.get(self.api_url+"?q="+repository)
        resp = json.loads(resp.text)["items"]
        if firstElement:
            return resp[0]
        else:
            return resp

    def install(self, repository):
        utils.mkDir(".staging")
        clone_url = self.__search(repository, firstElement=True)["clone_url"]
        print("Downloading...")
        os.system("git clone "+clone_url+" .staging")
        os.system("cp -a .staging/dist/. pages/libraries/")
        utils.rmdir(".staging")


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
