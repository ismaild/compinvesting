import glob
import os
import sys

pwd = os.path.dirname(os.path.abspath(__file__))

ifile = glob.glob( os.path.join(pwd,"data","all", '*.csv') )


for f in ifile:
    fname = f.split()
    f_new = os.path.join(fname[0], fname[1]).replace('/.','.')
    print f, fname, f_new
    os.rename(f,f_new)