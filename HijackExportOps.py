import bpy
import os
import json

#convienience variable
c = bpy.context

CONFIG_DIR = "./config.json"

#These varaibles are setup in the config file located  in the above directory
BASE_DIR = ""
PREFAB_DIR = ""
       
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
        prefabData = getPrefabData(bpy.context.selected_objects[0])
        output = json.dumps(prefabData)
        print(output)
        jsonFilePath = "%s%s/%s.json" %(BASE_DIR, PREFAB_DIR, prefabData['name'])
        print(jsonFilePath)
        outFile = open(jsonFilePath, 'w+')
        outFile.write(output)
        outFile.close()
        
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
        obj.rotation_mode = 'QUATERNION'
        aPrefab['pos'] = [obj.location.x, obj.location.y, obj.location.z]
        aPrefab['rot'] = [obj.rotation_quaternion.w, obj.rotation_quaternion.x, obj.rotation_quaternion.y, obj.rotation_quaternion.z]
        aPrefab['scale'] = [obj.scale.x, obj.scale.y, obj.scale.z]
        aPrefab['components'] = getComponents(obj)
        prefabChildren=[]
        for child in obj.children:
            child.rotation_mode = 'QUATERNION'
            childobj = {"name":child.name,"components": getComponents(child), "pos": [child.location.x, child.location.y, child.location.z], "rot": [child.rotation_quaternion.w, child.rotation_quaternion.x, child.rotation_quaternion.y, child.rotation_quaternion.z], "scale": [child.scale.x, child.scale.y, child.scale.z]}
            prefabChildren.append(childobj)
        aPrefab['children'] = prefabChildren
    return aPrefab

#def importPrefab(blendFilePath, jsonFilePath):
    #create an empty
    #set load children
    #set component properties

def loadConfig():
    configDataStr = ""
    with open(CONFIG_DIR, 'r') as f:
        for line in f:
            configDataStr += line
    configData = json.loads(configDataStr)
    global BASE_DIR
    global PREFAB_DIR
    PREFAB_DIR = configData['exportConfig']['PREFAB_DIR']    
    BASE_DIR = configData['exportConfig']['BASE_DIR']

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
    loadConfig()

def unregister():
    bpy.utils.unregister_class(ExportJsonPrefab)
    bpy.utils.unregister_class(AddPrefab)

if __name__ == "__main__":
    register()
