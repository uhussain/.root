import ROOT

# Set up dotrootImport() function
from dotrootImport import dotrootImport
# TODO: possibly compile dotrootImport (will it make a difference?)
ROOT.gROOT.ProcessLineSync(".L dotrootImport.C")

# Mapping python functions into root:
# global namespace functions stored in hashtable
# ROOT.gROOT.GetListOfGlobalFunctions()
# Maybe TPython has a method to generate a function
# signature to add to this list
# for pure python functions that have known types

# mapping python in python is easier

# for C macro functions, make available
# via the usual
# ROOT.gROOT.ProcessLine(".L function.C")

