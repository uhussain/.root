import ROOT
import os
import sys

# Package macro path
_dotrootBasePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
_prevpath = ROOT.gROOT.GetMacroPath()
if _prevpath[-1] != ':':
    _prevpath += ':'
ROOT.gROOT.SetMacroPath(_prevpath + os.path.join(_dotrootBasePath, 'dotroot', 'macro') + ':')

# Set up dotrootImport() function
from dotrootImport import dotrootImport
# TODO: possibly compile dotrootImport (will it make a difference?)
ROOT.gROOT.ProcessLineSync(".L dotrootImport.C")
