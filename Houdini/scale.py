# 0424

# scale * 2
import hou

# 후디니 노드를 가져옴
node = hou.selectedNodes()

if node:
    scale_parm = node[0].parm("scale")
    scale = scale_parm.eval()
    new_scale = scale * 2.0
    scale_parm.set(new_scale)
    
else:
    print("No Selected")
