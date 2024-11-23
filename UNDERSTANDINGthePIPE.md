# Basic Outline
Welcome to the game pipeline! In this file, we will discuss the ins' and outs' of the pipe to get you rolling. As of (11/22/2024), when you open the skygaurd pipeline. You will be met with a layout that looks like this:

- .githooks
- pipeline
- venv
- .gitignore
- .gitmodules
- Dungance Designer.Lnk
- Dungini.desktop
- Dungini.lnk
- gitTips.md
- LICENSE
- pyproject.toml
- README.md
- Sky Painter.lnk
- Skya.lnk
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

A .gitignore file is a text file that tells Git which files and directories to ignore when committing changes to your repository. This is crucial for maintaining a clean and efficient Git repository. 


