import os
import subprocess
from icaro.core.element import Element

def test(controller, type, elementName):
    element = controller.virtualarea.get_element(type, elementName)
    element.test()

