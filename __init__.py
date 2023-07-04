bl_info = {
	"name": "Scripting Toolbox",
	"author": "twistedturtle",
	"version": (0, 1, 1),
	"blender": (3, 5, 1),
	"location": "Text Editor -> Sidebar",
	"description": "A few simple tools for easier scripting",
	"warning": "",
	"doc_url": "",
	"category": "Text Editor",
}


moduleNames = [ "strack", "ui" ]


#########################################################
# Don't edit below here
#########################################################

import sys
import importlib
import os

from pathlib import Path

moduleFullNames = {}
for currentModuleName in moduleNames:
    if 'DEBUG_MODE' in sys.argv:
        moduleFullNames[currentModuleName] = ('{}'.format(currentModuleName))
    else:
        moduleFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))


for currentModuleFullName in moduleFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'moduleNames', moduleFullNames)

def register():
    for currentModuleName in moduleFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()


def unregister():
    for currentModuleName in moduleFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()

if __name__ == "__main__":
    register()
