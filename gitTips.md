# Git Tips for working with the pipe
As of now, this is simply a file to help myself (Aubury) or anyone else who is a noob at git so that they understand how to get goood workflow and not break stuff. 

## Making a branch

## Getting the latest changes from the origin, master or production folder on to your branch
git fetch --all
git merge origin/prod

## Making sure your username and email are set
git config --global user.name "John Doe"
git config --global user.email "johndoe@email.com"

you can check if that setting is set by going into your repository and typing:
git config -l --show-origin