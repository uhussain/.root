dotroot
=======

Goal: to provide a more convenient way to include user scripts for [ROOT](https://root.cern.ch/drupal/) by emulating 
package ecosystems like [vundle](https://github.com/gmarik/Vundle.vim) and [brew](http://brew.sh/)

Chances of success: possibly zero.

Installation
------------
* Clone repo: `pushd ~ && git clone https://github.com/nsmith-/.root.git && popd`
* Edit `rootlogon.C`, add line `gROOT->ProcessLineSync(".x $HOME/.root/dotrootInit.C+");`
* Enjoy!

Importing Packages
------------------
  The dotroot library, by itself, does nothing other than provide a convenient interface to include packages of 
generic ROOT macros into analysis, either interactive or through scripts.  All dotroot packages must exist as a
publicly accessible github repository, and are addressed by the syntax `username/repository`

### Importing interactively
  Interactive analysis will have all previously imported packages available, plus a convenient function to
import additional packages, `dotrootImport("user/package")`

### Importing from scripts
  A script that uses a packages managed by dotroot will have a list of required packages declared in its initialization.
Dotroot checks if the necessary packages are installed, and if not, automatically downloads and installs them.

ROOT Example: (`macro.C`)
```cpp
void macro ( int argument )
{
  dotrootImport("nsmith-/buildLegend");

  // ... code ...
}
```

PyROOT Example: (`macro.py`)
```python
import ROOT
ROOT.dotrootImport('nsmith-/buildLegend')

# ... code ...
```

Creating Packages
-----------------
### New package
  To create a new package, simply create a new repository on github, and then `dotrootImport()` it.  If your 
github credentials are appropriately set up, dotroot will detect that you are importing a package you own 
and set the SSH remote URL.  You then have a clone of your repository in `~/.root/packages/` ready to be worked on.

### Fork a package
  Because every package is on github, users are highly encouraged to fork existing packages for their own use, 
modify them as necessary, and send pull requests if applicable.  To fork, find the package URL on github
(`https://github.com/username/package`) and click `Fork`.  Then use `dotrootImport()` on your fork.

