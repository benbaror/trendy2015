import sys
import os
import numpy as np
import matplotlib.pyplot as plt
path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path+'/../../../code')
from linear_dyn import Stars
import argparse
import subprocess
import tempfile
plt.style.use(path + '/dark_background.mplstyle')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make cluster escape animation')
    parser.add_argument('fname', help='Save animation to fname')
    parser.add_argument('--E_Ec', type=float, default=0.99,  help='Relative Excess energy <= 1.0')
    parser.add_argument('--x_max', type=float, default=1.0, help='Maximal initial distance form L1')
    parser.add_argument('--ecc', type=float, default=0.0, help='eccentricity')
    parser.add_argument('--phi0', type=float, default=0.0, help='Initial true anomaly (0 at periapsis)')
    parser.add_argument('--Ns', type=int, default=100, help='Number of stars')
    parser.add_argument('--Nt', type=int, default=100, help='Number of time steps')
    parser.add_argument('--tmax', type=float, default=1.0, help='Maximal time in units of orbital period')
    args = parser.parse_args()
    print args
    S = Stars(args.E_Ec, args.Ns, args.Nt, args.ecc, args.phi0, args.tmax, args.x_max)
    print sum(S.r[0,:,-1]>0)
    #    fname = 'esc_movie_{}_{}_{}.gif'.format(E_Ec,xL_max,colors.count('g'))
    with tempfile.NamedTemporaryFile(suffix = '.gif') as temp:
        S.anim.save(temp.name,  writer='imagemagick', fps=15)
        cmd = 'gifsicle -U --disposal=previous --transparent="#000000" -O2 {} > {}'.format(temp.name, args.fname)
        subprocess.call(cmd,  shell=True)


