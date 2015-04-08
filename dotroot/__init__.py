import ROOT
import os
import sys

# Package macro path
dotrootBasePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ROOT.gROOT.SetMacroPath(ROOT.gROOT.GetMacroPath() + os.path.join(dotrootBasePath, 'dotroot', 'macro') + ':')

# Set up dotrootImport() function
from dotrootImport import dotrootImport
# TODO: possibly compile dotrootImport (will it make a difference?)
ROOT.gROOT.ProcessLineSync(".L dotrootImport.C")
