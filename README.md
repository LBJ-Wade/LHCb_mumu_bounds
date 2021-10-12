# LHCb_mumu_bounds
Calculates the LHCb B -> K mu mu bounds from 1612.07818 for a chosen BSM model


lhcb_2015_036.root combined with the \*.c files contain allthe information from Fig.4 in lhcb_2015_036.root
parameter_scan.py compares the theoretically predicted values from an input file (formatted as #  m  [GeV] ,  tau  [ps] ,  c ,  BR_theo(K+->pi+  a)) to the experimental predictions for the same (m, tau), extracted from lhcb_2015_036.root. The result is saved to the output_combined_Rfactor[] folder.

To run the example type  python3 parameter_scan.py inputfiles/input_example.dat 1
