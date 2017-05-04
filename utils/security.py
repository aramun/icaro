def api(req, allow_addrs):
    if allow_addrs == None or req.remote_addr in allow_addrs:
            return True
    return False

def static(req, page, role, widget, allow_addrs):
    if allow_addrs == None or req.remote_addr in allow_addrs:
        for section in page:
            for section_role in section["roles"]:
                if section["widget"] == widget and section_role == role:
                    return True
    return False

def lib(req, allow_addrs):
    if allow_addrs == None or req.remote_addr in allow_addrs:
            return True
    return False

def page(req, allow_addrs):
    if allow_addrs == None or req.remote_addr in allow_addrs:
            return True
    return False
