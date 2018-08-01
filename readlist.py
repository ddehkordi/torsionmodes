# -*- coding: utf-8 -*-


import pandas as pd


mo = pd.read_csv('modes.dat', sep=' ', skipinitialspace=True)        


for eigmode in range(1,11):
    cmode = mo.loc[mo.Cartesian_mode == eigmode]
#    f= open("simulation/run/mode_{}/plu_{}.dat".format(eigmode,eigmode),"w+")
    f= open("plu_{}.dat".format(eigmode),"w+")
    bias_arg = "ABMD ARG="
    bias_to= " TO="
    bias_kappa= " KAPPA="
    bias_label= " LABEL=abmd\n"
    dump = "PRINT ARG=abmd.bias,"
    torvars = "# DEFINE THE TORSION VARIABLES\n"
#    cal_dtau = " # CALCULATE THE DEVIATION FROM THE INITIAL TORSION\n"
    
    for idx,i in enumerate(cmode.index):
        torvars = torvars + "t{}: TORSION ATOMS=".format(idx) + cmode.loc[i].ATOM_1.astype(int).astype(str) +\
                                          "," + cmode.loc[i].ATOM_2.astype(int).astype(str) +\
                                          "," +cmode.loc[i].ATOM_3.astype(int).astype(str) +\
                                          "," + cmode.loc[i].ATOM_4.astype(int).astype(str)+"\n"

        
#        if cmode.loc[i].Old_torsion.astype(float) > 0:
#            cal_dtau= cal_dtau + "dtau{}: MATHEVAL ARG=t{} FUNC=x-{} PERIODIC=-3.14159,3.14159\n".format(idx,idx,cmode.loc[i].Old_torsion.astype(float)) 
#        else:
#                cal_dtau= cal_dtau + "dtau{}: MATHEVAL ARG=t{} FUNC=x+{} PERIODIC=-3.14159,3.14159\n".format(idx,idx,abs(cmode.loc[i].Old_torsion.astype(float)))                 

        bias_arg    = bias_arg + "t{},".format(idx)
        bias_to     = bias_to + str(cmode.loc[i].New_torsion.astype(float))+","
        bias_kappa  = bias_kappa + "0.1,"
        dump = dump + "t{},".format(idx)
    f.write(torvars)    
    f.write(bias_arg[:-1] + bias_to[:-1] + bias_kappa[:-1] + bias_label)
    f.write(dump[:-1] + " STRIDE=10 FILE=colvar{}.dat FMT=%8.4f\n".format(eigmode))
    f.close()


