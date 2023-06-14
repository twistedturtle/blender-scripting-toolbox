
import bpy
import sys

addon_name = "strack"

# Get list of modules
d = {}
for m in sys.modules:
	if m.startswith(addon_name):
		d[m] = sys.modules[m]
		print(m)


def get_active_text():
	for a in bpy.data.screens["Scripting"].areas:
		if a.type == "TEXT_EDITOR":
			return a.spaces.active.text
			try:
				if not at.filepath == "":
					return a.spaces.active.text
			except:
				return None

class TEXTEDITOR_PT_strack(bpy.types.Panel):
	bl_category = "Text"
	bl_idname = "OBJECT_PT_strack"
	bl_label = "strack"
	bl_space_type = 'TEXT_EDITOR'
	bl_region_type = 'UI'
	bl_context = "text_edit"

	@classmethod
	def poll(cls, context):
		return True

	def draw(self, context):
		at = get_active_text()

		self.layout.label(text="Console Output")
		self.layout.prop(context.scene.strack, "c_out", text="System Console")
		self.layout.prop(context.scene.strack, "p_out", text="Python Console")

		row = self.layout.row()
		row.enabled = context.scene.strack.p_out
		row.prop(context.scene.strack, "clear", text="Clear Python Console")

		row = self.layout.row()
		row.enabled = context.scene.strack.clear if context.scene.strack.p_out else False
		row.prop(context.scene.strack, "banner", text="Keep Banner")


		self.layout.label(text="Track External Scripts")
		self.layout.prop(context.scene.strack, "track", text="Track (global)")

		row = self.layout.row()
		row.enabled = context.scene.strack.track
		row.prop(context.scene.strack, "autorun", text="Autorun (global)")


		if at:
			self.layout.label(text="Track Script Objects")
			self.layout.prop(at.strack, "autotrack", text="Autotrack")
			self.layout.prop(at.strack, "keep", text="Keep (per Text)")


		self.layout.operator(d[f"{addon_name}.strack2"].runScriptOperator.bl_idname,
				text="Run Script", icon='PLUGIN')




def register():
	bpy.utils.register_class(TEXTEDITOR_PT_strack)

def unregister():
	bpy.utils.unregister_class(TEXTEDITOR_PT_strack)

