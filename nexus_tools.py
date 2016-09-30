import bpy
from bpy.props import *

class LayoutDemoPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Nexus Tools"
    bl_idname = "nexustoolsid"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Nexus Tools"
    bl_context = "objectmode"
    
    bpy.types.Scene.explodeX = FloatProperty(
        name = "X",
        min = 0,
        default = 0.0,
        description = "Explode meshes by X coordinate"
    )
    
    bpy.types.Scene.explodeY = FloatProperty(
        name = "Y",
        min = 0,
        default = 0.0,
        description = "Explode meshes by Y coordinate"
    )
    
    bpy.types.Scene.explodeZ = FloatProperty(
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


def register():
    bpy.utils.register_class(LayoutDemoPanel)


def unregister():
    bpy.utils.unregister_class(LayoutDemoPanel)


if __name__ == "__main__":
    register()
