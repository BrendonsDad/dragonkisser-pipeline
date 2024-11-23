# Basic Outline
Welcome to the game pipeline! In this file, we will discuss the ins' and outs' of the pipe to get you rolling. As of (11/22/2024), when you open the skygaurd pipeline. You will be met with a layout that looks like this:

- .githooks
- pipeline
- venv
- .gitignore
- .gitmodules
- gitTips.md
- LICENSE
- pyproject.toml
- README.md
- Sky Designer.lnk
- Sky Painter.lnk
- Skya.lnk
- Skydini.desktop
- Skydini.lnk
- UNDERSTANDINGthePIPE.md

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

## Dungance Designer.