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
from subprocess import run, PIPE, CalledProcessError
# Pathlib for path manipulation stuff
from pathlib import PurePath
# Argv for arguments
from sys import argv
from shutil import which

def getFileWithNoExt(file):
    purePathFile = PurePath(file)
    return purePathFile.stem

def getFileExt(file):
    purePathFile = PurePath(file)
    return purePathFile.suffix

def exists(tool):
    return which(tool) is not None

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

def isDeno():
    try:
        if argv[2] == "--deno":
            return True
        else:
            return False
    except:
        pass
            
def notInstalledError(name, link):
    return f"{name} is not installed. Install it at {link}"


def runTsc(file, fileNoExt):
    tscCommandToRun = ['tsc', file, '--target', 'es6', '--outfile', f'{fileNoExt}.js']
    run(tscCommandToRun, check=True)

def runCommand(command):
    result = run(command, stdout=PIPE, check=True).stdout.decode('utf-8')
    return result

def nodeCommand(fileNoExt):
    return ['node', f'{fileNoExt}.js']


def runFile(file):
    fileNoExt = getFileWithNoExt(file)
    ext = getFileExt(file)
    isTsQ = isTs(ext)
    isDenoQ = isDeno()
    if isDenoQ:
        if exists('deno'):
            try:
                result = runCommand(['deno', 'run', file])
                print(result)
            except:
                print('ERROR IN DENO')
        else:
            print(notInstalledError('deno', 'https://deno.land'))
    elif isTsQ:
        if exists('tsc'):
            try:
                runTsc(file, fileNoExt)
            except CalledProcessError:
                print('ERROR IN THE TYPESCRIPT COMPILER')
        else:
            print(notInstalledError('typescript', 'https://typescript-lang.org'))
        if exists('node'):
            try:
                nodeCommandToRun = nodeCommand(fileNoExt)
                result = runCommand(nodeCommandToRun)
                print(result)
            except CalledProcessError:
                print('ERROR IN NODE')
        else:
            print(notInstalledError('node', 'https://nodejs.org'))
        noDel = checkIfNoDeleate()
        if not noDel:
            remove(f'{fileNoExt}.js')
    else:
        isMjsQ = isMjs(ext)
        isCjsQ = isCjs(ext)
        if isMjsQ:
            result = run(['node', file], stdout=PIPE).stdout.decode('utf-8')
            print(result)
        elif isCjsQ:
            result = run(['node', file], stdout=PIPE).stdout.decode('utf-8')
            print(result)
        else:
            result = run(['node', file], stdout=PIPE).stdout.decode('utf-8')
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