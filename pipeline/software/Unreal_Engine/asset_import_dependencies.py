import os
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import unreal
import pickle

MAMPATH = "/Game/EditorUtilities/M_AutoMaster"
ENDSTR = "end_options"
STRTSTR = "start_options"
FUNC_ID_MODEL = "model"
FUNC_ID_TEXTURE = "texture"
IMPORT_PICKLE_MESSAGE_1 = "Hi! This is either your first time running the script on this pc, or you've deleted a previous pkl file! We're going to walk you through how to get this set up again. \nTo explain a bit about what is happening, I need 2 folders given to me in order to help imports work smoothly. \n\nThe first folder I need is going to be the source folder, or where you want to import files from. Keep this in mind: If you want the files to be organized the same way as they were in your editor, you need to select the PARENT folder. \n\nExample: I have a folder ARTPROJECT, with folders inside named CHARACTERS and VEHICLES. What I am asking for is the folder ARTPROJECT. That way, when you upload files from the other two subfolders, the files will be automatically put into new folders with their respective subfolder names, CHARACTERS or VEHICLES."
IMPORT_PICKLE_MESSAGE_2 = "Sorry about the lengthy explanation. Anyways, I will now ask for: \n\n\nPARENT SOURCE FOLDER"




"""
Creates import tasks
"""
def build_import_tasks(filename: str, destination_name: str, destination_path: str, options):
    task = unreal.AssetImportTask()
    task.set_editor_property("automated", True)
    task.set_editor_property("destination_name", destination_name)
    task.set_editor_property("destination_path", destination_path)
    task.set_editor_property("filename", filename)
    task.set_editor_property("options", options)
    return task

"""
Import Option configuration
"""
def build_import_options(static_mesh_data, texture_data):
    options = unreal.FbxImportUI()
    if static_mesh_data is not None:
        options.set_editor_property('import_mesh', True)
        options.set_editor_property('import_as_skeletal', False)
        options.set_editor_property("static_mesh_import_data", static_mesh_data)
    if texture_data is not None:
        options.set_editor_property('import_textures', True)
        options.set_editor_property('import_materials', False)
        options.set_editor_property("texture_import_data", texture_data)
    return options

"""
Static mesh import options configuration
"""
def build_static_mesh_data():
    static_mesh_data = unreal.FbxStaticMeshImportData()
    static_mesh_data.set_editor_property("build_nanite", False)
    static_mesh_data.set_editor_property("convert_scene", True)
    static_mesh_data.set_editor_property("force_front_x_axis", True)
    static_mesh_data.set_editor_property("auto_generate_collision", True)
    return static_mesh_data

"""
Texture import options configuration
"""
def build_texture_data():
    master_mat_path = unreal.SoftObjectPath("/Game/EditorUtilities/M_AutoMaster")
    texture_data = unreal.FbxTextureImportData()
    texture_data.set_editor_property("base_material_name", master_mat_path)
    texture_data.set_editor_property("base_color_name", "BaseColor")
    texture_data.set_editor_property("base_emmisive_texture_name", "Emissive")
    texture_data.set_editor_property("base_normal_texture_name", "Normal")
    return texture_data

"""
Imports a static mesh
filepath: path on disk to static mesh you want to import
destination_name: the name you want to give the asset in engine
destination_path: the path in Unreal to import asset to
"""
def import_static_mesh(filepath: str, destination_name: str, destination_path: str):
    # Get all import options and build task
    static_mesh_data = build_static_mesh_data()
    texture_data = build_texture_data()
    import_options = build_import_options(static_mesh_data, texture_data)
    # TODO: get texture info and build more tasks for importing the textures
    #       remove texture import in FBX static mesh import itself
    task = build_import_tasks(filepath, destination_name, destination_path, import_options)

    # make directory if it doesn't exist yet
    eal = unreal.EditorAssetLibrary()
    if not eal.does_directory_exist(destination_path):
        eal.make_directory(destination_path)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])





#helper function for other 2 scripts.
def import_helper(fd, typea):
    if typea == FUNC_ID_TEXTURE:
        import_textures(fd[0], fd[1], fd[2])
    if typea == FUNC_ID_MODEL:
        import_static_mesh(fd[0], fd[1], fd[2])
    return (fd[1], fd[2])
"""
Imports textures
"""
def import_textures(filepath: str, destination_name: str, destination_path: str):
    static_mesh_data = None # compare build_static_mesh_data() Note: Modified b-i-o to accept none, and just not include those options if it is none.
    texture_data = build_texture_data() # What exactly does this do? Find out.
    
    import_options = build_import_options(static_mesh_data, texture_data)
    task = build_import_tasks(filepath, destination_name, destination_path, import_options)

    eal = unreal.EditorAssetLibrary()
    if not eal.does_directory_exist(destination_path):
        eal.make_directory(destination_path)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    asset_tools.import_asset_tasks([task])
    pass

"""
Create material instance for asset
"""
def create_mat_instance(mat_name: str, destination_path: str):
    eal = unreal.EditorAssetLibrary()
    parent_mat = eal.load_asset(MAMPATH)
    if parent_mat == None:
        print("Error: Auto Texturer Master Material not found." +
              "Make sure AutoMatWidget directory is in the Content folder.")
    
    # create material instance if it doesn't exist
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    if eal.does_asset_exist(f"{destination_path}/{mat_name}"):
        print("MI already created")
        mat_asset_data = eal.find_asset_data(f"{destination_path}/{mat_name}")
        mat_inst = mat_asset_data.get_asset()

    else:
        try:
            mat_inst = asset_tools.create_asset(mat_name, destination_path, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        except:
            print("Error creating material")
            return

    mat_inst.set_editor_property("parent", parent_mat)
    return mat_inst



def check_format_of_filename(filepath, format, filetype, asset_path):
    print("beginning of checkformatoffilename")
    splitpath= filepath.split(".")
    path = ".".join(splitpath[:-1]) # all but the last one
    extension = splitpath[-1]
    if extension not in filetype:
        return None
    print("path:", path, sep=" ")
    filename = path.split("\\")[-1]
    print("filename:", filename, sep=" ")
    path = path.split("\\")[:-1] #removes the filename, which we have now extracted
    path = "\\".join(path)
    print("path:", path, sep=" ")
    name_pieces = filename.split("_")
    print(name_pieces)
    #format = {STRTSTR:"T_", ENDSTR:["BaseColor", "ORM", "Normal", "Emissive"]}
    if name_pieces[0] not in format[STRTSTR]:
        name_pieces.insert(0, format[STRTSTR][0])
    if name_pieces[-1] not in format[ENDSTR]:
        name_pieces.append(format[ENDSTR][0])
    print(name_pieces)
    destination_name = "_".join(name_pieces)
    destination_path = calculate_destination_path(asset_path, "/Game/")
    print("end of checkformatoffilename:", filepath, destination_name, destination_path, sep="\n")
    return filepath, destination_name, destination_path


def calculate_destination_path(relativep, ueconst):
    return ueconst + relativep

"""
Creates a material instance for each material slot
in a static mesh.
asset_name: name of the static mesh in unreal (NO FILE EXTENSION)
asset_dir: directory the asset is found in
"""
def create_mat_instances(asset_name: str, asset_dir: str):
    # get asset from editor
    eal = unreal.EditorAssetLibrary()
    asset_data = eal.find_asset_data(f"{asset_dir}/{asset_name}")
    print(f"{asset_dir}/{asset_name}")
    asset = asset_data.get_asset()

    destination_path = asset_dir + "/Textures"
    mat_instances = [] 

    # create Material Instances for each material slot
    for material_slot in asset.static_materials:
        mat_name = "MI_" + str(material_slot.material_slot_name)
        mat_inst = create_mat_instance(mat_name, destination_path)
        mat_instances.append(mat_inst)

#import_static_mesh("H:/Desktop/manny_lambert.fbx", "SM_MannyLambert", "/Game/TestManny_Lambert")
#create_mat_instances("manny_blinn", "/Game/TestManny")

"""
NOTE:
All the parts are there!!! The build functions are good the way they are (but double check build_texture_data())
Just tested putting in a mesh with multiple shading groups while having material imports disabled, and the groups
import correctly. meaning the slots still exist.
TODO:
- import textures
- integrate with shotgrid to get paths etc.
- change names for assets in pipeline to follow UE5 naming conventions
"""
