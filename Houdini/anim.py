# ** 수정 예정인 파일
# material 색상변경, anim 추가 까지

import hou

def Obj():

    #create node, obj, geo
    obj = hou.node("/obj")
    
    gap = 3
    
    # create obj node to list
    for i in range(3):
        myGeo = obj.createNode('geo', 'myGeo')
        myGeo.setPosition(hou.Vector2(i * gap, 0)) # set position node (not geo)
        myGeo.parmTuple('t').set([5 * (i+0), 0, 0])
        
        sphere = myGeo.createNode('sphere', 'mySphere')
            
        # scale * 2
        if myGeo:
            scale_parm = myGeo.parm("scale")
            scale = scale_parm.eval()
            new_scale = scale * 2.0
            scale_parm.set(new_scale)
        else:
            print("No Selected")
            
    # name_change
    for i in obj.children():
        name = i.name()
        prefix = 'New_'
        fullName = f'{prefix}{name}'
        upper_name = fullName.upper()
       
        i.setName(upper_name)
        print(name)
        
    # material (principledshader 적용)
    mat_node = hou.node("/mat").createNode("principledshader")
    
    for i in obj.children():
        i.parm("shop_materialpath").set(mat_node.path()) # use for loop
    
def save():
    hou.hipFile.save("Test.hip")
            
Obj()
save()
