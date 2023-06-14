bl_info = {
	"name": "Scripting Toolbox",
	"author": "twistedturtle",
	"version": (0, 1, 0),
	"blender": (3, 5, 1),
	"location": "Text Editor -> Sidebar",
	"description": "Tools for easier scripting",
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


    mods = [ "tracky" ]
    # p = Path("/home.dm/.config/blender/3.4/scripts/modules")
    # if p.exists():
    for m in sys.modules:
        if m == "tracky":
            print(m)
    for m in mods:
        # f = p / m
        # fmn = f"{__name__}.{m}"
        if m in sys.modules:
            importlib.reload(sys.modules[m])


def unregister():
    for currentModuleName in moduleFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()

if __name__ == "__main__":
    register()
