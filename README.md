# Scripting Toolbox

Provides a few simple tools for easier scripting within blender. The controls are located in the sidebar for the text editor. In addition to the below, it also stores the filepaths to any external scripts in the .blend file, so they're remembered when you re-open the file.

#### Console Ouput
System Console - Output to the terminal blender was started from.

Python Console - Output to the python console in the Scripting tab.

Clear Python Console - Clears the python console before running the script.

Keep Banner - Keeps the python banner when the python console is cleared.

#### Track External Scripts
Track - Keep track of external file's modification time and update the text editor. Single option for all scripts, but only applies to the active script.

Autorun - When the script is updated also run the script. Will work even if you're not in the scripting tab.

#### Track Script Objects
Autotrack - Automatically track objects created by the script. Next time the script is run, the objects will be deleted first.

Keep - Keep the objects from the last run of this script. This is per script.


#### Run Script
When running the script manually, you need to use the custom Run Script operator or the features won't work.


### Install

Download the .zip file from the `Code` button above. Use the Install button in Blender's addon preferences.

Arch based distros -  An AUR PKGBUILD may be forthcoming.


### Questions/Bugs/Issues/Feature requests etc
If you have any questions or feedback etc please open an issue.
