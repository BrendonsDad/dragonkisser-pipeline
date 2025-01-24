

from pipe.db import DB
from pipe.glui.dialogs import FilteredListDialog, MessageDialog
from env_sg import DB_Config
from shared.util import get_production_path
from os import listdir
from os.path import isfile
from pathlib import Path
from software.Unreal_Engine import asset_import_dependencies as dep
from Qt.QtWidgets import QApplication, QWidget

CHILD_MODE = DB.ChildQueryMode.ALL

def main():
    
    FBX_FORMAT_STR = {dep.STRTSTR:["SM"], dep.ENDSTR:[""]}
    FBX_FILETYPES = ["fbx"]
    FBX_IMPORT_HELPER_ID_STRING = dep.FUNC_ID_MODEL

    TEX_FORMAT_STR = {dep.STRTSTR:["T"], dep.ENDSTR:["Texture_Map", "BaseColor", "ORM", "Normal", "Emissive", "ORMG"]} #if something complains later, remove texture_map or fix error
    TEX_FILETYPES = ["png"]
    TEX_IMPORT_HELPER_ID_STRING = dep.FUNC_ID_TEXTURE
    app = QApplication.instance()
    if(app is None):
        app = QApplication([])
    root = QWidget()
    # root.show()
    root.closeEvent = lambda event: app.quit()
    _conn = DB.Get(DB_Config)
    
    fld = FilteredListDialog(root,
    _conn.get_asset_name_list(sorted=True, child_mode=CHILD_MODE),
    "Import Asset Via Association using ShotGrid:", "Select an asset group to import", accept_button_name = "Import")
    if not fld.exec():
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
    fbx_path = str(asset_path / f"{asset.name}.fbx")
    
    tex_assets_path:Path = get_production_path() / asset.tex_path
    tex_assets_stringpath_list = [str(tex_assets_path / f) for f in listdir(tex_assets_path) if isfile((tex_assets_path / f))]
    fbx_assets_stringpath_list = [str(get_production_path()/f for f in listdir(get_production_path()) if isfile(get_production_path()/f))]

    # print("Attempting to fetch: {fbx_path}".format(fbx_path = fbx_path))
    # filename_check = dep.check_format_of_filename(fbx_path, FBX_FORMAT_STR, FBX_FILETYPES, asset.path)  # replaced this section with a for loop version (to allow for multiple fbx files in a single import)
    # print(filename_check)
    # if asset_path is not None:
    
    #     if fbx_path:
    #         pop = dep.import_helper(filename_check, FBX_IMPORT_HELPER_ID_STRING)
    #         print(pop)
    #         if len(pop) < 2 or pop[0] is None or pop[1] is None:
    #             raise ValueError("")
    #         dep.create_mat_instances(pop[0], pop[1])
    #     if filename_check is None:
    #         print("Failed import. Check the naming convention?")

    filtered_fbx_stringpath_list = [x for x in fbx_assets_stringpath_list if ".fbx" in x]
    for oneFile in filtered_fbx_stringpath_list:
        print("Attempting to fetch: {oneFile}".format(oneFile = oneFile))
        filename_check = dep.check_format_of_filename(oneFile, FBX_FORMAT_STR, FBX_FILETYPES, asset.path)
        print("filename_check_return value:", filename_check, sep="\n")
        if oneFile:
            pop = dep.import_helper(filename_check, FBX_IMPORT_HELPER_ID_STRING)
            if len(pop) < 2 or pop[0] is None or pop[1] is None:
                raise ValueError("")
        dep.create_mat_instances(pop[0], pop[1])
        if filename_check is None:
            pass
   
    filtered_stringpath_list = [x for x in tex_assets_stringpath_list if ".png" in x]
    for oneFile in filtered_stringpath_list:
        print("Attempting to fetch: {oneFile}".format(oneFile = oneFile))
        filename_check = dep.check_format_of_filename(oneFile, TEX_FORMAT_STR, TEX_FILETYPES, asset.path + "/Textures")
        print("filename_check_return value:", filename_check, sep="\n")
        if oneFile:
            pop = dep.import_helper(filename_check, TEX_IMPORT_HELPER_ID_STRING)
        if filename_check is None:
            pass
    else:
        print("No file selected.")
        exit(0)



    # tex_file_paths TODO figure this out.
    
    pass

main()
