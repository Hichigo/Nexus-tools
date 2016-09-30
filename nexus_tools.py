# bl_info
bl_info = {
	"name": "Nexus tools",
	"author": "nexus studio",
	"version": (0,0,1),
	"blender": (2,77),
	"location": "T > Nexus Tools",
	"description": "Explode meshes",
	"warning": "",
	"wiki_url": "",
	"categoy": "Mesh"
}

import bpy
import mathutils
from bpy.props import *

def calc(self):
	centerPoint = mathutils.Vector((0,0,0))
	for ob in bpy.data.objects:
		centerPoint += ob.location

	centerPoint = centerPoint/len(bpy.data.objects)
	bpy.ops.view3d.snap_cursor_to_selected()

#class init explode
class OBJECT_OT_InitExplode(bpy.types.Operator):
	bl_label = "Calculate explode meshes"
	bl_idname = "object.calc"
	bl_options = {'REGISTER', 'UNDO'}

	offsetX = bpy.types.Scene.explodeX = FloatProperty(
		name = "X",
		min = 0,
		default = 0.0,
		description = "Explode meshes by X coordinate"
	)
	
	offsetY = bpy.types.Scene.explodeY = FloatProperty(
		name = "Y",
		min = 0,
		default = 0.0,
		description = "Explode meshes by Y coordinate"
	)
	
	offsetZ = bpy.types.Scene.explodeZ = FloatProperty(
		name = "Z",
		min = 0,
		default = 0.0,
		description = "Explode meshes by Z coordinate"
	)

	@classmethod
	def poll(cls, context):
		return context.active_object is not None

	def execute(self, context):
		calc(self)

		return {'FINISHED'}


#class panel
class NexusToolsPanel(bpy.types.Panel):
	"""Creates a Panel in the view3d context of the tools panel (key "T")"""
	bl_label = "Nexus Tools"
	bl_idname = "nexustoolsid"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Nexus Tools"
	bl_context = "objectmode"
	
	def draw(self, context):
		layout = self.layout
		scene = context.scene

		box = layout.box()
		box.label(text="Explode objects")
		
		col = box.column(align=True)
		col.prop(scene, "explodeX")
		col.prop(scene, "explodeY")
		col.prop(scene, "explodeZ")

		col.operator("object.calc", text="run")


def register():
	bpy.utils.register_class(NexusToolsPanel)
	bpy.utils.register_class(OBJECT_OT_InitExplode)


def unregister():
	bpy.utils.unregister_class(NexusToolsPanel)
	bpy.utils.unregister_class(OBJECT_OT_InitExplode)

if __name__ == "__main__":
	register()
