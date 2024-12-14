# Basic Outline
Welcome to the game pipeline! In this file, we will discuss the ins' and outs' of the pipe to get you rolling. As of (11/22/2024), when you open the skygaurd pipeline. You will be met with a layout that looks like this:

* .githooks
* pipeline
* venv
* .gitignore
* .gitmodules
* gitTips.md
* LICENSE
* pyproject.toml
* README.md
* Sky Designer.lnk
* Sky Painter.lnk
* Skya.lnk
* Skydini.desktop
* Skydini.lnk
* UNDERSTANDINGthePIPE.md

Lets take a look at each of these real quick.

## .githooks
The folder for scripts to be run as git hooks (ie pre-commit, post-checkout, etc)

What is the purpose of a .githooks file? Git hooks are scripts that run automatically every time a particular event occurs in a Git repository. They let you customize Git's internal behavior and trigger customizable actions at key points in the development life cycle. For example, you can create them so that everytime you commit changes on your branch/repo, a githook could block that commit if it does not reach certain preset standards. You can also set it so that you can trigger another hook before pushing if again your push does not pass the requirements you set, therefore preventing them from leaving and entering your remote repository if that hook fails. In fact, three githoks that come up the most often are pre-commit, pre-push, and pre-recieve. Inour case, we have pre-commit, post-checkout, setup-env, and shotgun.pyi. Your githooks can be written in any language. The .githooks directory helps with the following:
- Organization: It provides a centralized Loacation to store and manage all Git hooks for a project, making them easier to find, edit and maintain.
- Clarity: It clearly seperates Git hooks from other project files, improving code organization and readability. 
- Best Practices: It aligns with common git practices and helps enforce oding standards and autmated checks. 

## pipeline
All the hte code.

This is where you will most likely spend the majority of your time. There is ALOT in the pipeline, so this area will get a more indepth look further down. For now, just understand that it contains (among others) two big directories, pipe and software. This is where a lot of your coding will be. 

## venv
Site-specific things that we don't want committed to the git repo, including where all of our software is installed. 

A venv directory, short for "virtual enviornment," is a self-contained directory that isolates a specific Python installation and its associated packages from the system wide Python installation. This isolation is crucial for managing different Python projects with varying dependencies without conflicts. 

## .gitignore
Files hat we do not want to be committed to the git repo, either for security reasons or becuase they are transient files that get regenerated automatically.

A .gitignore file is a text file that tells Git which files and directories to ignore when committing changes to your repository. This is crucial for maintaining a clean and efficient Git repository. You can either explicity list files that you want hidden, or you can use patterns.
Common patterns to look for:
- Specific file names: file.txt
- File extensions: *.log
- Directories: build/

For example, in our file we have '*.tex' which ignores all files ending with '.tex'

*Important Note*
- If a file is already tracked by Git, adding it to .gitignore will not automatically ignore it. You'll need to use git rm --chached <filename> to remove it from the staging area and then add it to .gitignore.

By effectively using a .gitignore file, you can maintain a well-organized, secure, and efficient pipe.

## .gitmodules
All our submodules

A submodule is a git repository within another git repository. It is a great way to add an existing repository as a submodule to your repo. Not only is it a reference to the repo, it is a reference to a specific commit in the repo. This helps with modular development becuase it breaks down large projects into smaller, more manageable submodules.

So how does it work?
- Submodule Initialization: When you add a submodule to your project, Git creates a .gitmodules file.
- Submodule Configuration: This file stores information about each submodule, indluding its path, URL, and commit hash

Structure:
[submodule "submodule name"]
    path = submodule_path
    url = git@github.com:username/repository.git      #  this can be https as well

* Path: Where the submodule files reside in your project
* URL: Location of the external repository

## gitTips.md
An md file which contains git commands that future TDs might find helpful.
Feel free to add to this. (Well, feel free to edit any of these, with mindfulness of course.)

## LICENSE
The open-source license that the project is under. Just leave this where it is.

## pyproject.toml
Configuration for 

## README.md
Front page on the github. Good for developer documentation. 

## Sky Designer.lnk
The link that goes to Substance Designer, custumized for the film use and forked for the game (with minor edits)

## Sky Painter.lnk
The link that goes to Substance Painter, custumized for the game.

## Skya.lnk
The link that goes to Maya, custumized for the game.

## Skydini.desktop and Skydini.lnk
As you can see, there are both Skydini.desktop and Skydini.lnk. You might be wonder what the purpose of the desktop file is. 
### Houdini.lnk
* **Windows Shortcut:** This is typically a Windows shortcut file, used to point to the executable file of Houdini. 
* **Purpose:** It provides a convenient way to launch Houdini directly from the desktop or other locations
* **Functionality:** Double-clicking this shortcut triggers the execution of the Houdini application.
### Houdini.desktop:
* **Linux Desktop Entry:** This file is specific to Linux-based systems and is used to create desktop entries
* **Purpose:** it allows the integration of applications into te desktop enviornment including the ability to lauch the application from the menud, dock, or other places. 
* **Functionality:** It defines various properties of the application, such as the name, icon, command to execute, and working directory.
### Why Two Links?
The reason for having both links is to cater to different operating systems.
* **Windows:** Uses .lnk files for shortcuts
* **Linux:** Uses .desktop files for desktop entries
By having both, the pipeline code can ensure compatibility across different platforms.


## UNDERSTANDINGthePIPE.md
The file you are reading right now. Meant to provide comprehensive documentation for people on boarding. (Or just with general questions). Feel free to edit this if you can add changes that would be beneficial to those trying to learn how to use and add to and edit the game pipeline code. 


Okay, So that is the basic skeleton! Let's dig a little deeper and dive into the pipeline folder

# The pipeline folder
Opening up the pipeline folder, we are again met with a variety of directories (folders) and files.

* _pycache_
    * pycache should not be added to get. It's a bunch of compiled python files. each time you start up a python instance (or DCC), the first time you call a python file, if the .py file is more recent than the last _pycache_ the python code will be recompiled
* lib
    * This is a bunch of miscellaneous stuff, mostly third-party code. Not very well organized at the moment.
* pipe
    * Python module for code that is imported and run from the DCC.
    * We will take a deeper dive into this folder.
* shared
    * Utilities used by 'pipe' and 'software' modules.
* software
    * Module called by '__main__.py' to initialize environments and launch DCCS
    * This is where most of your personal code will be. You will build pluggins here.
    * We will take a deeper dive into this folder as well.
* _init_.py
    * In Python, the __init__.py file serves a crucial role in defining packages and modules. While it might appear empty or contain minimal code, its presence signifies to Python that a directory should be treated as a package.
    * What is a package? A package is a collection of modues organized hierarchically within a directory structure. It allows you to structure your code efficiently, especially for larger projects. 
    * This allows you to import modules from within that package using the dot notation.
    * Our's is empty at the moment, but it still plays an important role in communicating to the interpreter that this directory contains modules. 
* _main_.py
    * The file __main__.py serves two distinct purposes in Python:
    * Top-level Script Execution: When you run any python script directly, the script itself becomes the __main__ module.
    * Any Code written directly in the script executes within the __main__ scope. 
    * This is useful for standalone scripts that have thier own entry point
    * Using __main__.py ensures automatic execution when running the script or package appropriately. 
    * In essense, use __main__.py for the main script or package entry point. This is preffered and its execution is automatic when running the script. 
* env_sg.py
    * Contains the authentication information for the BYU shotgrid instance. This is equivalent to a username and password and should not be added to git.
* env.py
    * Various environment parameters that we don't want to be committed and//or related to the specific setup of the BYU image, so we want them as enviornment parameters so that this could in theory work at another studio. 
* env.py.md
    * Documentation for env.py, might be out of date. 

Again, the most important folder to understand is the software folder. We will now briefly take a look at the pipe folder, and then we will take a deep dive into software. 

# The pipeline/pipe folder 
Upon opening the pipe folder, we see a handful of condensly named directories, and a few files.
* db
* glui
* h
* m
* sp
* struct
* u
* __init__.py
* textconverter.py
* util.py

Upon observation, it becomes obvious that these are folders for our dccs. We will explore db, textconverter.py and util.py.
* textconverter.py:
    * This is as the name suggests, a file that converts png files into tex files.
* util.py
    * This code defines several utilities for managing modules and subprocesses.
    * After our imports, the code creates the dotdict class. 
    * dotdict class inhertis from dict and provides dot notation access to dictionary attributes. 
    * It overrides getattr, setattr, and delattr methods to allow accessing keys and values using dotnotation. (e.g., obj.key instead of obj['key'])

* def dict_index(d: dict[KT, VT], V: VT) ->:
    * This function takes a dictionary and a value as argruments. 
    * It returns the key associated with the given value in the dictionary. This is essentially a way to find the key for the specific value within a dictionary. 
    *