{
  // TODO: double-include guard
  // TODO: check version, at minimum need pyroot

  if ( strcmp(gApplication->ClassName(), "TRint") == 0 )
  {
    // Explicit load is optional as of some version, but harmless
    gSystem->Load("libPyROOT");
    TPython::Exec("execfile('dotrootInit.py')");
  }
  else if ( strcmp(gApplication->ClassName(), "PyROOT::TPyROOTApplication") == 0 )
  {
    // TODO: Can we escape to pyroot or are we
    // nesting python inside root inside python?
    // The line
    // ROOT.gROOT.ProcessLine(' TPython::Exec("val = [2,3,4]"); ')
    // will set 'val' in the native python session, so I'm going
    // to take that as yes we can escape to python.
    // In this case, there is no difference between
    // the two TApplication types.
    TPython::Exec("execfile('dotrootInit.py')");
  }
  else
  {
    // Ruby binding?? PROOF?
    // Not sure how PROOF will go along with this...
    cout << "dotroot: Unsupported TApplication type: " << gApplication->ClassName() <<
      ", trying TPython::Exec() anyway! Good Luck!" << endl;
    cout << "File an issue if you get it working :)" << endl;
    TPython::Exec("execfile('dotrootInit.py')");
  }
}
