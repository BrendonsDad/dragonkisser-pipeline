from pathlib import Path, PureWindowsPath
from software.Unreal_Engine import asset_import_dependencies as dep
import tkinter
from tkinter import filedialog


root = tkinter.Tk() # } execute these lines once, to "initialise" tkinter
root.iconify()
def prompt_files():
    try:
        file_paths = filedialog.askopenfilenames()
        root.iconify()
    except tkinter.TclError: # this error was raised once or twice while testing, just in case return an empty list
        return []
    else:
        return file_paths
def stop_tk(): # call this when you're done selecting files, to stop tkinter from running mainloop in the background
    root.destroy()

def main():
    
    FBX_FORMAT_STR = {dep.STRTSTR:["SM"], dep.ENDSTR:[""]}
    FBX_FILETYPES = ["fbx"]
    FBX_IMPORT_HELPER_ID_STRING = dep.FUNC_ID_MODEL

    TEX_FORMAT_STR = {dep.STRTSTR:["T"], dep.ENDSTR:["Texture_Map", "BaseColor", "ORM", "Normal", "Emissive", "ORMG"]} #if something complains later, remove texture_map or fix error
    TEX_FILETYPES = ["png"]
    TEX_IMPORT_HELPER_ID_STRING = dep.FUNC_ID_TEXTURE

    SOURCE_DIRECTORY: Path = Path("G:\\skyguard\\prototypeAssets")
    DESTINATION_DIRECTORY:Path = Path("Y25\\Art\\Props")
    files_to_import = prompt_files()
    fbx_files = []
    fbx_offsrcc = []
    tex_files = []
    tex_offsrcc = []
    for file in files_to_import:
        ext = file.split(".").pop(-1).lower()
        if ext == "png":
            tex_files.append(Path(file))
            tex_offsrcc.append(Path(file).relative_to(SOURCE_DIRECTORY))
        if ext == "fbx":
            fbx_files.append(Path(file))
            fbx_offsrcc.append(Path(file).relative_to(SOURCE_DIRECTORY))

    print(fbx_files)
    print(fbx_offsrcc)
    print(tex_files)
    print(tex_offsrcc)
    
    for file, fbx_offsrc in zip(fbx_files, fbx_offsrcc):
        print("Attempting to fetch: {file}".format(file = str(PureWindowsPath(file))))
        filename_check = dep.check_format_of_filename(str(PureWindowsPath(file)), FBX_FORMAT_STR, FBX_FILETYPES, str(PureWindowsPath(fbx_offsrc)))
        print("filename_check_return value:", filename_check, sep="\n")
        if str(PureWindowsPath(file)):
            pop = dep.import_helper(filename_check, FBX_IMPORT_HELPER_ID_STRING)
            print("location 1", pop)
            if len(pop) < 2 or pop[0] is None or pop[1] is None:
                raise ValueError("")
        print("output of import_helper:" , pop)
        # newPath = "/".join(pop[1].replace("Game/", "").split("/")[:-1])
        # print(newPath, "np")
        # newName = pop[0].replace("SM_G:/skyguard/prototypeAssets", "").replace(newPath, "").replace("/", "")
        # print(newName, "nn\n\n\n")
        # newPath = "/Game" + newPath
        # print("parameters:", newName, newPath)
        newPath = "/".join(pop[1].split("/")[:-1])
        newName = pop[0]
        print("np: ", newPath)
        print("nn: ", newName)
        dep.create_mat_instances(newName, newPath)
        if filename_check is None:
            pass
   
    for file, tex_offsrc in zip(tex_files, tex_offsrcc):
        print("Attempting to fetch: {file}".format(file = str(PureWindowsPath(file))))
        filename_check = dep.check_format_of_filename(str(PureWindowsPath(file)), TEX_FORMAT_STR, TEX_FILETYPES, str(PureWindowsPath(tex_offsrc)))
        print("filename_check_return value:", filename_check, sep="\n")
        if str(PureWindowsPath(file)):
            pop = dep.import_helper(filename_check, TEX_IMPORT_HELPER_ID_STRING)
        if filename_check is None:
            pass
    stop_tk()

main()
