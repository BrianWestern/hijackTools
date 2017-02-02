import bpy
import json

c = bpy.context
BASE_DIR = "/home/brian/hijackTools/hijackTools/assets"
PREFAB_DIR = "/prefabs"
       
class AddPrefab(bpy.types.Operator):
    bl_label = "add a prefab"
    bl_idname = "objects.add_prefab"
    prefabCount = 0
    
    def execute(self, context):
        #create empty
        self.prefabCount += 1
        uniqueName = "prefab_%d" %self.prefabCount
        newPrefab = bpy.data.objects.new(uniqueName, None)
        newPrefab['components'] = []
        newPrefab['type'] = 'PREFAB'
        
        c.scene.objects.link(newPrefab)
        
        return {'FINISHED'}
 
class ExportJsonPrefab(bpy.types.Operator):
    """Prefab Export"""
    bl_idname = "hijack.prefab_export"
    bl_label = "Export Prefab Hijack"
    
    def execute(self, context):
        print(json.dumps(getPrefabData(bpy.context.selected_objects[0])))
        return {'FINISHED'}
    
def getTypeName(obj):
    if 'type' in obj.keys():
        return obj['type']
    else:
        return obj.type

def getComponents(obj):
    components = []
    #convert from blenders IDPropertyGroup data structure
    if 'components' in obj.keys():
        for i in obj['components']:
            components.append({i:obj['components'][i]})
    ### blender object components
    curObjType = getTypeName(obj)
    aComponent = {"type": curObjType}
    if(curObjType == 'MESH'):
        aComponent['blendPath'] = bpy.path.relpath(getFilePath(obj), start=BASE_DIR)
    elif(curObjType == 'PREFAB'):
        aComponent['prefabId'] = PREFAB_DIR 
    components.append(aComponent)
    

    return components        

def getPrefabData(obj):
    if getTypeName(obj) == 'PREFAB':
        aPrefab = {"name":obj.name}
        aPrefab['components'] = getComponents(obj)
        prefabChildren=[]
        for child in obj.children:
            childobj = {"name":child.name,"components": getComponents(child), "pos": [child.location.x, child.location.y, child.location.z], "rot": [child.rotation_quaternion.w, child.rotation_quaternion.x, child.rotation_quaternion.y, child.rotation_quaternion.z], "scale": [child.scale.x, child.scale.y, child.scale.z]}
            prefabChildren.append(childobj)
        aPrefab['children'] = prefabChildren
    return aPrefab

#def importPrefab(blendFilePath, jsonFilePath):
    #create an empty
    #set load children
    #set component properties

def getFilePath(obj):
    #for linked file:
    fpath = ""
    try:
        fpath = obj.data.library.filepath
    except:
        if bpy.data.is_saved:
            fpath = bpy.data.filepath
        else:
            raise ValueError("A resource that is being exported needs to first be saved.  Please save this blend file and try again.all")
    return fpath

def register():
    bpy.utils.register_class(ExportJsonPrefab)
    bpy.utils.register_class(AddPrefab)

def unregister():
    bpy.utils.unregister_class(ExportJsonPrefab)
    bpy.utils.unregister_class(AddPrefab)

if __name__ == "__main__":
    register()
