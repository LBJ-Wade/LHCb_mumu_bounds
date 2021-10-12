import glob
import re
import numpy as np
from numpy import genfromtxt
import subprocess
import sys

#To run: python parameter_scan.py file-with-masses&taus Rfactor(luminocity ratio) (Rfactor=1 for the original analysis) 
#Input file units: mass in GeV, tau in ps
#Output stored in the output_combined_Rfactor folder

#reads m and tau from input file, runs root macro to get BR and writes (m, tau, BRexp) to a file 
inputfile=sys.argv[1]
print(inputfile)

Rfactor=sys.argv[2]
params = genfromtxt(inputfile,  comments="#", delimiter=',')#you can choose the delimiter you like
print(params)

outputfile=re.sub(".dat","_exp.dat",re.sub("\A([\S]+)/",'output_experimental/',inputfile))

# writes the table with same parameters and experimental BR only (the LHCb code automatically otputs results in a file)
with open(outputfile,'w') as fout:
    fout.write("#m [GeV],  tau [ps], c, BRexp(B+->K+mumu)\n")

#runs the LHCb root file using the mass=params[i,0] and tau=params[i,1] parameters
for i in range(params.shape[0]):
	cmd="root -b -q B2KX_Fig4.C BRmtau.C'({mass},{tau},\"{outfile}\")'".\
            format(mass=params[i,0]*10**3,tau=params[i,1],outfile=outputfile)
	subprocess.call([cmd],shell=True)

#calculates if BRtheory is allowed and combines together (m, tau, BRtheory, BRexp, allowed/not allowed (1/0))
expparams=genfromtxt(outputfile,  comments="#", delimiter='\t')

#creating the combined output file
combooutput=re.sub(".dat","_comb.dat",re.sub("\A([\S]+)/",'output_combined_Rfactor{0}/'.format(Rfactor),inputfile))
with open(combooutput,'w') as foutcomb:
    print("output_comb: "+combooutput)
    allparams=[]
    foutcomb.write("#m [GeV],  tau [ps], c, BRtheo(B+->K+mumu), BRexp, allowed/excluded(1/0)\n")#if you have more coupling, add the corresponding column here

    
    for i in range(params.shape[0]):
        ifallowed=0
        if (float(params[i,3])<float(expparams[i,2])/float(Rfactor)):#comparing theoretical BR, params[i,3], and experimental ratio, expparams[i,2].
            ifallowed=1#1 if allowed, 0 if excluded
        newparams=np.append(params[i],[expparams[i,2],ifallowed])
        allparams.append(newparams)
    allparams=np.array(allparams)
    print(allparams)
    np.savetxt(foutcomb, allparams, fmt='%5e', delimiter='\t')#you can choose the delimiter you like

