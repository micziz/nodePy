# PyJS
# Run Javascript (or Typescript) directly in python
# Feauters:

# Runs .js .mjs and .cjs files.
# Supports all libraries (just runs node in a hidden way!)
# Automatticaly compiles .ts files and runs them with NO tsconfig(uses tsc) 
# No dependencies
# Uses modern apis

# System to run tsc. We dont need stdout
# Remove to remove js file if we compile
from os import system, remove, getcwd
# Subprocces to run node and get the result
from subprocess import run, PIPE
# Pathlib for path manipulation stuff
from pathlib import PurePath
# Argv for arguments
from sys import argv

def getFileWithNoExt(file):
    purePathFile = PurePath(file)
    return purePathFile.stem

def getFileExt(file):
    purePathFile = PurePath(file)
    return purePathFile.suffix

def isTs(Ext):
    if '.ts' in Ext:
        return True
    else:
        return False

def isMjs(Ext):
    if '.mjs' in Ext:
        return True
    else:
        return False

def isCjs(Ext):
    if '.cjs' in Ext:
        return True
    else:
        return False

def checkIfNoDeleate():
    try:
        if argv[2] == '--noDel':
            return True
        else:
            return False
    except IndexError:
        pass

def runFile(file):
    fileNoExt = getFileWithNoExt(file)
    ext = getFileExt(file)
    isTsQ = isTs(ext)
    if isTsQ:
        system(f'tsc {file} --target es6 --outfile {fileNoExt}.js')
        result = run(['node', f'{fileNoExt}.js'], stdout=PIPE).stdout.decode('utf-8')
        noDel = checkIfNoDeleate()
        if not noDel:
            remove(f'{fileNoExt}.js')
    else:
        isMjsQ = isMjs(ext)
        isCjsQ = isCjs(ext)
        if isMjsQ:
            result = run(['node', f'{fileNoExt}.mjs'], stdout=PIPE).stdout.decode('utf-8')
        elif isCjsQ:
            result = run(['node', f'{fileNoExt}.cjs'], stdout=PIPE).stdout.decode('utf-8')
        else:
            result = run(['node', f'{fileNoExt}.js'], stdout=PIPE).stdout.decode('utf-8')
    print(result)

def cli():
    try:
        if argv[1] == '--help':
            print("""
usage: nodePy [file] (options)

    --noDel: Don't delate the js file after compilation
            """)
        else:
            runFile(f'{getcwd()}/{argv[1]}')
    except IndexError:
        print("""
usage: nodePy [file] (options)

    --noDel: Don't delate the js file after compilation
        """)

if __name__ == '__main__':
    cli()