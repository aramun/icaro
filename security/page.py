def static(req, page, role, widget):
	if req.remote_addr == "127.0.0.1":
			for section in page:
				for section_role in section["roles"]:
					if section["widget"] == widget and section_role == role:
						return True
	return False 

def lib(req):
	if req.remote_addr == "127.0.0.1":
		return True
	return False

def page(req):
	if req.remote_addr == "127.0.0.1":
		return True
	return False