// This could be compiled, include headers
#include "TPython.h"
#include "TString.h"

int dotrootImport(const char *package) {
  TString package_(package);
  int returnValue = TPython::Eval("dotroot.dotrootImport('"+package_+"')");
  return returnValue;
}

