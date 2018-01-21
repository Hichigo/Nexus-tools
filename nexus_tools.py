# bl_info
bl_info = {
	"name": "Nexus tools",
	"author": "Nexus Studio",
	"version": (0,1,2),
	"blender": (2,79),
	"location": "T > Nexus Tools",
	"description": "Tools",
	"warning": "",
	"wiki_url": "None",
	"category": "User"
}

import bpy
from math import fabs, sqrt
import mathutils
from bpy.props import *
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

def read_blend_data(context, filepath, use_some_setting):
	print("running read_blend_data...")
	# TODO
	with bpy.data.libraries.load(filepath) as (data_from, data_to):
		data_to.objects = data_from.objects

	for ob in data_to.objects:
		print(ob.name)

	# would normally load the data here
	# print(data)

	return {'FINISHED'}


def uv_create_to_selected():
	for ob in bpy.context.selected_objects:
		if ob.type == "MESH":
			bpy.context.scene.objects.active = ob
			#create and rename uv
			bpy.ops.mesh.uv_texture_add()
			bpy.context.scene.objects.active.data.uv_layers[0].name = 'UV_Main'
			bpy.ops.mesh.uv_texture_add()
			bpy.context.scene.objects.active.data.uv_layers[1].name = 'UV_Lightpack'

def rename_object_to_selected():
	for ob in bpy.context.selected_objects:
		ob.name = "SM_Mesh"

def rename(addon_prefs):
	rename_mesh(addon_prefs)
	rename_mat(addon_prefs)

def rename_mat(addon_prefs):
	selected_objects = bpy.context.selected_objects
	for i in range( len( selected_objects ) ):
		# selected_objects[i].name = "{}{}{}".format(addon_prefs.mesh_preffix, addon_prefs.mesh_name, addon_prefs.mesh_suffix)
		if bpy.context.scene.name_mat_set:
			number_of_materials = len( selected_objects[i].data.materials )
			if number_of_materials > 0: #rename material
				if bpy.context.scene.get_object_name: # get name from object
					name_mat = "{}{}{}".format(addon_prefs.mesh_preffix, addon_prefs.mesh_name, addon_prefs.mesh_suffix)
					selected_objects[i].data.materials[0].name = name_mat
				else: # get our name
					name_mat = "{}{}{}".format(addon_prefs.mat_preffix, addon_prefs.mat_name, addon_prefs.mat_suffix)
					selected_objects[i].data.materials[0].name = name_mat
			else: #create material
				if bpy.context.scene.get_object_name: # get name from object
					name_mat = "{}{}{}".format(addon_prefs.mesh_preffix, addon_prefs.mesh_name, addon_prefs.mesh_suffix)
					selected_objects[i].data.materials.append( bpy.data.materials.new( name_mat ) )
				else: # get our name
					name_mat = "{}{}{}".format(addon_prefs.mat_preffix, addon_prefs.mat_name, addon_prefs.mat_suffix)
					selected_objects[i].data.materials.append( bpy.data.materials.new( name_mat ) )

def rename_mesh(addon_prefs):
	selected_objects = bpy.context.selected_objects
	for i in range( len( selected_objects ) ):
		selected_objects[i].name = "{}{}{}".format(addon_prefs.mesh_preffix, addon_prefs.mesh_name, addon_prefs.mesh_suffix)

def add_suffix(addon_prefs):
	selected_objects = bpy.context.selected_objects
	for i in range( len( selected_objects ) ):
		temp_name = selected_objects[i].name
		temp_name = "{}{}".format(temp_name, addon_prefs.mesh_suffix)
		selected_objects[i].name = temp_name

def add_preffix(addon_prefs):
	selected_objects = bpy.context.selected_objects
	for i in range( len( selected_objects ) ):
		temp_name = selected_objects[i].name
		temp_name = "{}{}".format(addon_prefs.mesh_preffix, temp_name)
		selected_objects[i].name = temp_name


def GetMaterialByName(name):
	for mat in bpy.data.materials:
		if mat.name == name:
			return mat
	return False



class ImportBlendData(Operator, ImportHelper):
	"""This appears in the tooltip of the operator and in the generated docs"""
	bl_idname = "import_blend.blend_data"  # important since its how bpy.ops.import_blend.blend_data is constructed
	bl_label = "Import Blend Data"

	# ImportHelper mixin class uses this
	filename_ext = ".blend" # remove?

	filter_glob = StringProperty(
					default="*.blend",
					options={'HIDDEN'},
					maxlen=255,  # Max internal buffer length, longer would be clamped.
					)

	# List of operator properties, the attributes will be assigned
	# to the class instance from the operator settings before calling.
	use_setting = BoolProperty(
					name="Example Boolean",
					description="Example Tooltip",
					default=True,
					)

	type = EnumProperty(
					name="Example Enum",
					description="Choose between two items",
					items=(('OPT_A', "First Option", "Description one"),
								 ('OPT_B', "Second Option", "Description two")),
					default='OPT_A',
					)

	def execute(self, context):
			return read_blend_data(context, self.filepath, self.use_setting)

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
	self.layout.operator(ImportBlendData.bl_idname, text="Blend (.blend)")


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

class OBJECT_OT_rename(bpy.types.Operator):
	"""Rename meshes and materials"""
	bl_label = "Fast rename meshes"
	bl_idname = "object.rename"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		rename(addon_prefs)
		return {'FINISHED'}

class OBJECT_OT_rename_mat(bpy.types.Operator):
	"""Rename material"""
	bl_label = "Rename material"
	bl_idname = "object.rename_mat"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		rename_mat(addon_prefs)
		return {'FINISHED'}

class OBJECT_OT_rename_mesh(bpy.types.Operator):
	"""Rename mesh"""
	bl_label = "Rename material"
	bl_idname = "object.rename_mesh"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		rename_mesh(addon_prefs)
		return {'FINISHED'}

class OBJECT_OT_add_suffix(bpy.types.Operator):
	"""Add suffix to name object"""
	bl_label = "Add suffix to name object"
	bl_idname = "object.add_suffix"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		add_suffix(addon_prefs)
		return {'FINISHED'}

class OBJECT_OT_add_preffix(bpy.types.Operator):
	"""Add preffix to name object"""
	bl_label = "Add preffix to name object"
	bl_idname = "object.add_preffix"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		user_preferences = bpy.context.user_preferences
		addon_prefs = user_preferences.addons[__name__].preferences

		add_preffix(addon_prefs)
		return {'FINISHED'}

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
		description = "If the material is missing, then create it, otherwise create it"
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

		col = layout.column()
		col.operator("object.rename", text="Rename mesh and material")

		box = layout.box()
		col = box.column(align=True)
		col.label("Mesh")
		col.prop(addon_prefs, "mesh_preffix", text="Preffix")
		col.prop(addon_prefs, "mesh_name", text="Name")
		col.prop(addon_prefs, "mesh_suffix", text="Suffix")
		col.operator("object.rename_mesh", text="Rename mesh")

		row = box.row(align=True)
		row.operator("object.add_preffix", text="Add preffix")
		row.operator("object.add_suffix", text="Add suffix")

		col = layout.column(align=True)
		col.prop(scene, "name_mat_set", text="Add material")
		col.prop(scene, "get_object_name", text="Get object name")

		box = layout.box()
		col = box.column(align=True)
		col.label("Material")
		col.prop(addon_prefs, "mat_preffix", text="Preffix")
		col.prop(addon_prefs, "mat_name", text="Name")
		col.prop(addon_prefs, "mat_suffix", text="Suffix")
		col.operator("object.rename_mat", text="Rename mat")
		col.enabled = bpy.context.scene.name_mat_set

class UnrealPresetPanel(bpy.types.Panel):
	"""Creates a Panel in the view3d context of the tools panel (key "T")"""
	bl_label = "Unreal preset"
	bl_idname = "unrealpresetid"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Nexus Tools"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout
		obj = context.object
		scene = context.scene

		col = layout.column()
		col.operator("object.unreal_preset", text="Unreal preset")

class OBJECT_OT_unreal_preset(bpy.types.Operator):
	"""Fast rename meshes"""
	bl_label = "Unreal preset"
	bl_idname = "object.unreal_preset"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		uv_create_to_selected()
		rename_object_to_selected()
		return {'FINISHED'}

class ChangeMaterial(bpy.types.Panel):
	"""Creates a Panel in the view3d context of the tools panel (key "T")"""
	bl_label = "Change materials"
	bl_idname = "changematid"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Nexus Tools"
	bl_context = "objectmode"

	def draw(self, context):
		layout = self.layout
		obj = context.object
		scene = context.scene

		col = layout.column()
		col.operator("object.change_mat", text="Change materials")
		col.operator("object.del_dulpi_mat", text="Delete materials")

class OBJECT_OT_change_mat(bpy.types.Operator):
	"""Change materials on active objects by template: NameMat.something"""
	bl_label = "Change materials"
	bl_idname = "object.change_mat"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		for ob in bpy.context.selected_objects:
			i = 0
			for mat in ob.data.materials:
				if (len(mat.name.split('.')) > 1):
					mainMat = GetMaterialByName(mat.name.split('.')[0])
					if mainMat != False:
						ob.data.materials[i] = mainMat
				i += 1

		return {'FINISHED'}

class OBJECT_OT_delete_duplicate_mat(bpy.types.Operator):
	"""Delete duplicate materials by template from ALL list material: NameMat.something"""
	bl_label = "Delete materials"
	bl_idname = "object.del_dulpi_mat"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return context.mode == "OBJECT"

	def execute(self, context):
		for mat in bpy.data.materials:
			if len(mat.name.split('.')) > 1:
				bpy.data.materials.remove(mat)

		return {'FINISHED'}

def register():
	bpy.utils.register_class(FastRenamePanel)
	bpy.utils.register_class(UnrealPresetPanel)
	bpy.utils.register_class(OBJECT_OT_rename)
	bpy.utils.register_class(OBJECT_OT_rename_mesh)
	bpy.utils.register_class(OBJECT_OT_rename_mat)
	bpy.utils.register_class(OBJECT_OT_add_suffix)
	bpy.utils.register_class(OBJECT_OT_add_preffix)
	bpy.utils.register_class(OBJECT_OT_unreal_preset)
	bpy.utils.register_class(ExampleAddonPreferences)
	bpy.utils.register_class(ChangeMaterial)
	bpy.utils.register_class(OBJECT_OT_change_mat)
	bpy.utils.register_class(OBJECT_OT_delete_duplicate_mat)
	bpy.utils.register_class(ImportBlendData)
	bpy.types.INFO_MT_file_import.append(menu_func_import)
	# bpy.utils.register_class(ExplodeData)

def unregister():
	bpy.utils.unregister_class(FastRenamePanel)
	bpy.utils.unregister_class(UnrealPresetPanel)
	bpy.utils.unregister_class(OBJECT_OT_rename)
	bpy.utils.unregister_class(OBJECT_OT_rename_mesh)
	bpy.utils.unregister_class(OBJECT_OT_rename_mat)
	bpy.utils.unregister_class(OBJECT_OT_add_suffix)
	bpy.utils.unregister_class(OBJECT_OT_add_preffix)
	bpy.utils.unregister_class(OBJECT_OT_unreal_preset)
	bpy.utils.unregister_class(ExampleAddonPreferences)
	bpy.utils.unregister_class(ChangeMaterial)
	bpy.utils.unregister_class(OBJECT_OT_change_mat)
	bpy.utils.unregister_class(OBJECT_OT_delete_duplicate_mat)
	bpy.utils.unregister_class(ImportBlendData)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)
	# bpy.utils.unregister_class(ExplodeData)

if __name__ == "__main__":
	register()
# bpy.types.Object.explode_data = bpy.props.PointerProperty(type=ExplodeData)
