import bpy
import bmesh
so=bpy.context.active_object
bpy.ops.mesh.uv_texture_add()
bpy.ops.object.editmode_toggle()
bpy.ops.uv.select_all(action='SELECT')
#uvlayer=so.data.uv_layers.active
#for face in so.faces:
#    for v,l in zip(face.vertices,face.loop_indices):
#        uv_layer.data[l].uv=(0,0)
me = so.data
bm = bmesh.from_edit_mesh(me)

uv_layer = bm.loops.layers.uv.verify()

    # adjust uv coordinates
for face in bm.faces:
    for loop in face.loops:
        loop_uv = loop[uv_layer]
            # use xy position of the vertex as a uv coordinate
        loop_uv.uv = (0,0)

bmesh.update_edit_mesh(me)


so.modifiers.new("subsurf",'SUBSURF') 
bpy.context.object.modifiers["subsurf"].render_levels = 1
so.modifiers.new("array",'ARRAY')
bpy.context.object.modifiers["array"].use_relative_offset = False
bpy.context.object.modifiers["array"].show_in_editmode = False

bpy.context.object.modifiers["array"].count = 70
bpy.context.object.modifiers["array"].offset_u = 0.0001
 
mod_displace=so.modifiers.new("displace",'DISPLACE')
bpy.context.object.modifiers["displace"].texture_coords = 'UV'
bpy.context.object.modifiers["displace"].uv_layer = "UVMap.001"
bpy.context.object.modifiers["displace"].strength = 0.2
bpy.context.object.modifiers["displace"].mid_level = 0.2


so.modifiers.new("weld",'WELD') 

#bpy.ops.uv.snap_selected(target='CURSOR')


bpy.ops.object.editmode_toggle()
#bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)




