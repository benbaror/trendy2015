import sys
import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../code')
import esc
import argparse
import subprocess
import tempfile
reload(esc)

from matplotlib import rcParams  
try:
    import seaborn as sns
    #sns.set(style="whitegrid")
    #sns.set(style="nogrid")
    sns.set(style="ticks",context = 'paper', font = 'serif')
    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'
    colors = lambda n: sns.color_palette("jet", n)
except ImportError:
    print "'seaborn' is not installed using default 'matplotlib' plots"
    cmap = plt.cm.Set1
    colors = lambda n: map(tuple, cmap(np.linspace(0, 1, 12)[:n])[:, :3])
#    colors = lambda n: mpl.cm.hsv(linspace(0,1,n))

def set_backgroundcolor(ax, color):
    '''Sets the background color of the current axes (and legend).
    Use 'None' (with quotes) for transparent. To get transparent
    background on saved figures, use:
    pp.savefig("fig1.svg", transparent=True)
    '''
    ax.patch.set_facecolor(color)
    lh = ax.get_legend()
    if lh != None:
        lh.legendPatch.set_facecolor(color)

def init_fun():
#    ax.clear()
    ax.plot(x,y,'--w',x,-y,'--w',lw = 1.0)
    ymin = y.min()
    print 'ymin = ' +  str(ymin)
    ax.plot([1.0, 1.0], [-ymin, ymin], '--w', lw = 1.0, zorder = 1)
    ax.plot([-1.0, -1.0], [-ymin, ymin], '--w', lw = 1.0, zorder = 1)
    [lines[i].set_data([],[]) for i in xrange(n)]
    [points[i].set_data([],[]) for i in xrange(n)]
    return lines + points,

def run(it):
    if np.mod(it,max(1,t.size/100)) == 0:
        print 1.0*it/t.size
    # update the data
    ax.set_xlim(-2, 2)
    ax.set_ylim(-1, 1)
    nt = max(0,it-n_track)
    [lines[i].set_data(v[i,nt:it,0],v[i,nt:it,1]) for i in xrange(n)]
    [points[i].set_data(v[i,it,0],v[i,it,1]) for i in xrange(n)]
    fig.tight_layout(0,0,0,0)
    return lines + points,



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make cluster escape animation')
    parser.add_argument('fname', help='Save animation to fname')
    parser.add_argument('E_Ec', type=float,  help='Relative Excess energy <= 1.0')
    parser.add_argument('xL_max', type=float, help='Maximal initial distance form L1')
    args = parser.parse_args()
    E_Ec = args.E_Ec
    xL_max = args.xL_max
    t = np.linspace(0, 2*np.pi, 500)

    S1 = esc.Stars(E_Ec,xL_max = xL_max,n=10000, linear = 0.0, neg_x = 1.0)
    r = np.random.rand(S1._n); r = r/r.sum()
    w = S1.wight0/S1.wight0.sum()
    ix = np.where(r<w)[0]
    print ix.size
    n = 30


    n_track = t.size/100
    fig = plt.figure()

    ax = plt.axes()
    set_backgroundcolor(ax,'k')
    ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)
    x = np.linspace(-1.5,1.5,1000)
    y = esc.get_ymax(x-1,E_Ec,0)

    generate = True
    i = 0
    j = 0
    v = np.zeros([n,t.size,4])
    while i<n:
        print i,j
        vi,output = esc.integrate(t,S1.vec0[ix[j]], Dfun = esc.Jac, full_output = 1)
        if np.all(output['mused']>=1) and np.all(abs(esc.calc_E(vi[:,:])*2/9. + E_Ec) < 1e-9):
            v[i,:,:] = vi
            i = i+1
        j = j+1

    print sum(abs(esc.calc_E(v[:,-1,:])*2/9. + E_Ec) < 1e-9)
              
    n = v.shape[0]
    print 'n = {}'.format(n)

    if E_Ec < 1.0:
        colors = ['b' if np.all(np.abs(v[i,:,0])<1.0) else 'r' if np.any(np.abs(v[i,-1,0])>1.0) else 'g' for i in xrange(n)]
    else:
        colors = ['w' for i in xrange(n)]
    print colors.count('b'), colors.count('r'), colors.count('g'), colors.count('w')
    lines = [ax.plot([], [], ms=3, marker = '.', ls = '' , color = colors[i])[0] for i in xrange(n)]
    points = [ax.plot([], [], ms=10, marker = '.', ls = '' , color = colors[i])[0] for i in xrange(n)]

    #ax.grid()
    xdata, ydata = [], []

    anim = animation.FuncAnimation(fig, run, init_func=init_fun, frames = t.size, interval=25, blit=True)
    #    fname = 'esc_movie_{}_{}_{}.gif'.format(E_Ec,xL_max,colors.count('g'))
    with tempfile.NamedTemporaryFile(suffix = '.gif') as temp:
        anim.save(temp.name,  writer='imagemagick', fps=15)
        cmd = 'gifsicle -U --disposal=previous --transparent="#000000" -O2 {} > {}'.format(temp.name, args.fname)
        subprocess.call(cmd,  shell=True)

