/* dotrootInit.C : Sets up paths so that dotroot is available to both root and python
 *   This is done by adding the .root/macro directory to ROOT's MacroPath, and by adding
 *   .root/dotroot to python's path
 *   
 */
#include "TApplication.h"
#include "TEnv.h"
#include "TPython.h"
#include "TSystem.h"
#include "TString.h"

void dotrootInit() {
  // Double-include guard
  if ( gEnv->GetValue("dotroot.Initialized", 0) == 0 ) {
    gEnv->SetValue("dotroot.Initialized", 1);
  } else {
    return;
  }

  // TODO: check version, at minimum need pyroot

  // Explicit load is optional as of ROOT v4.00/06, but harmless
  gSystem->Load("libPyROOT");

  // TString because trying to be as ROOT-centric as possible
  // TODO: figure out directory this script is called from
  TString dotrootPath(gSystem->ExpandPathName("$HOME/.root"));

  TPython::Exec("import sys");
  TPython::Exec("sys.path.append('" + dotrootPath + "')");

  gROOT->SetMacroPath( gROOT->GetMacroPath() + dotrootPath + "/macro:" );

  if ( strcmp(gApplication->ClassName(), "TRint") == 0 ) {
    // interactive ROOT
    // As we go through dotroot imports, inevitably an
    // 'import ROOT' will get called, at which point
    // pyroot will try to re-evaluate rootlogin.C
    // (see $ROOTSYS/lib/ROOT.py, ModuleFacade.__finalSetup)
    // We don't want that, so we prevent that by setting
    // the -n argument, triggering pyroot initialization,
    // and removing it.
    // TODO: if pyroot is already initialized, this will
    // make complaints, so check that, and warn user that
    // somehow they are initializing pyroot in their login
    // script, which causes a double-run of the login script
    TPython::Exec("sys.argv.append('-n')");
    TPython::Exec("ROOT._ModuleFacade__finalSetup()");
    TPython::Exec("del ROOT.__class__._ModuleFacade__finalSetup");
    TPython::Exec("sys.argv.pop()");
  } else if ( strcmp(gApplication->ClassName(), "PyROOT::TPyROOTApplication") == 0 ) {
    // interactive python
  } else {
    // Batch mode? Ruby binding? PROOF?
  }

  TPython::Exec("import dotroot");

}
