class dep:
    from tkinter import messagebox
    

    MAMPATH = "/Game/EditorUtilities/M_AutoMaster"
    ENDSTR = "end_options"
    STRTSTR = "start_options"
    FUNC_ID_MODEL = "model"
    FUNC_ID_TEXTURE = "texture"
    
    def PromptSourceFolder(self, filename: str, filename_check, paths):
        IMPORT_PICKLE_MESSAGE_1 = "Hi! This is either your first time running the script on this pc, or you've deleted a previous pkl file! We're going to walk you through how to get this set up again. \nTo explain a bit about what is happening, I need 2 folders given to me in order to help imports work smoothly. \n\nThe first folder I need is going to be the source folder, or where you want to import files from. Keep this in mind: If you want the files to be organized the same way as they were in your editor, you need to select the PARENT folder. \n\nExample: I have a folder ARTPROJECT, with folders inside named CHARACTERS and VEHICLES. What I am asking for is the folder ARTPROJECT. That way, when you upload files from the other two subfolders, the files will be automatically put into new folders with their respective subfolder names, CHARACTERS or VEHICLES."
        IMPORT_PICKLE_MESSAGE_2 = "Sorry about the lengthy explanation. Anyways, I will now ask for: \n\n\nPARENT SOURCE FOLDER"
        from tkinter.filedialog import askdirectory
        import os

        import unreal
        import pickle
        from tkinter import messagebox

        messagebox.showinfo("Pickle Not Found:", IMPORT_PICKLE_MESSAGE_1)
        messagebox.showinfo("Pickle Not Found:", IMPORT_PICKLE_MESSAGE_2)
        # Note: Do we want to make it so that it does this by deleting everything outside of a keyword folder?
        while filename_check == False and filename:
            filename = askdirectory(title="Pick Source Directory") 
        # opendialogbox. choose file of filetype given and other options
            if filename:
                print("Attempting to fetch: {filename}".format(filename = filename))
                filename_check = os.path.exists(filename)
            if filename_check == False:
                print("Failed file selection. Exiting...")
        if filename:
            paths.append(filename)
            filename_check = False
            filename = "Empty"
            initialdir = os.path.expanduser('~/Documents')#unreal.EditorUtilityLibrary.get_current_content_browser_path()
            print(initialdir)
        else:
            messagebox.showerror("sorry", "We need these directories to run properly. Maybe I'll make it not needed in the future, but for now, they are neccesary.")
            return False
        paths.append("/Game")
        with open("mipickle.pk", 'wb') as fi:
            pickle.dump(paths, fi)
        return True


    """
    Creates import tasks
    """
    def build_import_tasks(self, filename: str, destination_name: str, destination_path: str, options):
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
    def build_import_options(self, static_mesh_data, texture_data):
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
    def build_static_mesh_data(self):
        static_mesh_data = unreal.FbxStaticMeshImportData()
        static_mesh_data.set_editor_property("build_nanite", False)
        static_mesh_data.set_editor_property("convert_scene", True)
        static_mesh_data.set_editor_property("force_front_x_axis", True)
        static_mesh_data.set_editor_property("auto_generate_collision", True)
        return static_mesh_data

    """
    Texture import options configuration
    """
    def build_texture_data(self):
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
    def import_static_mesh(self, filepath: str, destination_name: str, destination_path: str):
        # Get all import options and build task
        static_mesh_data = self.build_static_mesh_data()
        texture_data = self.build_texture_data()
        import_options = self.build_import_options(static_mesh_data, texture_data)
        # TODO: get texture info and build more tasks for importing the textures
        #       remove texture import in FBX static mesh import itself
        task = self.build_import_tasks(filepath, destination_name, destination_path, import_options)

        # make directory if it doesn't exist yet
        eal = unreal.EditorAssetLibrary()
        if not eal.does_directory_exist(destination_path):
            eal.make_directory(destination_path)

        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        asset_tools.import_asset_tasks([task])
    #helper function for other 2 scripts.
    def import_helper(self, fd, typea):
        if typea == self.FUNC_ID_TEXTURE:
            self.import_textures(fd[0], fd[1], fd[2])
        if typea == self.FUNC_ID_MODEL:
            self.import_static_mesh(fd[0], fd[1], fd[2])
        return (fd[1], fd[2])
    """
    Imports textures
    """
    def import_textures(self, filepath: str, destination_name: str, destination_path: str):
        static_mesh_data = None # compare build_static_mesh_data() Note: Modified b-i-o to accept none, and just not include those options if it is none.
        texture_data = self.build_texture_data() # What exactly does this do? Find out.
        
        import_options = self.build_import_options(static_mesh_data, texture_data)
        task = self.build_import_tasks(filepath, destination_name, destination_path, import_options)

        eal = unreal.EditorAssetLibrary()
        if not eal.does_directory_exist(destination_path):
            eal.make_directory(destination_path)

        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        asset_tools.import_asset_tasks([task])
        pass

    """
    Create material instance for asset
    """
    def create_mat_instance(self, mat_name: str, destination_path: str):
        eal = unreal.EditorAssetLibrary()
        parent_mat = eal.load_asset(self.MAMPATH)
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

    def calculate_destination_path(self, original_filepath):
        import pickle
        with open("mipickle.pk", 'rb') as fi:
            constants = pickle.load(fi)
        source_folder_const = constants[0]
        new_filepath = original_filepath.replace(source_folder_const, '')
        new_filepath = constants[1] + new_filepath # 0 is source main folder, 1 is game folder in UE.
        return new_filepath

    def check_format_of_filename(self, filepath, format, filetype):
        splitpath= filepath.split(".")
        path = ".".join(splitpath[:-1]) # all but the last one
        extension = splitpath[-1]
        if extension not in filetype:
            return None
        filename = path.split("/")[-1]
        path = path.split("/")[:-1] #removes the filename, which we have now extracted
        path = "/".join(path)
        name_pieces = filename.split("_")
        #format = {STRTSTR:"T_", ENDSTR:["BaseColor", "ORM", "Normal", "Emissive"]}
        if name_pieces[0] not in format[self.STRTSTR]:
            name_pieces.insert(0, format[self.STRTSTR][0])
        if name_pieces[-1] not in format[self.ENDSTR]:
            name_pieces.append(format[self.ENDSTR][0])
        destination_name = "_".join(name_pieces)
        destination_path = self.calculate_destination_path(path)
        return filepath, destination_name, destination_path




    """
    Creates a material instance for each material slot
    in a static mesh.
    asset_name: name of the static mesh in unreal (NO FILE EXTENSION)
    asset_dir: directory the asset is found in
    """
    def create_mat_instances(self, asset_name: str, asset_dir: str):
        # get asset from editor
        eal = unreal.EditorAssetLibrary()
        asset_data = eal.find_asset_data(f"{asset_dir}/{asset_name}")
        asset = asset_data.get_asset()

        destination_path = asset_dir + "/Textures"
        mat_instances = []

        # create Material Instances for each material slot
        for material_slot in asset.static_materials:
            mat_name = "MI_" + str(material_slot.material_slot_name)
            mat_inst = self.create_mat_instance(mat_name, destination_path)
            mat_instances.append(mat_inst)

    pass




from pipe.db import DB
from pipe.glui.dialogs import FilteredListDialog, MessageDialog
from env_sg import DB_Config
from shared.util import get_production_path
from os import listdir
from os.path import isfile
from pathlib import Path
# from . import asset_import_dependencies as dep
import unreal
from Qt.QtWidgets import QWidget


FBX_FORMAT_STR = {dep.STRTSTR:["SM"]}
FBX_FILETYPES = ["fbx"]
FBX_IMPORT_HELPER_ID_STRING = dep.FUNC_ID_MODEL


TEX_FORMAT_STR = {dep.STRTSTR:["T"], dep.ENDSTR:["Texture_Map", "BaseColor", "ORM", "Normal", "Emissive", "ORMG"]} #if something complains later, remove texture_map or fix error
TEX_FILETYPES = ["png"]
TEX_IMPORT_HELPER_ID_STRING = dep.FUNC_ID_TEXTURE

root = QWidget()
def main():

    print("hello")
    return
    _conn = DB.Get(DB_Config)
    start = MessageDialog(root, "Welcome aboard! You meant to import a fully built asset, yes?", "Begin Import?", has_cancel_button=True).exec_()
    if (not start):
        return
    
    fld = FilteredListDialog(root,
    _conn.get_asset_name_list(sorted=True),#note:child_mode might be neccesary. 
    "Import Asset Via Association using ShotGrid:", "Select an asset group to import", accept_button_name = "Import")
    if not fld.exec_():
        return
    item = fld.get_selected_item()
    if item is None:
        start = MessageDialog(root, "No asset selected. Cancelling Import", "Null Asset",).exec_()
        return
    
    asset = _conn.get_asset_by_name(item)
    try:
        assert asset is not None
        assert asset.path is not None
    except AssertionError:
        
        return

    asset_path = get_production_path() / asset.path
    fbx_path = asset_path / f"{asset.name}.fbx"
    tex_assets_path:Path = get_production_path() / asset.tex_path
    tex_assets_smlist = [tex_assets_path / f for f in listdir(tex_assets_path) if isfile((tex_assets_path / f))]

    print("Attempting to fetch: {fbx_path}".format(fbx_path = fbx_path))
    filename_check = dep.check_format_of_filename(fbx_path, FBX_FORMAT_STR, FBX_FILETYPES)
    if asset_path != "":
    
        if fbx_path:
            pop = dep.import_helper(filename_check, FBX_IMPORT_HELPER_ID_STRING)
            dep.create_mat_instances(pop[0], pop[1])
        if filename_check is None:
            print("Failed import. Check the naming convention?")

        for oneFile in tex_assets_smlist:
            print("Attempting to fetch: {oneFile}".format(oneFile = oneFile))
            filename_check = dep.check_format_of_filename(oneFile, TEX_FORMAT_STR, TEX_FILETYPES)
            if oneFile:
                pop = dep.import_helper(filename_check, TEX_IMPORT_HELPER_ID_STRING)
                dep.create_mat_instances(pop[0], pop[1])
            if filename_check is None:
                pass
    else:
        print("No file selected.")
        exit(0)



    # tex_file_paths TODO figure this out.
    
    pass

# main()