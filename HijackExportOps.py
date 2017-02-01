import bpy
import json

c = bpy.context

##Exports json for mesh data for all selected objects, creating a separate file for each
class ExportJsonMesh(bpy.types.Operator):
    """Mesh Export"""
    bl_idname = "hijack.mesh_export"
    bl_label = "Export Mesh Hijack"
    def execute(self, context):
        print("Exporting Mesh...")
        selectedObjs = context.selected_objects
        exportObjData = []
        for x,obj in enumerate(selectedObjs):
            if(obj.type == "MESH"):
                exportObjData.append({"id":obj.name,"kind": getTypeName(obj)})
                selObjVerts = obj.data.vertices
                exportVertData = []
                for vert in selObjVerts:
                    exportVertData.append({
                    "x":vert.co.x,
                    "y":vert.co.y,
                    "z":vert.co.z})
                
                    exportObjData[x]['vertices'] = exportVertData
                print(json.dumps(exportObjData))
            else:
                print("Not of Mesh type.")
        return {'FINISHED'}
        
class ExportJsonPrefab(bpy.types.Operator):
    """Prefab Export"""
    bl_idname = "hijack.prefab_export"
    bl_label = "Export Prefab Hijack"
    
    def execute(self, context):
        #export name:
        #components[]
        #children
            #name:
            #components[
                #type:
                #meshId: path/to/resource
            #]
            #position: x,y,z
            #rot: w,x,y,z
            #scale: x,y,z
        
#check what type of obj it is:
        prefabData = []
        selectedObjects = bpy.context.selected_objects
        for obj in selectedObjects:
            if getTypeName(obj) == 'PREFAB':
                aPrefab = {"name":obj.name}
                aPrefab['components'] = getComponents(obj)
                prefabChildren=[]
                for child in obj.children:
                    childobj = {"name":child.name,"components": getComponents(child.data), "pos": [child.location.x, child.location.y, child.location.z], "rot": [child.rotation_quaternion.w, child.rotation_quaternion.x, child.rotation_quaternion.y, child.rotation_quaternion.z], "scale": [child.scale.x, child.scale.y, child.scale.z]}
                    try:
                        childobj['components'].append({"meshId": child.data.library.filepath})
                    except:
                        print("mesh is not linked")
                        path = bpy.data.filepath
                        if(not bpy.data.is_saved):
                            raise ValueError("non linked mesh comes from current file which has not been saved yet. Try saving and rerunning the exporter.")
                        childobj['components'].append({"meshId":path})
                    prefabChildren.append(childobj)
                aPrefab['children'] = prefabChildren
                prefabData.append(aPrefab)
        
        print("Exporting prefab...")
        print(json.dumps(prefabData))
        return {'FINISHED'}
    
class ExportJsonScene(bpy.types.Operator):
    """Prefab Export"""
    bl_idname = "hijack.scene_export"
    bl_label = "Export Scene Hijack"
    
    def execute(self, context):
        print("Exporting scene...")
        sceneData = {"id": c.scene.name, "kind":"SCENE", "actors": []}
        for i in c.scene.objects:
            obType = getTypeName(i)
            sceneData['actors'].append({"id":i.name, "kind":obType})
        print(sceneData)
        
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
    return components        

def register():
    bpy.utils.register_class(ExportJsonMesh)
    bpy.utils.register_class(ExportJsonPrefab)
    bpy.utils.register_class(ExportJsonScene)

def unregister():
    bpy.utils.unregister_class(ExportJsonMesh)
    bpy.utils.unregister_class(ExportJsonPrefab)
    bpy.utils.unregister_class(ExportJsonScene)

if __name__ == "__main__":
    register()

