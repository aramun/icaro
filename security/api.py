def api(req):
	if req.remote_addr == "127.0.0.1":
		return True
	return False