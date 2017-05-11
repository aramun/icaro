import jinja2
import icaro.utils.security as security
import os
import sys
import falcon
import magic
import icaro.core.utils as utils

reload(sys)
sys.setdefaultencoding("utf-8")

def build_head(template, libraries, page):
	template += '<html><head>'
	for library in libraries:
            if library.find("http://") != -1 or library.find("https://") != -1:
                template += '<link rel="stylesheet" href="' + library + '">'
            else:
                template += '<link rel="stylesheet" href="lib/css/' + library + '">'
	for section in page:
            template += '<link rel="stylesheet" href="static/' + section["widget"] + '/css/style.css">'
	template += '</head><body>'
	return template

def build_footer(template, libraries, page):
	for library in libraries:
            if library.find("http://") != -1 or library.find("https://") != -1:
		template += '<script src="' + library + '"></script>'
            else:
		template += '<script src="lib/js/' + library + '"></script>'
	for section in page:
		template += '<script src="static/' + section["widget"] + '/js/main.js"></script>'
	template += '</body></html>'
	return template

def load_template(role, page, libraries):
	template = ""
	body = ""
	template = build_head(template, libraries["css"], page)
	for section in page:
		for section_role in section["roles"]:
			if role == section_role:
				path = os.path.join('widgets', section["widget"] + "/index.html")
				with open(os.path.abspath(path), 'r') as fp:
					body += fp.read()
	template += body
	template = build_footer(template, libraries["js"], page)
	return jinja2.Template(template)


class Lib:
    def __init__(self, addrs):
        self.addrs = addrs

    def on_get(self, req, resp, type, file):
        if security.lib(req, self.addrs):
            file = "pages/libraries/" + type + "/" + file
            resp.status = falcon.HTTP_200
            mime = magic.Magic(mime=True)
            resp.content_type = mime.from_file(file)
            resp.body = utils.readLines(file)
        else:
           falcon.HTTP_403
           resp.body = "Access Denied"


class Media:
    def __init__(self, media_widget, user):
        self.media_folder = media_widget
        self.user = user

    def on_get(self, req, resp, media_name):
        file = "widgets/" + self.media_widget + "/" + self.user + "/" + media_name
        resp.status = falcon.HTTP_200
        mime = magic.Magic(mime=True)
        resp.content_type = mime.from_file(file)
        resp.body = utils.readLines(file)


class Upload:
    def __init__(self, upload_widget, user):
        self.media_folder = upload_widget
        self.user = user

    def on_post(self, req, resp, file_name):
        resp.status = falcon.HTTP_200
        file = "widgets/" + self.upload_widget + "/" + self.user + "/" + file_name
        try:
            utils.fileWrite(file_name, req.stream.read())
            resp.body = "OK"
        except Exception as e:
            resp.body = "There was an error: " + e.message 

class Static:
    def __init__(self, addrs, role, page):
        self.addrs = addrs
        self.role = role
        self.page = page

    def on_get(self, req, resp, widget, type, file):
        if security.static(req, self.page, self.role, widget, self.addrs):
            file = "widgets/" + widget + "/" + type + "/" +file
            resp.status = falcon.HTTP_200
            mime = magic.Magic(mime=True)
            resp.content_type = mime.from_file(file)
            resp.body = utils.readLines(file)
        else:
            falcon.HTTP_403
            resp.body = "Access Denied"

class Page:
    def __init__(self, addrs, role, page, libraries, data):
        self.addrs = addrs
        self.role = role
        self.page = page
        self.libraries = libraries
        self.data = data

    def on_get(self, req, resp):
        if security.page(req, self.addrs):
            template = load_template(self.role, self.page, self.libraries)
            resp.status = falcon.HTTP_200
            resp.content_type = 'text/html'
            resp.body = template.render(data = self.data)
        else:
            falcon.HTTP_403
            resp.body = "Access Denied"
