import os
import subprocess
from icaro.core.virtualarea.element import Element

def test(controller, type, elementName):
    element = controller.virtualarea.get_element(type, elementName)
    element.test()

