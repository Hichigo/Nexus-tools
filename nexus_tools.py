# bl_info
bl_info = {
	"name": "Nexus tools",
	"author": "Nexus Studio",
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


def explode():
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
			ob.normal_location = ob.location
			ob.offset = ob.location - cur
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


def return_pos():
	for ob in bpy.data.objects:
		if ob.type == "MESH":
			ob.location.xyz = ob.normal_location

def rename(addon_prefs):
	selected_objects = bpy.context.selected_objects
	for i in range( len( selected_objects ) ):
		selected_objects[i].name = "{}{}{}".format(addon_prefs.mesh_preffix, addon_prefs.mesh_name, addon_prefs.mesh_suffix)
		if ( bpy.context.scene.name_mat_set ):
			if ( bpy.context.scene.get_object_name ):
				name_mat = "{}{}{}".format(addon_prefs.mat_preffix, addon_prefs.mesh_name, addon_prefs.mesh_suffix)
				selected_objects[i].data.materials.append( bpy.data.materials.new( name_mat ) )
			else:
				name_mat = "{}{}{}".format(addon_prefs.mat_preffix, addon_prefs.mat_name, addon_prefs.mat_suffix)
				selected_objects[i].data.materials.append( bpy.data.materials.new( name_mat ) )

class ExampleAddonPreferences(bpy.types.AddonPreferences):
	# this must match the addon name, use '__package__'
	# when defining this in a submodule of a python package.
	bl_idname = __name__

	mesh_preffix = bpy.types.Scene.mesh_preffix = StringProperty(
		name="Mesh name preffix",
		default="SM_"
		# subtype='FILE_PATH',
	)
	mesh_name = bpy.types.Scene.mesh_name = StringProperty(
		name="Mesh name",
		default="NameObject"
	)
	mesh_suffix = bpy.types.Scene.mesh_suffix = StringProperty(
		name="Mesh name suffix",
		default="_HP"
	)

	mat_preffix = bpy.types.Scene.mat_preffix = StringProperty(
		name="Material name preffix",
		default="M_"
	)
	mat_name = bpy.types.Scene.mat_name = StringProperty(
		name="Material name",
		default="NameMaterial"
	)
	mat_suffix = bpy.types.Scene.mat_suffix = StringProperty(
		name="Material name suffix",
		default="_LOW"
	)




	def draw(self, context):
		layout = self.layout

		col = layout.column(align=True)
		col.prop(self, "mesh_preffix")
		col.prop(self, "mesh_name")
		col.prop(self, "mesh_suffix")

		col = layout.column(align=True)
		col.prop(self, "mat_preffix")
		col.prop(self, "mat_name")
		col.prop(self, "mat_suffix")


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
	offset = bpy.types.Object.offset = FloatVectorProperty(
		name = "offset",
		default = (0.0, 0.0, 0.0),
		subtype = "XYZ",
		description = "Vector direction from cursor pointer to object"
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
		# update = return_pos
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
		subtype = "XYZ",
		description = "distance from center of objects"
	)

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def invoke(self, context, event):
		explode()
		return {'FINISHED'}

#class init rename
class OBJECT_OT_rename(bpy.types.Operator):
	"""Fast rename meshes"""
	bl_label = "Fast rename meshes"
	bl_idname = "object.rename"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def invoke(self, context, event):
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		rename(addon_prefs)
		return {'FINISHED'}

#class panel
class ExplodeObjectsPanel(bpy.types.Panel):
	"""Creates a Panel in the view3d context of the tools panel (key "T")"""
	bl_label = "Explode object"
	bl_idname = "explodeobjectsid"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Nexus Tools"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout
		obj = context.object
		scene = context.scene

		col = layout.column(align=True)
		col.operator("object.find_center", text="Find center")
		col.prop(scene, "cur_to_center", text="Cursor to center")

		box = layout.box()
		box.prop(scene, "explode_distance", text="Explode distance")

		col = layout.column(align=True)
		col.operator("object.explode", text="Explode objects")
		col.operator("object.return_pos", text="Return objects")

		box = layout.box()
		box.prop(obj, "offset", text="Offset")

class FastRenamePanel(bpy.types.Panel):
	"""Creates a Panel in the view3d context of the tools panel (key "T")"""
	bl_label = "Fast rename"
	bl_idname = "fastrenameid"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Nexus Tools"
	bl_context = "objectmode"

	name_mat_set = bpy.types.Scene.name_mat_set = BoolProperty(
		name = "Add material",
		default = False,
		description = "create new material?"
	)

	get_object_name = bpy.types.Scene.get_object_name = BoolProperty(
		name = "Get object name",
		default = False,
		description = "Get object name?"
	)

	def draw(self, context):
		layout = self.layout
		obj = context.object
		scene = context.scene
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		col = layout.column(align=True)
		col.operator("object.rename", text="Rename")

		box = layout.box()
		col = box.column(align=True)
		col.label("Mesh")
		col.prop(addon_prefs, "mesh_preffix", text="Preffix")
		col.prop(addon_prefs, "mesh_name", text="Name")
		col.prop(addon_prefs, "mesh_suffix", text="Suffix")

		col = layout.column(align=True)
		col.prop(scene, "name_mat_set", text="Add material")
		col.prop(scene, "get_object_name", text="Get object name")

		box = layout.box()
		col = box.column(align=True)
		col.label("Material")
		col.prop(scene, "mat_preffix", text="Preffix")
		col.prop(scene, "mat_name", text="Name")
		col.prop(scene, "mat_suffix", text="Suffix")
		col.enabled = bpy.context.scene.name_mat_set

def register():
	bpy.utils.register_class(FastRenamePanel)
	bpy.utils.register_class(ExplodeObjectsPanel)
	bpy.utils.register_class(OBJECT_OT_explode)
	bpy.utils.register_class(OBJECT_OT_find_center)
	bpy.utils.register_class(OBJECT_OT_rename)
	bpy.utils.register_class(OBJECT_OT_return_pos)
	bpy.utils.register_class(ExampleAddonPreferences)
	# bpy.utils.register_class(ExplodeData)

def unregister():
	bpy.utils.unregister_class(FastRenamePanel)
	bpy.utils.unregister_class(ExplodeObjectsPanel)
	bpy.utils.unregister_class(OBJECT_OT_explode)
	bpy.utils.unregister_class(OBJECT_OT_find_center)
	bpy.utils.unregister_class(OBJECT_OT_rename)
	bpy.utils.unregister_class(OBJECT_OT_return_pos)
	bpy.utils.unregister_class(ExampleAddonPreferences)
	# bpy.utils.unregister_class(ExplodeData)

if __name__ == "__main__":
	register()
# bpy.types.Object.explode_data = bpy.props.PointerProperty(type=ExplodeData)
