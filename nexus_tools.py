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
from math import fabs, sqrt
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
				pos.x += x * ob.offsetK[0]
			else:
				pos.x -= x * ob.offsetK[0]

			if pos.y > bpy.context.scene.cursor_location.y:
				pos.y += y * ob.offsetK[1]
			else:
				pos.y -= y * ob.offsetK[1]

			if pos.z > bpy.context.scene.cursor_location.z:
				pos.z += z * ob.offsetK[2]
			else:
				pos.z -= z * ob.offsetK[2]

def find_center():
	bpy.ops.object.select_all(action='DESELECT')
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			ob.select = True

	if bpy.context.scene.cur_to_center:
		bpy.ops.view3d.snap_cursor_to_selected()


	cur = bpy.context.scene.cursor_location
	cursorX = cur.x
	cursorY = cur.y
	cursorZ = cur.z
	# curLen = sqrt(cursorX*cursorX+cursorY*cursorY+cursorZ*cursorZ)

	for ob in bpy.data.objects:
		if ob.type == "MESH":
			ob.select = True
			ob.normal_location = ob.location
			# obLen = sqrt(ob.location.x*ob.location.x+ \
			# 						 ob.location.y*ob.location.y+ \
			# 						 ob.location.z*ob.location.z)
			



			if fabs(ob.location.x) > fabs(cursorX): #???
				ob.offsetK[0] = fabs(ob.location.x / cursorX)
			else:
				ob.offsetK[0] = fabs(cursorX / ob.location.x)

			if fabs(ob.location.y) > fabs(cursorY): #???
				ob.offsetK[1] = fabs(ob.location.y / cursorY)
			else:
				ob.offsetK[1] = fabs(cursorY / ob.location.y)

			if fabs(ob.location.z) > fabs(cursorZ): #???
				ob.offsetK[2] = fabs(ob.location.z / cursorZ)
			else:
				ob.offsetK[2] = fabs(cursorZ / ob.location.z)

			print(ob.name)
			print(ob.offsetK[0])
			print(ob.offsetK[1])
			print(ob.offsetK[2])


def return_pos():
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			ob.location.xyz = ob.normal_location



#class of explode data variable
# class ExplodeData(bpy.types.PropertyGroup):
# 	normal_location = bpy.props.FloatVectorProperty(
# 		name = "normal_location",
# 		default = (0.0, 0.0, 0.0),
# 		description = "normal location before explode"
# 	)

#class find center
class OBJECT_OT_find_center(bpy.types.Operator):
	"""Find center and remember normal location objects"""
	bl_label = "Find center and remember normal location objects"
	bl_idname = "object.find_center"
	bl_options = {'REGISTER', 'UNDO'}

	cur_to_center = bpy.types.Scene.cur_to_center = BoolProperty(
		name = "cur_to_center",
		default = True,
		description = "Translate 3d cursor to center objects"
	)

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

	offsetK = bpy.types.Object.offsetK = FloatVectorProperty(
		name = "offsetK",
		min = 1.0,
		default = (0.0, 0.0, 0.0),
		description = "coefficient offset object"
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
		
		col = box.column(align=True)
		col.operator("object.find_center", text="Find center")
		col.prop(scene, "cur_to_center", text="Cursor to center")

		box.prop(scene, "explode_distance", text="Explode distance")

		col = box.column(align=True)
		col.operator("object.explode", text="Explode objects")
		col.operator("object.return_pos", text="Return objects")

def register():
	bpy.utils.register_class(NexusToolsPanel)
	bpy.utils.register_class(OBJECT_OT_explode)
	bpy.utils.register_class(OBJECT_OT_find_center)
	bpy.utils.register_class(OBJECT_OT_return_pos)
	# bpy.utils.register_class(ExplodeData)

def unregister():
	bpy.utils.unregister_class(NexusToolsPanel)
	bpy.utils.unregister_class(OBJECT_OT_explode)
	bpy.utils.unregister_class(OBJECT_OT_find_center)
	bpy.utils.unregister_class(OBJECT_OT_return_pos)
	# bpy.utils.unregister_class(ExplodeData)

if __name__ == "__main__":
	register()
# bpy.types.Object.explode_data = bpy.props.PointerProperty(type=ExplodeData)