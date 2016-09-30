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
from bpy.props import *



#class panel
class NexusToolsPanel(bpy.types.Panel):
	"""Creates a Panel in the view3d context of the tools panel (key "T")"""
	bl_label = "Nexus Tools"
	bl_idname = "nexustoolsid"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Nexus Tools"
	bl_context = "objectmode"
	
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

	def draw(self, context):
		layout = self.layout
		
		box = layout.box()
		
		box.label(text="Explode objects")
		
		col = box.column(align=True)
		col.prop(context.scene, "explodeX")
		col.prop(context.scene, "explodeY")
		col.prop(context.scene, "explodeZ")

	def execute(self, context):
		bpy.context.object.location.x += offsetX


def register():
	bpy.utils.register_class(LayoutDemoPanel)


def unregister():
	bpy.utils.unregister_class(LayoutDemoPanel)


if __name__ == "__main__":
	register()
