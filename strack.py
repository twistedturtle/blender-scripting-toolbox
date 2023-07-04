import os
import re
import bpy
import sys
import traceback
import subprocess
from pathlib import Path
from itertools import islice

# Python module to redirect the sys.stdout
from contextlib import redirect_stdout
# So we can create a file-like object
import io
import builtins as __builtin__

interval = 1

warn = "\033[38;5;196m"
reset = "\033[0m"



def update_text(text, path):
	if str(path) == ".":
		return

	with open(path) as file:
		text.from_string(file.read())


def get_mtime(file):
	return file.stat().st_mtime


# Will this always work?
def get_active_editor():
	for a in bpy.data.screens["Scripting"].areas:
		if a.type == "TEXT_EDITOR":
			return a


def print_exception(name, e):
	print(f"{warn}Exception in {name}:{reset} {e}\n")
	print(traceback.format_exc())
	print("Still running")


def cls(banner=False):
	for a in bpy.context.screen.areas:
		if a.type == "CONSOLE":
			for region in a.regions:
				if region.type == 'WINDOW':
					with bpy.context.temp_override(area=a, region=region):
						bpy.ops.console.clear()
						if banner:
							bpy.ops.console.banner()


def get_obj(name):
	for o in bpy.data.objects:
		if o.name == name:
			return o
	return None


def clear(console=False, banner=True):
	for text in bpy.data.texts:
		if not text.strack.keep:
			if len(text.strack.objs) > 0:
				for i in reversed(range(len(text.strack.objs))):
					item = text.strack.objs[i]
					obj = get_obj(item.name)
					if obj:
						bpy.data.objects.remove(obj, do_unlink=True)
					text.strack.objs.remove(i)
	if console:
		cls(banner)


def console_print(*args, **kwargs):
	context = bpy.context
	for s in bpy.data.screens:
		if s.name == "Scripting":
			for a in s.areas:
				if a.type == 'CONSOLE':
					c = {}
					c['area'] = a
					c['space_data'] = a.spaces.active
					c['region'] = a.regions[-1]
					c['window'] = context.window
					c['screen'] = context.screen
					s = " ".join([str(arg) for arg in args])
					for line in s.split("\n"):
						bpy.ops.console.scrollback_append(c, text=line)


def track(at, obj=None):
	if obj == None:
		obj = bpy.context.active_object

	item = at.strack.objs.add()
	item.name = obj.name


def _run_script(at):
	try:
		at.as_module()
	except Exception as e:
		print_exception(at.name, e)


def run_script(at):
	sct = bpy.context.scene.strack
	st = bpy.context.scene.strack

	clear(console=st.clear, banner=st.banner)

	if at.strack.autotrack:
		objs = [ obj for obj in bpy.data.objects ]

	# our new output
	stdout = io.StringIO()
	with redirect_stdout(stdout):
		_run_script(at)

		if at.strack.autotrack:
			objs2 = [ obj for obj in bpy.data.objects ]
			new_objs = list(set(objs2).difference(objs))
			for o in new_objs:
				track(at, o)

	stdout.seek(0)
	output = stdout.read()
	del stdout

	if sct.p_out:
		console_print(output)
	if sct.c_out:
		__builtin__.print(output) # to system


def get_external_texts():
	texts = bpy.context.scene.strack.texts
	for t in bpy.data.texts:
		if t.name in texts:
			t.filepath = texts[t.name].filepath


# Python detection
##################

# import statements are usually among the first statements we come to
# if we only check for correct syntax
# there are several other languages that could match
# though they're unlikely to be found within blender
# If we check for blender module imports
# we can almost guarantee that we have a python script
# as other languages are unlikely to have the same modules

# stick with the simple method for now (less restrictions
# on the script), see how it goes
pattern = re.compile(f"import \w*|from \w* import \w*")
nlines = 30

def isPython(at):
	if at.filepath:
		if at.filepath.endswith(".py"):
			return True

		with open(at.filepath) as f:
			head = list(islice(f, nlines))

	else:
		head = []
		count = 0
		for line in at.lines:
			head.append(line.body)
			count += 1
			if count >= nlines:
				break

	for line in head:
		if pattern.match(line):
			return True
	return False


#########################################################

def poll_file():
	if not bpy.context.scene.strack.track:
		return interval

	if not (ed := get_active_editor()):
		return interval

	if not (at := ed.spaces.active.text):
		return interval

	file = Path(at.filepath)

	# Save filepath for when blender is re-opened
	if not at.name in bpy.context.scene.strack.texts and not str(file) in [ "//", "."]:
		entry = bpy.context.scene.strack.texts.add()
		entry.name = at.name
		entry.filepath = at.filepath


	if file.exists():
		if (mtime := get_mtime(file)) != float(at.strack.mtime):
			at.strack.mtime = str(mtime)
			update_text(at, file)
			ed.tag_redraw()
			if bpy.context.scene.strack.autorun:
				# Ignore non-python files
				if isPython(at):
					run_script(at)
	return interval


def toggle_poll(self, context):
	if bpy.context.scene.strack.track:
		if not bpy.app.timers.is_registered(poll_file):
			bpy.app.timers.register(poll_file, persistent=True)
	else:
		if bpy.app.timers.is_registered(poll_file):
			bpy.app.timers.unregister(poll_file)


class runScriptOperator(bpy.types.Operator):
	bl_idname = "text.strack_run_script"
	bl_label = "Run Script"
	bl_description = "Run script through strack"

	def execute(self, context):
		if not (ed := get_active_editor()):
			return {"CANCELLED"}

		at = ed.spaces.active.text
		# Ignore non-python files
		if isPython(at):
			run_script(at)

		return {'FINISHED'}




class strackColPG(bpy.types.PropertyGroup):
	name: bpy.props.StringProperty(name="name")


class strackCol2PG(bpy.types.PropertyGroup):
	name: bpy.props.StringProperty(name="name")
	filepath: bpy.props.StringProperty(name="filepath")

class strackTextPG(bpy.types.PropertyGroup):
	keep: bpy.props.BoolProperty(name="keep", default=False)
	objs: bpy.props.CollectionProperty(name="objs", type=strackColPG)
	mtime: bpy.props.StringProperty(name="mtime", default="-1.0")
	autotrack: bpy.props.BoolProperty(name="autotrack", default=True)


class strackScenePG(bpy.types.PropertyGroup):
	track: bpy.props.BoolProperty(name="track", default=True, update=toggle_poll)
	autorun: bpy.props.BoolProperty(name="autorun", default=True)
	texts: bpy.props.CollectionProperty(name="texts", type=strackCol2PG)

	c_out: bpy.props.BoolProperty(name="c_out", default=True)
	p_out: bpy.props.BoolProperty(name="p_out", default=True)
	clear: bpy.props.BoolProperty(name="clear", default=True)
	banner: bpy.props.BoolProperty(name="banner", default=True)




def register():
	bpy.utils.register_class(strackColPG)
	bpy.utils.register_class(strackCol2PG)
	bpy.utils.register_class(strackTextPG)
	bpy.utils.register_class(strackScenePG)
	bpy.utils.register_class(runScriptOperator)

	bpy.types.Text.strack = bpy.props.PointerProperty(type=strackTextPG)
	bpy.types.Scene.strack = bpy.props.PointerProperty(type=strackScenePG)

	bpy.app.timers.register(get_external_texts, first_interval=0.00001)
	bpy.app.timers.register(poll_file, persistent=True)


def unregister():
	if bpy.app.timers.is_registered(poll_file):
		bpy.app.timers.unregister(poll_file)

	if bpy.types.Scene.strack:
		del bpy.types.Scene.strack
	if bpy.types.Text.strack:
		del bpy.types.Text.strack

	bpy.utils.unregister_class(runScriptOperator)
	bpy.utils.unregister_class(strackScenePG)
	bpy.utils.unregister_class(strackTextPG)
	bpy.utils.unregister_class(strackCol2PG)
	bpy.utils.unregister_class(strackColPG)

