"""CURRENT BLOCK: MODULENOTFOUNDERROR: NO MODULE NAMED 'attrs'. NOTE TO SELF: FIND OUT WHY THIS IS HAPPENING AND FIX IT"""





from pipe.db import DB
from pipe.glui.dialogs import FilteredListDialog, MessageDialog
from pipe.sp.local import get_main_qt_window
from env_sg import DB_Config
from shared.util import get_production_path
import hou
from os import listdir
from os.path import isfile
from pathlib import Path
import asset_import_dependencies as dep


FBX_FORMAT_STR = {dep.STRTSTR:["SM"]}
FBX_FILETYPES = ["fbx"]
FBX_IMPORT_HELPER_ID_STRING = dep.FUNC_ID_MODEL


TEX_FORMAT_STR = {dep.STRTSTR:["T"], dep.ENDSTR:["Texture_Map", "BaseColor", "ORM", "Normal", "Emissive", "ORMG"]} #if something complains later, remove texture_map or fix error
TEX_FILETYPES = ["png"]
TEX_IMPORT_HELPER_ID_STRING = dep.FUNC_ID_TEXTURE


def main():
    _conn = DB.Get(DB_Config)
    start = MessageDialog(get_main_qt_window(), "Welcome aboard! You meant to import a fully built asset, yes?", "Begin Import?", has_cancel_button=True).exec_()
    if (not start):
        return
    
    fld = FilteredListDialog(get_main_qt_window(),
    _conn.get_asset_name_list(sorted=True),#note:child_mode might be neccesary. 
    "Import Asset Via Association using ShotGrid:", "Select an asset group to import", accept_button_name = "Import")
    if not fld.exec_():
        return
    item = fld.get_selected_item()
    if item is None:
        start = MessageDialog(get_main_qt_window(), "No asset selected. Cancelling Import", "Null Asset",).exec_()
        return
    
    asset = _conn.get_asset_by_name(item)
    try:
        assert asset is not None
        assert asset.path is not None
    except AssertionError:
        hou.ui.displayMessage(
            "The asset you are trying to load does not have a path set in ShotGrid. Please let a Lead know",
            buttons=("OK"),
            severity=hou.severityType.ImportantMessage,
        )
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

main()