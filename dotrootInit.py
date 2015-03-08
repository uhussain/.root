print "I'm in python"

# Mapping python functions into root:
# global namespace functions stored in hashtable
# ROOT.gROOT.GetListOfGlobalFunctions()
# Maybe TPython has a method to generate a function
# signature to add to this list
# for pure python functions that have known types

# mapping python in python is easier
import dotrootImport
ROOT.dotrootImport = dotrootImport.dotrootImport
# Prevent namespace pollution (still in sys.modules)
dotrootImport = None


# for C macro functions, make available
# via the usual
# ROOT.gROOT.ProcessLine(".L function.C")

