import ROOT
import os

# Package macro path
dotrootPath = os.path.dirname(os.path.realpath(__file__))
ROOT.gROOT.SetMacroPath(ROOT.gROOT.GetMacroPath()+dotrootPath+"/macro:")

# Set up dotrootImport() function
from dotrootImport import dotrootImport
# TODO: possibly compile dotrootImport (will it make a difference?)
ROOT.gROOT.ProcessLineSync(".L dotrootImport.C")

# Mapping python functions into root:
# make a wrapper in macro, then 
# ROOT.gROOT.ProcessLine(".L function.C")

