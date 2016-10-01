# bl_info
bl_info = {
	"name": "Nexus tools",
	"author": "nexus studio",
	"version": (0,0,1),
	"blender": (2,78),
	"location": "T > Nexus Tools",
	"description": "Explode meshes",
	"warning": "",
	"wiki_url": "None",
	"category": "Mesh"
}

import bpy
import mathutils
from bpy.props import *

def calc(self):
	x = bpy.context.object.explodeX
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			pos = ob.location
			if pos.x > bpy.context.scene.cursor_location.x:
				pos.x += x
			else:
				pos.x -= x
	# 	centerPoint += ob.location
	# for ob in bpy.data.objects:
	# 	ob.location.x += bpy.context.object.explodeX

	# centerPoint = centerPoint/len(bpy.data.objects)
	# bpy.ops.view3d.snap_cursor_to_selected()

def explode_center():
	bpy.ops.object.select_all(action='DESELECT')
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			ob.select = True
	
	bpy.ops.view3d.snap_cursor_to_selected()
	print(12)

	# centerPoint = mathutils.Vector((0,0,0))
	# i = 0;
	# for ob in bpy.data.objects:
	# 	if ob.type == "MESH":
	# 		centerPoint += ob.location
	# 		i += 1

	# centerPoint = centerPoint / i


#class find center
class OBJECT_OT_center(bpy.types.Operator):
	bl_label = "Find center point between all meshes"
	bl_idname = "object.explode_center"
	bl_options = {'REGISTER', 'UNDO'}

	centerPoint = bpy.types.Object.centerPoint = FloatVectorProperty(
		name = "centerPoint",
		default = (0.0, 0.0, 0.0),
		description = "center point between all meshes"
	)

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def invoke(self, context, event):
		explode_center()

		return {'FINISHED'}


#class init explode
class OBJECT_OT_InitExplode(bpy.types.Operator):
	bl_label = "Calculate explode meshes"
	bl_idname = "object.calc"
	bl_options = {'REGISTER', 'UNDO'}

	offsetX = bpy.types.Object.explodeX = FloatProperty(
		name = "X",
		min = 0,
		default = 0.0,
		description = "Explode meshes by X coordinate"
	)
	
	offsetY = bpy.types.Object.explodeY = FloatProperty(
		name = "Y",
		min = 0,
		default = 0.0,
		description = "Explode meshes by Y coordinate"
	)
	
	offsetZ = bpy.types.Object.explodeZ = FloatProperty(
		name = "Z",
		min = 0,
		default = 0.0,
		description = "Explode meshes by Z coordinate"
	)

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def invoke(self, context, event):
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
		obj = context.object

		box = layout.box()
		box.label(text="Explode objects")
		
		box.operator("object.explode_center", text="Find center")
		
		col = box.column(align=True)
		col.prop(obj, "explodeX")
		col.prop(obj, "explodeY")
		col.prop(obj, "explodeZ")

		box.operator("object.calc", text="Explode objects")


def register():
	bpy.utils.register_class(NexusToolsPanel)
	bpy.utils.register_class(OBJECT_OT_InitExplode)
	bpy.utils.register_class(OBJECT_OT_center)


def unregister():
	bpy.utils.unregister_class(NexusToolsPanel)
	bpy.utils.unregister_class(OBJECT_OT_InitExplode)
	bpy.utils.unregister_class(OBJECT_OT_center)

if __name__ == "__main__":
	register()
