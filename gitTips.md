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

## CR LF line endings
Common line-ending related issues, how to fix and avoid them.

### What are line terminators
Computers need to know when to start a new line, but the characters used to represent this can vary between platforms. This causes compatibility issues and unforseen side effects, such as giant git diffs with no apparent change. 

There are 2 control characters that represent line endings. 

* carriage return
    * aka CR \r ^M 0xod
    * represent a cursor movement back to column 0
* line feed
    * aka LF \n $ 0x0a
    * represents a cursor movement directly downward

window uses CR + LF to represent line-endings

any unix-like operating system (linux, *BSD, macOS) represent line-endings with a single LF

### how to check line endings

the file command will explicitly stat CRLF endings; LF is implicit.

$ file lf.txt
lf.txt: ASCII text

$ file crlf.txt
crl.txt: ASCII text, with CRLF line terminators

use cat with h -v or -e option

* ^M=CR
* $=LF

$ cat -v crlf.txt # hides LF
never gonna give you up^M
never gonna let you down^M

$ cat -e crlf.txt # shows LF
never gonna give you up^M$
never gonna let you down^M$

### How to fix line-endings
#### for one-off files 
use a tool like
* dos2unix /unix2dos
*vim sed tr etc

most reliable is probably dos2unix (may require install)

$ dos2unix crlf.txt # convert to LF
$ unix2dos lf.txt # convert to CRLF

some other ways

$ sed 's/\r$//' crlf.txt > lf.txt

#### to configure git (+repos)
configure git locally to use LF endings

git config --global core.autocrlf true

configure line endings per project (RECOMMENDED)

create a .gitattributes file in project root dir 

* text=auto

* i recommend starting with a gitattributes template
* to understand warning: lF will be replaced by CRLF, refer to this stack overflow answer

to change endings in an EXISTING project:

// save files before changing


$ git add . -u
$ git commit -m "Saving files before refreshing line endings"


// renormalize endings (make sure run from project root)

git add --renomalize

# check and commit

$ git status
$ git commit -m "normalize line endings"

* carriage return brings it to the first column. Line feed brings it straight.

# launch a dcc
/c/Program\ Files/Autodesk/Maya2025/bin/mayapy.exe pipeline --log-level=INFO maya

# Using pip and other cool things on windows. 
Do so through a python installation

for example, if I am on windows and want to download the six module i would try:

C:\Program Files\Autodesk\Maya2025\bin\mayapy.exe -m pip download six