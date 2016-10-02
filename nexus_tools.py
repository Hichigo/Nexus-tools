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


def explode(self):
	x = bpy.context.scene.explode_distance[0]
	y = bpy.context.scene.explode_distance[1]
	z = bpy.context.scene.explode_distance[2]
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			pos = ob.location

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

def find_center():
	bpy.ops.object.select_all(action='DESELECT')
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			ob.select = True
			ob.normal_location = ob.location
	
	bpy.ops.view3d.snap_cursor_to_selected()
	print(12)


def return_pos():
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			ob.location.xyz = ob.normal_location


#class find center
class OBJECT_OT_find_center(bpy.types.Operator):
	"""Find center and remember normal location objects"""
	bl_label = "Find center and remember normal location objects"
	bl_idname = "object.find_center"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def invoke(self, context, event):
		find_center()

		return {'FINISHED'}

#class return position objects
class OBJECT_OT_return_pos(bpy.types.Operator):
	"""Return object location to normal location"""
	bl_label = "Return object location to normal location"
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
class OBJECT_OT_explode(bpy.types.Operator):
	"""Calculate explode meshes"""
	bl_label = "Calculate explode meshes"
	bl_idname = "object.explode"
	bl_options = {'REGISTER', 'UNDO'}

	explode_distance = bpy.types.Scene.explode_distance = FloatVectorProperty(
		name = "explode_distance",
		min = 0.0,
		default = (0.0, 0.0, 0.0),
		description = "distance from center of objects"
	)

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def invoke(self, context, event):
		explode(self)
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
		scene = context.scene

		box = layout.box()
		box.label(text="Explode objects")
		
		box.operator("object.find_center", text="Find center")

		box.prop(scene, "explode_distance", text="Explode distance")

		col = box.column(align=True)
		col.operator("object.explode", text="Explode objects")
		col.operator("object.return_pos", text="Return objects")


def register():
	bpy.utils.register_class(NexusToolsPanel)
	bpy.utils.register_class(OBJECT_OT_explode)
	bpy.utils.register_class(OBJECT_OT_find_center)
	bpy.utils.register_class(OBJECT_OT_return_pos)


def unregister():
	bpy.utils.unregister_class(NexusToolsPanel)
	bpy.utils.unregister_class(OBJECT_OT_explode)
	bpy.utils.unregister_class(OBJECT_OT_find_center)
	bpy.utils.unregister_class(OBJECT_OT_return_pos)

if __name__ == "__main__":
	register()
