import sys
import icaro.core.utils as utils

def __machines_validator(machines):
    for machine_name, machine in machines.iteritems():
        command = utils.ssh_execute(machine, "ls /")
        if not command["status"]:
            print "Invalid configuration for "+machine_name+". Details: "+",".join(command["message"])
            sys.exit()

def valid(settings):
    if settings["machines"]:
        __machines_validator(settings["machines"])
    print "Machines --> OK"
    return settings

