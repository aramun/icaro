import os
import icaro.core.utils as utils

def set_proxy(proxy_settings, virtualarea):
    apt = ""
    system = ""
    for protocol in proxy_settings:
        if proxy_settings[protocol]:
            apt += 'Acquire::' + protocol + '::proxy "' + protocol + '://' + proxy_settings[protocol] + '/";'
            system += "ENV " + protocol + "_proxy="+ protocol +"://" + proxy_settings[protocol] + "\r\n"
    utils.fileWrite(virtualarea + "/apt.conf", apt)
    return system



