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
        selectedObjs = context.selected_objects
        group = bpy.data.groups
        groupMap = group.keys()
        exportPrefabData = []
        
        selectedGroups = []
        
        #gather list of groups selected
        for groupName in groupMap:
            for obj in selectedObjs:
                if(obj.name in group[groupName].objects and groupName not in selectedGroups):
                    selectedGroups.append(groupName)
        
        #create prefab data structure            
        for g in selectedGroups:
            prefab = {"id": g, "part":[], "kind":"PREFAB", "props":{}}
            #prefab props:
            for prop in group[g].keys():
                prefab['props'][prop] = group[g][prop]
            for obj in group[g].objects:
                obType = getTypeName(obj);
                prefab['part'].append({"id":obj.name,"kind":obType}) 
            #TODO - replace with file write
            print(prefab)         
        
        print("Exporting prefab...")

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
    #define if it is a prefab or just a mesh
    obType = 'PREFAB' if (obj.type == 'EMPTY' and obj.dupli_group) else obj.type
    return obType
        
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