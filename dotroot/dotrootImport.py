import json
import os
import subprocess
import urllib

dotrootBasePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# Python 2.7: subprocess.check_output(cmd)
localGitUser = subprocess.Popen(['git', 'config', '--get', 'user.github'], stdout=subprocess.PIPE).stdout.read().strip()

class dotrootException(Exception) :
    pass

def dotrootImport(packageName) :
    try :
        package = findPackage(packageName)
        # Python 2.7: 
        #   import importlib
        #   importlib.import_module('packages.'+package) 
        __import__('packages.'+package)
        return 1
    except dotrootException as ex :
        print 'dotroot Exception while trying to import ' + packageName
        print '-'*40
        print ex
    return 0

def findPackage(packageName) :
    (gituser, package) = parsePackageName(packageName)
    packagePath = os.path.join(dotrootBasePath, 'packages', package)
    if not os.path.exists(packagePath) :
        installPackage(package, gituser)
    elif not os.path.exists(os.path.join(packagePath, '.git/refs/remotes', gituser)) :
        if checkGithubUrlExists(package, gituser) :
            addRemoteToPackage(package, gituser)
        else :
            raise dotrootException('The package %s has no fork for user %s' % (package, gituser))
    checkoutPackage(package, gituser)
    return package
    
def installPackage(package, gituser) :
    giturl = findGithubUrl(package, gituser)
    if checkGithubUrlExists(package, gituser) :
        cmd = ['git', 'clone', '-q', '--origin', gituser, giturl]
        if subprocess.call(cmd, cwd=os.path.join(dotrootBasePath, 'packages')) != 0 :
            raise dotrootException('Failed to clone package repo: %s' % giturl)
        if gituser != localGitUser :
            cmd = ['git', 'checkout', '-q', gituser+'/master']
            subprocess.call(cmd, cwd=os.path.join(dotrootBasePath, 'packages', package))
            cmd = ['git', 'branch', '-q', '-d', 'master']
            subprocess.call(cmd, cwd=os.path.join(dotrootBasePath, 'packages', package))
    # TODO: decide how to handle creating new package
    # elif 'git@github.com' in giturl :
    #     createNewPackage(package, gituser)
    else :
        raise dotrootException('The package %s either does not exist or has no fork for user %s' % (package, gituser))

def createNewPackage(package, gituser) :
    print 'Creating new package for you!  You have to push to the remote yourself.'
    packageDir = os.path.join(dotrootBasePath, 'packages', package)
    os.makedirs(packageDir)
    cmd = ['git', 'init']
    subprocess.call(cmd, cwd=packageDir)
    with open(os.path.join(packageDir, '__init__.py'), 'w') as initFile :
        initFile.write('import ROOT')
    cmd = ['git', 'add', '__init__.py']
    subprocess.call(cmd, cwd=packageDir)
    cmd = ['git', 'commit', '-m', 'Auto-generated initial commit for dotroot package']
    subprocess.call(cmd, cwd=packageDir)

def addRemoteToPackage(package, gituser) :
    packagePath = os.path.join(dotrootBasePath, 'packages', package)
    giturl = findGithubUrl(package, gituser)
    cmd = ['git', 'remote', 'add', gituser, giturl]
    if subprocess.call(cmd, cwd=packagePath) != 0 :
        raise dotrootException('Failed to add remote %s for package %s' % (gituser, package))

def checkoutPackage(package, gituser) :
    branch = gituser+'/master'
    if gituser == localGitUser :
        branch = 'master'
    packagePath = os.path.join(dotrootBasePath, 'packages', package)
    cmd = ['git', 'checkout', '-q', branch]
    if subprocess.call(cmd, cwd=packagePath) != 0 :
        raise dotrootException('Failed to checkout branch %s for package %s' % (branch, package))

def findGithubUrl(package, gituser) :
    urlBase = 'https://github.com/%s/' % gituser
    if gituser == localGitUser :
        urlBase = 'git@github.com:%s/' % localGitUser
    return urlBase+package+'.git'

def checkGithubUrlExists(package, gituser) :
    req = '/'.join(['https://api.github.com/repos', gituser, package])
    try :
        info = json.load(urllib.urlopen(req))
        if 'id' in info :
            return True
    except IOError:
        raise dotrootException('Failed to query github API when checking package existence for %s/%s' % (gituser, package))

    return False

def parsePackageName(packageName) :
    strs = packageName.split('/')
    if len(strs) != 2 :
        raise dotrootException('Package "%s" appears invalid, please check.' % packageName)
    return (strs[0], strs[1])

