def api(req, nginx_addr):
	if req.remote_addr == nginx_addr:
		return True
	return False

def static(req, page, role, widget, nginx_addr):
	if req.remote_addr == nginx_addr:
			for section in page:
				for section_role in section["roles"]:
					if section["widget"] == widget and section_role == role:
						return True
	return False 

def lib(req, nginx_addr):
	if req.remote_addr == nginx_addr:
		return True
	return False

def page(req, nginx_addr):
	if req.remote_addr == nginx_addr:
		return True
	return False