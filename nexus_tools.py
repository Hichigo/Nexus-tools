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
	y = bpy.context.object.explodeY
	z = bpy.context.object.explodeZ
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			pos = ob.location
			ob.normal_location = ob.location.xyz
			if pos.x > bpy.context.scene.cursor_location.x:
				pos.x += x
			else:
				pos.x -= x

			if pos.y > bpy.context.scene.cursor_location.y:
				pos.y += y
			else:
				pos.y -= y

			if pos.z > bpy.context.scene.cursor_location.z:
				pos.z += z
			else:
				pos.z -= z

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

def return_pos():
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			ob.location.xyz = ob.normal_location


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

#class return position objects
class OBJECT_OT_return_pos(bpy.types.Operator):
	bl_label = "Find center point between all meshes"
	bl_idname = "object.return_pos"
	bl_options = {'REGISTER', 'UNDO'}

	normal_location = bpy.types.Object.normal_location = FloatVectorProperty(
		name = "normal_location",
		default = (0.0, 0.0, 0.0),
		description = "normal location before explode"
	)

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def invoke(self, context, event):
		return_pos()

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

		col = box.column(align=True)
		col.operator("object.calc", text="Explode objects")
		col.operator("object.return_pos", text="Return objects")

		# box.prop(obj, "location", text="Transform")

def register():
	bpy.utils.register_class(NexusToolsPanel)
	bpy.utils.register_class(OBJECT_OT_InitExplode)
	bpy.utils.register_class(OBJECT_OT_center)
	bpy.utils.register_class(OBJECT_OT_return_pos)


def unregister():
	bpy.utils.unregister_class(NexusToolsPanel)
	bpy.utils.unregister_class(OBJECT_OT_InitExplode)
	bpy.utils.unregister_class(OBJECT_OT_center)
	bpy.utils.unregister_class(OBJECT_OT_return_pos)

if __name__ == "__main__":
	register()
