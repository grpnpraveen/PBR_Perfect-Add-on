bl_info = {
    "name": "PBR Perfect",
    "author": "Gali_Ravi_Praveen",
    "version": (1, 0),
    "blender": (2, 91, 2),
    "location": "View3D > Toolshelf",
    "description": "Adds a new Shader to your Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Shader",
}


import bpy
import bmesh
import os
images_path=["1","2","3","4","5","6","7"]
#Custom properties
class MyProperties(bpy.types.PropertyGroup):
    
    mat_string: bpy.props.StringProperty(name="Name")
    
    height_strength: bpy.props.FloatProperty(name="Normal_map Strength",min=1,max=10,default=1.0)

    efficiency_strength: bpy.props.EnumProperty(name="Bump Efficiency",description="your choice",items=[('OP1',"Medium",""),('OP2',"High","")])
    
    render_engine: bpy.props.EnumProperty(name="Render Engine",description="important",items=[('OP1',"Eevee",""),('OP2',"Cycles","")])
    
    shape:bpy.props.EnumProperty(name="shape",description="imp",items=[('NP',"Not a Square thing",""),('P',"Square thing","")])


#           PANEL  DESIGN                                                                                  
class ShaderMainPanel(bpy.types.Panel):
    bl_label = "PBR Perfect"
    bl_idname = "SHADER_PT_MAINPANEL"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'PBR Perfect'

    def draw(self, context):
        layout = self.layout
        scene=context.scene
        mytool=scene.my_tool
        row=layout.row()
        row.label(text="Select Suitable Texture Maps.")
        row=layout.row()
        row.label(text=None,icon="SHADING_TEXTURE")
        row.prop(mytool,"mat_string")               #one
        row=layout.row()
        row.scale_x=2.6    #map name
        row.label(text="Albedo Map")
        if images_path[0]!="1":
            row.label(text=os.path.basename(images_path[0]),icon="FILE_IMAGE")
        row.scale_x=2.1   #open button
        row.operator('shader.albedo_operator',text="open",icon="FILEBROWSER")
        row.scale_x=1   #cross button
        row.operator('shader.1cancel_operator',text="",icon="CANCEL")                 #need to write separate operator
        row=layout.row()                            #two
        row.scale_x=2.6    #map name
        row.label(text="Normal Map")
        if images_path[1]!="2":
            row.label(text=os.path.basename(images_path[1]),icon="FILE_IMAGE")
        row.scale_x=2.1   #open button
        row.operator('shader.normal_operator',text="open",icon="FILEBROWSER")
        row.scale_x=1   #cross button
        row.operator('shader.2cancel_operator',text="",icon="CANCEL")                 #need to write separate operator
        row=layout.row()
        row.prop(mytool,"height_strength")        #three
        row=layout.row()
        row.scale_x=2.6    #map name
        row.label(text="Roughness Map")
        if images_path[2]!="3":
            row.label(text=os.path.basename(images_path[2]),icon="FILE_IMAGE")
        row.scale_x=2.1   #open button
        row.operator('shader.roughness_operator',text="open",icon="FILEBROWSER")
        row.scale_x=1   #cross button
        row.operator('shader.3cancel_operator',text="",icon="CANCEL")                 #need to write separate operator
        row=layout.row()                            #four
        row.scale_x=2.6    #map name
        row.label(text="Ambient occlusion Map")
        if images_path[3]!="4":
            row.label(text=os.path.basename(images_path[3]),icon="FILE_IMAGE")
        row.scale_x=2.1   #open button
        row.operator('shader.ambient_operator',text="open",icon="FILEBROWSER")
        row.scale_x=1   #cross button
        row.operator('shader.4cancel_operator',text="",icon="CANCEL")                 #need to write separate operator
        row=layout.row()                           #five
        row.scale_x=2.6    #map name
        row.label(text="Metallic Map")
        if images_path[4]!="5":
            row.label(text=os.path.basename(images_path[4]),icon="FILE_IMAGE")
        row.scale_x=2.1   #open button
        row.operator('shader.metallic_operator',text="open",icon="FILEBROWSER")
        row.scale_x=1   #cross button
        row.operator('shader.5cancel_operator',text="",icon="CANCEL")                 #need to write separate operator
        row=layout.row()                           #six
        row.scale_x=2.6    #map name
        row.label(text="Height Map")
        if images_path[5]!="6":
            row.label(text=os.path.basename(images_path[5]),icon="FILE_IMAGE")
        row.scale_x=2.1   #open button
        row.operator('shader.height_operator',text="open",icon="FILEBROWSER")
        row.scale_x=1   #cross button
        row.operator('shader.6cancel_operator',text="",icon="CANCEL")                 #need to write separate operator
        row=layout.row()                        #seven
        row.scale_x=0    #efficiency  name
        row.prop(mytool,"efficiency_strength")                   #efficiency dropdown
        row=layout.row()
        row.scale_x=1.6    #map name
        row.label(text="Specular Map")
        if images_path[6]!="7":
            row.label(text=os.path.basename(images_path[6]),icon="FILE_IMAGE")
        row.scale_x=2.1   #open button
        row.operator('shader.specular_operator',text="open",icon="FILEBROWSER")
        row.scale_x=1   #cross button
        row.operator('shader.7cancel_operator',text="",icon="CANCEL")                 #need to write separate operator
        row=layout.row()
        row.prop(mytool,"render_engine") 
        row=layout.row()
        if mytool.efficiency_strength=='OP2':
            if mytool.render_engine=='OP1':
                row.prop(mytool,"shape")
        row=layout.row()
        row.scale_y=1.8
        row.operator('shader.material_operator',text="Create Material",icon="BRUSH_SOFTEN")

#     MATERIAL  ------------NODE SETUP

class Material(bpy.types.Operator):                              
    bl_label="open"
    bl_idname='shader.material_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        scene=context.scene
        mytool=scene.my_tool
        so=bpy.context.active_object
        new_material=bpy.data.materials.new(name=mytool.mat_string)
        so.data.materials.append(new_material)
        new_material.use_nodes=True
        new_material.use_backface_culling = True
        new_material.blend_method = 'CLIP'
        new_material.shadow_method = 'CLIP'
        nodes=new_material.node_tree.nodes #accesiing all the nodes of new_material
        links=new_material.node_tree.links
        material_output=nodes.get("Material Output")
        principle_bsdf=nodes.get("Principled BSDF")
        principle_bsdf.inputs[8].default_value = 0.35
        uv_map_node=nodes.new(type='ShaderNodeUVMap')
        uv_map_node.location=(-2600,300)
        uv_map_node.uv_map="UVMap"
        mapping_node=nodes.new(type='ShaderNodeMapping')  #mapping node
        mapping_node.inputs[3].default_value[0] = 1
        mapping_node.inputs[3].default_value[1] = 1
        mapping_node.inputs[3].default_value[2] = 1
        mapping_node.location=(-2400,300)
        material_output.location=(700,300)
        uvlink_to_mapping=links.new(uv_map_node.outputs[0],mapping_node.inputs[0])
        if images_path[0]!="1" and images_path[3]=="4":        #only albedo
             node_one=nodes.new(type='ShaderNodeTexImage')
             bpy.data.images.load(images_path[0], check_existing=True)
             tex = bpy.data.images.get(os.path.basename(images_path[0])) 
             node_one.location=(-800,540)
             node_one.image=tex
             node_one.label="Albedo Map"
             bpy.data.images[os.path.basename(images_path[0])].colorspace_settings.name='sRGB'
             new_link=links.new(node_one.outputs[0],principle_bsdf.inputs[0]) #link btwn albedo and pbsdf
             map_to_albe=links.new(mapping_node.outputs[0],node_one.inputs[0])
        if images_path[0]=="1" and images_path[3]!="4":       #only ambient  
             node_two=nodes.new(type='ShaderNodeTexImage')
             bpy.data.images.load(images_path[3], check_existing=True)
             tex = bpy.data.images.get(os.path.basename(images_path[3]))
             node_two.image=tex
             node_two.label="Ambient Occlusion Map"
             bpy.data.images[os.path.basename(images_path[3])].colorspace_settings.name='Non-Color' 
             node_two.location=(-1100,700)   #ambient occlusion  texture 
             node_three=nodes.new(type='ShaderNodeAmbientOcclusion')     #ambient occlusion map
             node_three.location=(-300,500)
             node_four=nodes.new(type='ShaderNodeValToRGB')    #color ramp
             node_four.location=(-700,600)
             node_four.color_ramp.elements[0].position= 0.32
             amb_color_link=links.new(node_two.outputs[0],node_four.inputs[0]) #link btwn ambient and colorramp
             coloramp_amb_link=links.new(node_four.outputs[0],node_three.inputs[0]) 
             amb_to_pbsdf=links.new(node_three.outputs[0],principle_bsdf.inputs[0])         
             map_to_ambi=links.new(mapping_node.outputs[0],node_two.inputs[0])
        if images_path[0]!="1" and images_path[3]!="4":           
             node_one=nodes.new(type='ShaderNodeTexImage')
             bpy.data.images.load(images_path[0], check_existing=True)          #both albedo and ambient
             tex = bpy.data.images.get(os.path.basename(images_path[0])) 
             node_one.image=tex
             node_one.label="Albedo Map"
             bpy.data.images[os.path.basename(images_path[0])].colorspace_settings.name='sRGB'
             node_one.location=(-1000,420)    #albedo
             node_two=nodes.new(type='ShaderNodeTexImage')
             bpy.data.images.load(images_path[3], check_existing=True)
             tex = bpy.data.images.get(os.path.basename(images_path[3]))
             node_two.image=tex
             node_two.label="Ambient Occlusion Map"
             bpy.data.images[os.path.basename(images_path[3])].colorspace_settings.name='Non-Color' 
             node_two.location=(-1100,700)   #ambient occlusion
             node_three=nodes.new(type='ShaderNodeMixRGB')
             node_three.location=(-400,500)    #mixrgb
             node_three.blend_type='MULTIPLY'     
             albedo_to_multiply_link=links.new(node_one.outputs[0],node_three.inputs[1])  #albedo to multiply
             ambient_multiply_link1=links.new(node_two.outputs[0],node_three.inputs[2])     #ambient to multiply
             ambient_multiply_link2=links.new(node_two.outputs[1],node_three.inputs[0])      #multiply to pBSDF
             multi_to_princile_link=links.new(node_three.outputs[0],principle_bsdf.inputs[0])
             map_to_albe=links.new(mapping_node.outputs[0],node_one.inputs[0])              #map to ambien and albedo
             map_to_ambient=links.new(mapping_node.outputs[0],node_two.inputs[0])  
        if images_path[1]!="2" and images_path[5]=="6":       
            node_one=nodes.new(type='ShaderNodeTexImage')                 #only normal map
            bpy.data.images.load(images_path[1], check_existing=True)
            tex = bpy.data.images.get(os.path.basename(images_path[1])) 
            node_one.image=tex 
            node_one.label="Normal Texture"
            bpy.data.images[os.path.basename(images_path[1])].colorspace_settings.name='Non-Color'
            node_one.location=(-690,-300)         #only NORMAL  texture
            node_two=nodes.new(type='ShaderNodeNormalMap')  #normal map
            node_two.uv_map='UVMap'
            node_two.inputs[0].default_value =mytool.height_strength
            node_two.location=(-300,-300) 
            link_to_normal=links.new(node_one.outputs[0],node_two.inputs[1])
            link_from_normal_to_princi=links.new(node_two.outputs[0],principle_bsdf.inputs[20])
            map_to_normtexture=links.new(mapping_node.outputs[0],node_one.inputs[0])
        if images_path[1]=="2" and images_path[5]!="6":
            if mytool.efficiency_strength=='OP1':                                 #when low efficiency
                node_three=nodes.new(type='ShaderNodeTexImage')                #  onlyheight texture
                bpy.data.images.load(images_path[5], check_existing=True)
                tex = bpy.data.images.get(os.path.basename(images_path[5])) 
                node_three.image=tex 
                node_three.label="Height Map"
                bpy.data.images[os.path.basename(images_path[5])].colorspace_settings.name='Non-Color'
                node_three.location=(-690,-280)
                node_four=nodes.new(type='ShaderNodeBump')   #BUMP texture
                node_four.location=(-200,-180)
                node_five=nodes.new(type='ShaderNodeRGBToBW')  #rgb to black and white
                node_five.location=(-425,-230)
                height_to_rgbw=links.new(node_three.outputs[0],node_five.inputs[0])
                rgbw_to_bump=links.new(node_five.outputs[0],node_four.inputs[2])
                bump_to_pbsdf=links.new(node_four.outputs[0],principle_bsdf.inputs[20])
                map_to_heighttex=links.new(mapping_node.outputs[0],node_three.inputs[0])
            if mytool.efficiency_strength=='OP2':                 #when high efficiency
                if mytool.render_engine=='OP2':                   #incycles
                    node_three=nodes.new(type='ShaderNodeTexImage') #height texture
                    gg=bpy.data.images.load(images_path[5], check_existing=True)
                    tex = bpy.data.images.get(os.path.basename(images_path[5])) 
                    node_three.image=tex 
                    node_three.label="Height Map"
                    bpy.data.images[os.path.basename(images_path[5])].colorspace_settings.name='Non-Color'
                    node_three.location=(200,200)
                    node_four=nodes.new(type='ShaderNodeDisplacement') #displace node
                    node_four.inputs[1].default_value=0.2
                    node_four.inputs[2].default_value=0.5
                    node_four.location=(490,200)
                    heigh_displ=links.new(node_three.outputs[0],node_four.inputs[0])
                    displ_materout=links.new(node_four.outputs[0],material_output.inputs[2])
                    map_to_disp=links.new(mapping_node.outputs[0],node_three.inputs[0])
                    mod_displace=so.modifiers.new("displace",'DISPLACE')
                    new_texture=bpy.data.textures.new("image",'IMAGE')
                    new_texture.image=gg
                    mod_displace.texture=new_texture
                    mod_subdivi=so.modifiers.new("subsurf",'SUBSURF')
                    mod_subdivi.subdivision_type = 'SIMPLE'
                    bpy.context.scene.render.engine = 'CYCLES'
                    bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
                    bpy.context.object.active_material.cycles.displacement_method = 'BOTH'
                    bpy.context.scene.cycles.preview_dicing_rate = 1
                    bpy.context.object.cycles.use_adaptive_subdivision = True
                if mytool.render_engine=='OP1':     #in Eevee
                    node_three=nodes.new(type='ShaderNodeTexImage') #height texture
                    gg=bpy.data.images.load(images_path[5], check_existing=True)
                    tex = bpy.data.images.get(os.path.basename(images_path[5])) 
                    node_three.image=tex 
                    node_three.label="Height Map"
                    bpy.data.images[os.path.basename(images_path[5])].colorspace_settings.name='Non-Color'
                    node_three.location=(200,200)
                    map_to_disp=links.new(mapping_node.outputs[0],node_three.inputs[0])#link from mapping to displ tex
                    #   Eevee displacement NODE GROUP
                    bpy.ops.mesh.uv_texture_add()
#                    so.data.uv_layers.new(name='hello')                                            use incase uv map already there with tha name uvmap.001
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.uv.select_all(action='SELECT')
                    me = so.data
                    bm = bmesh.from_edit_mesh(me)
                    uv_layer = bm.loops.layers.uv.verify()    #accessing uv map
                    for face in bm.faces:
                        for loop in face.loops:
                            loop_uv = loop[uv_layer]
                            loop_uv.uv = (0,0)
                    bmesh.update_edit_mesh(me)
                    so.modifiers.new("subsurf",'SUBSURF') 
                    bpy.context.object.modifiers["subsurf"].render_levels = 1
                    if mytool.shape=='P':
                        bpy.context.object.modifiers["subsurf"].subdivision_type = 'SIMPLE'     
                    so.modifiers.new("array",'ARRAY')
                    bpy.context.object.modifiers["array"].use_relative_offset = False
                    bpy.context.object.modifiers["array"].show_in_editmode = False
                    bpy.context.object.modifiers["array"].count = 70
                    bpy.context.object.modifiers["array"].offset_u = 0.0001
                    mod_displace=so.modifiers.new("displace",'DISPLACE')
                    new_texture=bpy.data.textures.new("blend",'BLEND')
                    new_texture.use_clamp = False
                    new_texture.use_color_ramp = True
                    new_texture.color_ramp.elements[0].color=(0,0,0,1)
                    new_texture.color_ramp.elements[1].position=0.01
                    new_texture.color_ramp.elements[1].color=(1,1,1,0)
                                                                                               #-----------------here used name of the uv map instead active
                    mod_displace.texture=new_texture
                    bpy.context.object.modifiers["displace"].texture_coords = 'UV'
                    bpy.context.object.modifiers["displace"].uv_layer = "UVMap.001"
                    bpy.context.object.modifiers["displace"].strength = 0.2
                    bpy.context.object.modifiers["displace"].mid_level = 0.2
                    so.modifiers.new("weld",'WELD') 
                    bpy.ops.object.editmode_toggle()
                    #uv
                    node_uv=nodes.new(type='ShaderNodeUVMap')
                    node_uv.uv_map="UVMap.001"
                    node_uv.location=(900,300)
                    #mul1
                    node_multiply1=nodes.new(type='ShaderNodeMath')
                    node_multiply1.operation='MULTIPLY'
                    node_multiply1.inputs[1].default_value=-1.0
                    node_multiply1.location=(900,100)
                    #mul2
                    node_multiply2=nodes.new(type='ShaderNodeMath')
                    node_multiply2.operation='MULTIPLY'
                    node_multiply2.inputs[1].default_value=-1.0
                    node_multiply2.location=(900,-100)
                    #mul3
                    node_multiply3=nodes.new(type='ShaderNodeMath')
                    node_multiply3.operation='MULTIPLY'
                    node_multiply3.inputs[1].default_value=-1.0
                    node_multiply3.location=(1100,100)
                    #mul4
                    node_multiply4=nodes.new(type='ShaderNodeMath')
                    node_multiply4.operation='MULTIPLY'
                    node_multiply4.inputs[1].default_value=1000
                    node_multiply4.use_clamp=False
                    node_multiply4.location=(1300,200)
                    #separatexyz
                    node_separatexyz=nodes.new(type='ShaderNodeSeparateXYZ')
                    node_separatexyz.location=(1100,300)
                    #add1
                    node_add1=nodes.new(type='ShaderNodeMath')
                    node_add1.operation='ADD'
                    node_add1.inputs[1].default_value=1.0
                    node_add1.location=(1100,-100)
                    #add2
                    node_add2=nodes.new(type='ShaderNodeMath')
                    node_add2.operation='ADD'
                    node_add2.location=(1300,-50)
                    #mixrgb
                    node_mixrgb=nodes.new(type='ShaderNodeMixRGB')
                    node_mixrgb.location=(1550,50)
                    #lessthan
                    node_less=nodes.new('ShaderNodeMath')
                    node_less.operation='LESS_THAN'
                    node_less.inputs[1].default_value = 0.001
                    node_less.location=(1800,125)
                    #greaterthan
                    node_greater=nodes.new('ShaderNodeMath')
                    node_greater.operation='GREATER_THAN'
                    node_greater.location=(1800,300)
                    #subtract
                    node_sub=nodes.new(type='ShaderNodeMath')
                    node_sub.operation='SUBTRACT'
                    node_sub.use_clamp=True
                    node_sub.location=(2000,213)
                    #mix shader
                    node_mixshad=nodes.new(type='ShaderNodeMixShader')
                    node_mixshad.location=(2200,120)
                    #transparentbsdf
                    node_transp=nodes.new(type='ShaderNodeBsdfTransparent')
                    node_transp.location=(2000,20)
                    #strength
                    node_stren=nodes.new(type='ShaderNodeValue')
                    node_stren.label="Strength"
                    node_stren.outputs[0].default_value=15
                    node_stren.location=(600,30)
                    #midlevel
                    node_mid=nodes.new(type='ShaderNodeValue')
                    node_mid.label="Midlevel"
                    node_mid.outputs[0].default_value=-2.4
                    node_mid.location=(600,-50)
                    #linking now
                    uv_sep=links.new(node_uv.outputs[0],node_separatexyz.inputs[0])
                    sep_mul4=links.new(node_separatexyz.outputs[0],node_multiply4.inputs[0])
                    mul4_mixrgb=links.new(node_multiply4.outputs[0],node_mixrgb.inputs[1])
                    mul1_mul3=links.new(node_multiply1.outputs[0],node_multiply3.inputs[1])
                    mul2_add1=links.new(node_multiply2.outputs[0],node_add1.inputs[0])
                    add1_add2=links.new(node_add1.outputs[0],node_add2.inputs[1])
                    mul3_add2=links.new(node_multiply3.outputs[0],node_add2.inputs[0])
                    add2_mixrgb=links.new(node_add2.outputs[0],node_mixrgb.inputs[2])
                    mixrgb_greater=links.new(node_mixrgb.outputs[0],node_greater.inputs[0])
                    mul4_less=links.new(node_multiply4.outputs[0],node_less.inputs[0])
                    great_sub=links.new(node_greater.outputs[0],node_sub.inputs[0])
                    less_sub=links.new(node_less.outputs[0],node_sub.inputs[1])
                    sub_mixshad=links.new(node_sub.outputs[0],node_mixshad.inputs[0])
                    transp_mixshad=links.new(node_transp.outputs[0],node_mixshad.inputs[2])
                    #link part2
                    displatex_mul3=links.new(node_three.outputs[0],node_multiply3.inputs[0])
                    principle_mixshad=links.new(principle_bsdf.outputs[0],node_mixshad.inputs[1])
                    mixshad_material=links.new(node_mixshad.outputs[0],material_output.inputs[0])
                    material_output.location=(2380,120)  
                    stren_mul1=links.new(node_stren.outputs[0],node_multiply1.inputs[0])
                    mid_mul2=links.new(node_mid.outputs[0],node_multiply2.inputs[0])
        if images_path[1]!="2" and images_path[5]!="6":     #if normal and displ selected                      
            if mytool.efficiency_strength=='OP1':                  #both normal and displacemnet
                node_one=nodes.new(type='ShaderNodeTexImage')           #  normal texture 
                bpy.data.images.load(images_path[1], check_existing=True)
                tex = bpy.data.images.get(os.path.basename(images_path[1])) 
                node_one.image=tex 
                node_one.label="Normal Texture"
                bpy.data.images[os.path.basename(images_path[1])].colorspace_settings.name='Non-Color'
                node_one.location=(-890,-550)         
                node_two=nodes.new(type='ShaderNodeNormalMap')  #normal map
                node_two.uv_map='UVMap'
                node_two.inputs[0].default_value =mytool.height_strength
                node_two.location=(-520,-520) 
                node_three=nodes.new(type='ShaderNodeTexImage') #height texture
                bpy.data.images.load(images_path[5], check_existing=True)
                tex = bpy.data.images.get(os.path.basename(images_path[5])) 
                node_three.image=tex 
                node_three.label="Height Map"
                bpy.data.images[os.path.basename(images_path[5])].colorspace_settings.name='Non-Color'
                node_three.location=(-690,-280)
                node_four=nodes.new(type='ShaderNodeBump')   #BUMP texture
                node_four.location=(-200,-180)
                node_five=nodes.new(type='ShaderNodeRGBToBW')  #rgb to black and white
                node_five.location=(-425,-230)
                nmap_to_bump=links.new(node_two.outputs[0],node_four.inputs[5])
                normal_link_to_nmap=links.new(node_one.outputs[0],node_two.inputs[1])          
                height_to_rgbw=links.new(node_three.outputs[0],node_five.inputs[0])
                rgbw_to_bump=links.new(node_five.outputs[0],node_four.inputs[2])
                bump_to_pbsdf=links.new(node_four.outputs[0],principle_bsdf.inputs[20])
                map_to_nortex=links.new(mapping_node.outputs[0],node_one.inputs[0])
                map_to_heighttex=links.new(mapping_node.outputs[0],node_three.inputs[0])
            if mytool.efficiency_strength=='OP2':    #high cycles
                if mytool.render_engine=='OP2':
                    node_one=nodes.new(type='ShaderNodeTexImage')                 #first normal tex
                    bpy.data.images.load(images_path[1], check_existing=True)
                    tex = bpy.data.images.get(os.path.basename(images_path[1])) 
                    node_one.image=tex 
                    node_one.label="Normal Texture"
                    bpy.data.images[os.path.basename(images_path[1])].colorspace_settings.name='Non-Color'
                    node_one.location=(-690,-300)         
                    node_two=nodes.new(type='ShaderNodeNormalMap')  #normal map
                    node_two.uv_map='UVMap'
                    node_two.inputs[0].default_value =mytool.height_strength
                    node_two.location=(-300,-300) 
                    link_to_normal=links.new(node_one.outputs[0],node_two.inputs[1])
                    link_from_normal_to_princi=links.new(node_two.outputs[0],principle_bsdf.inputs[20])
                    map_to_normtexture=links.new(mapping_node.outputs[0],node_one.inputs[0])
                    node_three=nodes.new(type='ShaderNodeTexImage') #height texture
                    gg=bpy.data.images.load(images_path[5], check_existing=True)
                    tex = bpy.data.images.get(os.path.basename(images_path[5])) 
                    node_three.image=tex 
                    node_three.label="Height Map"
                    bpy.data.images[os.path.basename(images_path[5])].colorspace_settings.name='Non-Color'
                    node_three.location=(200,200)
                    node_four=nodes.new(type='ShaderNodeDisplacement') #displace node
                    node_four.inputs[1].default_value=0.2
                    node_four.inputs[2].default_value=0.5
                    node_four.location=(490,200)
                    heigh_displ=links.new(node_three.outputs[0],node_four.inputs[0])
                    displ_materout=links.new(node_four.outputs[0],material_output.inputs[2])
                    map_to_disp=links.new(mapping_node.outputs[0],node_three.inputs[0])
                    mod_displace=so.modifiers.new("displace",'DISPLACE')
                    new_texture=bpy.data.textures.new("image",'IMAGE')
                    new_texture.image=gg
                    mod_displace.texture=new_texture
                    mod_subdivi=so.modifiers.new("subsurf",'SUBSURF')
                    mod_subdivi.subdivision_type = 'SIMPLE'
                    bpy.context.scene.render.engine = 'CYCLES'
                    bpy.context.scene.cycles.feature_set = 'EXPERIMENTAL'
                    bpy.context.object.active_material.cycles.displacement_method = 'BOTH'
                    bpy.context.scene.cycles.preview_dicing_rate = 1
                    bpy.context.object.cycles.use_adaptive_subdivision = True
                if mytool.render_engine=='OP1':
                    node_one=nodes.new(type='ShaderNodeTexImage')                 # normal tex
                    bpy.data.images.load(images_path[1], check_existing=True)
                    tex = bpy.data.images.get(os.path.basename(images_path[1])) 
                    node_one.image=tex 
                    node_one.label="Normal Texture"
                    bpy.data.images[os.path.basename(images_path[1])].colorspace_settings.name='Non-Color'
                    node_one.location=(-690,-300)         # NORMAL  texture
                    node_two=nodes.new(type='ShaderNodeNormalMap')  #normal map
                    node_two.uv_map='UVMap'
                    node_two.inputs[0].default_value =mytool.height_strength
                    node_two.location=(-300,-300) 
                    link_to_normal=links.new(node_one.outputs[0],node_two.inputs[1])
                    link_from_normal_to_princi=links.new(node_two.outputs[0],principle_bsdf.inputs[20])
                    map_to_normtexture=links.new(mapping_node.outputs[0],node_one.inputs[0])
                    node_three=nodes.new(type='ShaderNodeTexImage') #height texture
                    gg=bpy.data.images.load(images_path[5], check_existing=True)
                    tex = bpy.data.images.get(os.path.basename(images_path[5])) 
                    node_three.image=tex 
                    node_three.label="Height Map"
                    bpy.data.images[os.path.basename(images_path[5])].colorspace_settings.name='Non-Color'
                    node_three.location=(200,200)
                    map_to_disp=links.new(mapping_node.outputs[0],node_three.inputs[0])#link from mapping to displ tex
                    #   CUSTOM NODE GROUP
                    bpy.ops.mesh.uv_texture_add()
                    bpy.ops.object.editmode_toggle()
                    bpy.ops.uv.select_all(action='SELECT')
                    me = so.data
                    bm = bmesh.from_edit_mesh(me)
                    uv_layer = bm.loops.layers.uv.verify()
                    for face in bm.faces:
                        for loop in face.loops:
                            loop_uv = loop[uv_layer]
                            loop_uv.uv = (0,0)
                    bmesh.update_edit_mesh(me)
                    so.modifiers.new("subsurf",'SUBSURF') 
                    bpy.context.object.modifiers["subsurf"].render_levels = 1
                    if mytool.shape=='P':
                        bpy.context.object.modifiers["subsurf"].subdivision_type = 'SIMPLE'
                    so.modifiers.new("array",'ARRAY')
                    bpy.context.object.modifiers["array"].use_relative_offset = False
                    bpy.context.object.modifiers["array"].show_in_editmode = False
                    bpy.context.object.modifiers["array"].count = 70
                    bpy.context.object.modifiers["array"].offset_u = 0.0001
                    mod_displace=so.modifiers.new("displace",'DISPLACE')
                    new_texture=bpy.data.textures.new("blend",'BLEND')
                    new_texture.use_clamp = False
                    new_texture.use_color_ramp = True
                    new_texture.color_ramp.elements[0].color=(0,0,0,1)
                    new_texture.color_ramp.elements[1].position=0.01
                    new_texture.color_ramp.elements[1].color=(1,1,1,0)
                                                                                         #-----------------here used name of the uv map instead active
                    mod_displace.texture=new_texture
                    bpy.context.object.modifiers["displace"].texture_coords = 'UV'
                    bpy.context.object.modifiers["displace"].uv_layer = "UVMap.001"                  #same here see above comment when only displacement when highe evee
                    bpy.context.object.modifiers["displace"].strength = 0.2
                    bpy.context.object.modifiers["displace"].mid_level = 0.2
                    so.modifiers.new("weld",'WELD') 
                    bpy.ops.object.editmode_toggle()
                    #uv
                    node_uv=nodes.new(type='ShaderNodeUVMap')
                    node_uv.uv_map="UVMap.001"
                    node_uv.location=(900,300)
                    #mul1
                    node_multiply1=nodes.new(type='ShaderNodeMath')
                    node_multiply1.operation='MULTIPLY'
                    node_multiply1.inputs[1].default_value=-1.0
                    node_multiply1.location=(900,100)
                    #mul2
                    node_multiply2=nodes.new(type='ShaderNodeMath')
                    node_multiply2.operation='MULTIPLY'
                    node_multiply2.inputs[1].default_value=-1.0
                    node_multiply2.location=(900,-100)
                    #mul3
                    node_multiply3=nodes.new(type='ShaderNodeMath')
                    node_multiply3.operation='MULTIPLY'
                    node_multiply3.inputs[1].default_value=-1.0
                    node_multiply3.location=(1100,100)
                    #mul4
                    node_multiply4=nodes.new(type='ShaderNodeMath')
                    node_multiply4.operation='MULTIPLY'
                    node_multiply4.inputs[1].default_value=1000
                    node_multiply4.use_clamp=False
                    node_multiply4.location=(1300,200)
                    #separatexyz
                    node_separatexyz=nodes.new(type='ShaderNodeSeparateXYZ')
                    node_separatexyz.location=(1100,300)
                    #add1
                    node_add1=nodes.new(type='ShaderNodeMath')
                    node_add1.operation='ADD'
                    node_add1.inputs[1].default_value=1.0
                    node_add1.location=(1100,-100)
                    #add2
                    node_add2=nodes.new(type='ShaderNodeMath')
                    node_add2.operation='ADD'
                    node_add2.location=(1300,-50)
                    #mixrgb
                    node_mixrgb=nodes.new(type='ShaderNodeMixRGB')
                    node_mixrgb.location=(1550,50)
                    #lessthan
                    node_less=nodes.new('ShaderNodeMath')
                    node_less.operation='LESS_THAN'
                    node_less.inputs[1].default_value = 0.001
                    node_less.location=(1800,125)
                    #greaterthan
                    node_greater=nodes.new('ShaderNodeMath')
                    node_greater.operation='GREATER_THAN'
                    node_greater.location=(1800,300)
                    #subtract
                    node_sub=nodes.new(type='ShaderNodeMath')
                    node_sub.operation='SUBTRACT'
                    node_sub.use_clamp=True
                    node_sub.location=(2000,213)
                    #mix shader
                    node_mixshad=nodes.new(type='ShaderNodeMixShader')
                    node_mixshad.location=(2200,120)
                    #transparentbsdf
                    node_transp=nodes.new(type='ShaderNodeBsdfTransparent')
                    node_transp.location=(2000,20)
                    #strength
                    node_stren=nodes.new(type='ShaderNodeValue')
                    node_stren.label="Strength"
                    node_stren.outputs[0].default_value=15
                    node_stren.location=(600,30)
                    #midlevel
                    node_mid=nodes.new(type='ShaderNodeValue')
                    node_mid.label="Midlevel"
                    node_mid.outputs[0].default_value=-2.4
                    node_mid.location=(600,-50)
                    #linking now
                    uv_sep=links.new(node_uv.outputs[0],node_separatexyz.inputs[0])
                    sep_mul4=links.new(node_separatexyz.outputs[0],node_multiply4.inputs[0])
                    mul4_mixrgb=links.new(node_multiply4.outputs[0],node_mixrgb.inputs[1])
                    mul1_mul3=links.new(node_multiply1.outputs[0],node_multiply3.inputs[1])
                    mul2_add1=links.new(node_multiply2.outputs[0],node_add1.inputs[0])
                    add1_add2=links.new(node_add1.outputs[0],node_add2.inputs[1])
                    mul3_add2=links.new(node_multiply3.outputs[0],node_add2.inputs[0])
                    add2_mixrgb=links.new(node_add2.outputs[0],node_mixrgb.inputs[2])
                    mixrgb_greater=links.new(node_mixrgb.outputs[0],node_greater.inputs[0])
                    mul4_less=links.new(node_multiply4.outputs[0],node_less.inputs[0])
                    great_sub=links.new(node_greater.outputs[0],node_sub.inputs[0])
                    less_sub=links.new(node_less.outputs[0],node_sub.inputs[1])
                    sub_mixshad=links.new(node_sub.outputs[0],node_mixshad.inputs[0])
                    transp_mixshad=links.new(node_transp.outputs[0],node_mixshad.inputs[2])
                    #link part2
                    displatex_mul3=links.new(node_three.outputs[0],node_multiply3.inputs[0])
                    principle_mixshad=links.new(principle_bsdf.outputs[0],node_mixshad.inputs[1])
                    mixshad_material=links.new(node_mixshad.outputs[0],material_output.inputs[0])
                    material_output.location=(2380,120)
                    stren_mul1=links.new(node_stren.outputs[0],node_multiply1.inputs[0])
                    mid_mul2=links.new(node_mid.outputs[0],node_multiply2.inputs[0])
        if images_path[2]!="3":
             node_one=nodes.new(type='ShaderNodeTexImage')                            #roughness map 
             bpy.data.images.load(images_path[2], check_existing=True)
             tex = bpy.data.images.get(os.path.basename(images_path[2])) 
             node_one.image=tex 
             node_one.label="Roughness Map"
             bpy.data.images[os.path.basename(images_path[2])].colorspace_settings.name='Non-Color'
             node_one.location=(-300,-10)       
             roughtex_to_principle=links.new(node_one.outputs[0],principle_bsdf.inputs[7])       #rough map to principle bsdf
             map_to_roughness=links.new(mapping_node.outputs[0],node_one.inputs[0])
        if images_path[4]!="5":
             node_one=nodes.new(type='ShaderNodeTexImage')   #metallic map
             bpy.data.images.load(images_path[4], check_existing=True)
             tex = bpy.data.images.get(os.path.basename(images_path[4])) 
             node_one.image=tex
             node_one.label="Metallic Map"
             bpy.data.images[os.path.basename(images_path[4])].colorspace_settings.name='Non-Color' 
             node_one.location=(-730,300)
             metallic_to_principle=links.new(node_one.outputs[0],principle_bsdf.inputs[4]) #metallic to princi
             map_to_metalic=links.new(mapping_node.outputs[0],node_one.inputs[0])
        if images_path[6]!="7":
             node_one=nodes.new(type='ShaderNodeTexImage')
             bpy.data.images.load(images_path[6], check_existing=True)
             tex = bpy.data.images.get(os.path.basename(images_path[6])) 
             node_one.image=tex 
             node_one.label="Specular Map"
             bpy.data.images[os.path.basename(images_path[6])].colorspace_settings.name='Non-Color'
             node_one.location=(-680,30)
             specular_to_principle_link=links.new(node_one.outputs[0],principle_bsdf.inputs[5])#specular ti principle
             map_to_specular=links.new(mapping_node.outputs[0],node_one.inputs[0])                                             
        return {'FINISHED'}
#           OPERATORS
class Albedo_Map(bpy.types.Operator):           #one                   
    bl_label="open"
    bl_idname='shader.albedo_operator'
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[0]=self.filepath
        bpy.utils.unregister_class(ShaderMainPanel)
        bpy.utils.register_class(ShaderMainPanel)                                                                 
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Normal_Map(bpy.types.Operator):         #two                     
    bl_label="open"
    bl_idname='shader.normal_operator'
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None
    def execute(self, context):
        images_path[1]=self.filepath                                                                
        return {'FINISHED'}
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Roughness_Map(bpy.types.Operator):             #three                 
    bl_label="open"
    bl_idname='shader.roughness_operator'
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[2]=self.filepath                                                              
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Ambient_Map(bpy.types.Operator):     #four                         
    bl_label="open"
    bl_idname='shader.ambient_operator'
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[3]=self.filepath                                                                 
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Metallic_Map(bpy.types.Operator):          #five                    
    bl_label="open"
    bl_idname='shader.metallic_operator'
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[4]=self.filepath                                                                     
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Height_Map(bpy.types.Operator):       #six                       
    bl_label="open"
    bl_idname='shader.height_operator'
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[5]=self.filepath                                                                       
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class Specular_Map(bpy.types.Operator):        #seven                      
    bl_label="open"
    bl_idname='shader.specular_operator'
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[6]=self.filepath                                                                         
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# image cancel selection
class AlbedoCancel_Map(bpy.types.Operator):     #one                         
    bl_label="open"
    bl_idname='shader.1cancel_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[0]="1"
        bpy.utils.unregister_class(ShaderMainPanel)
        bpy.utils.register_class(ShaderMainPanel)                                                                  
        return {'FINISHED'}

class NormalCancel_Map(bpy.types.Operator):   #two                           
    bl_label="open"
    bl_idname='shader.2cancel_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[1]="2"                                                                        
        return {'FINISHED'}

class RoughnessCancel_Map(bpy.types.Operator):     #three                         
    bl_label="open"
    bl_idname='shader.3cancel_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[2]="3"                                                                    
        return {'FINISHED'}

class AmbientCancel_Map(bpy.types.Operator):     #four                         
    bl_label="open"
    bl_idname='shader.4cancel_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[3]="4"                                                                          
        return {'FINISHED'}

class MetallicCancel_Map(bpy.types.Operator):       #five                       
    bl_label="open"
    bl_idname='shader.5cancel_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[4]="5"                                                                 
        return {'FINISHED'}

class HeightCancel_Map(bpy.types.Operator):     #six                         
    bl_label="open"
    bl_idname='shader.6cancel_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[5]="6"                                                                   
        return {'FINISHED'}

class SpecularCancel_Map(bpy.types.Operator): #seven                             
    bl_label="open"
    bl_idname='shader.7cancel_operator'

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        images_path[6]="7"                                                                  
        return {'FINISHED'}

#         final reg and unregis

classes=[Material,AlbedoCancel_Map,SpecularCancel_Map,NormalCancel_Map,HeightCancel_Map,ShaderMainPanel,MetallicCancel_Map,AmbientCancel_Map,RoughnessCancel_Map,Albedo_Map,Normal_Map,Roughness_Map,Ambient_Map,Metallic_Map,Height_Map,Specular_Map,MyProperties]   #need to add different maps names

def register():
    for clas in classes:
        bpy.utils.register_class(clas)
    bpy.types.Scene.my_tool=bpy.props.PointerProperty(type=MyProperties)

def unregister():
    for clas in classes:
         bpy.utils.unregister_class(clas)           
    del bpy.types.Scene.my_tool
    
if __name__ == "__main__":
    register()


    
