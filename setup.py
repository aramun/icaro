import sys
import os

def prepend(file, prepend_text):
    with open(file, "r") as file_obj:
        text = file_obj.readlines()
    return [prepend_text+"\n"] + text

if __name__ == "__main__":
    with open("/usr/bin/icaro", "w") as file_obj:
        file_obj.writelines(prepend("icaro", "#!/usr/bin/env python"))
    os.system("chmod +x /usr/bin/icaro")
