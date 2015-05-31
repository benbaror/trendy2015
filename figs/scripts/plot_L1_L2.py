import sys
import os
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../../../code')
import esc
import argparse
from matplotlib import rcParams  
import mpld3
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




rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 18
rcParams['xtick.labelsize'] = 18 
rcParams['ytick.labelsize'] = 18 
rcParams['legend.fontsize'] = 18 
#rcParams['font.family'] = 'serif'  
#rcParams['font.serif'] = ['Computer Modern Roman']  
#rcParams['font.serif'] = ['Times New Roman']  
rcParams['text.usetex'] = False
#rcParams['figure.figsize'] = 7.3, 4.2
rcParams['figure.figsize'] = 8.0, 6.0
plt.rcParams['xtick.major.size'] = 3
plt.rcParams['xtick.minor.size'] = 3
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['ytick.major.size'] = 3
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['ytick.major.width'] = 1
plt.rcParams['ytick.minor.width'] = 1
plt.rcParams['legend.frameon'] = False
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['lines.linewidth'] = 3

rcParams['legend.frameon'] = False



models = ['Steps','Gaussian','a','Uncorrelated','b', 'Exponential']
model_color = dict(zip(models,colors(len(models))))


def set_foregroundcolor(ax, color):
     '''For the specified axes, sets the color of the frame, major ticks,                                                             
         tick labels, axis labels, title and legend                                                                                   
     '''
     for tl in ax.get_xticklines() + ax.get_yticklines():
         tl.set_color(color)
     for spine in ax.spines:
         ax.spines[spine].set_edgecolor(color)
     for tick in ax.xaxis.get_major_ticks():
         tick.label1.set_color(color)
     for tick in ax.yaxis.get_major_ticks():
         tick.label1.set_color(color)
     ax.axes.xaxis.label.set_color(color)
     ax.axes.yaxis.label.set_color(color)
     ax.axes.xaxis.get_offset_text().set_color(color)
     ax.axes.yaxis.get_offset_text().set_color(color)
     ax.axes.title.set_color(color)
     lh = ax.get_legend()
     if lh != None:
         lh.get_title().set_color(color)
         lh.legendPatch.set_edgecolor('none')
         labels = lh.get_texts()
         for lab in labels:
             lab.set_color(color)
     for tl in ax.get_xticklabels():
         tl.set_color(color)
     for tl in ax.get_yticklabels():
         tl.set_color(color)

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot the L1 L2')
    parser.add_argument('fname', help='Save figure to fname')
    args = parser.parse_args()
    fig, ax = plt.subplots()

    E_Ec = [0.6,0.8,0.9,1.0,1.3]
    x = np.linspace(-1.5,1.5,10000)
    for E_Ecc in E_Ec:
        y = esc.get_ymax(x-1,E_Ecc,0)
        ax.plot(x,y,'w')
        ax.plot(x,-y,'w')

    # plt.xlabel(r'$x$')
    # plt.ylabel(r'$y$')
    ax.axes.get_yaxis().set_visible(False)

    ax.set_ylim(-1.5,1.5)
    set_foregroundcolor(ax,'w')
    set_backgroundcolor(ax,'k')
    plt.savefig(args.fname, transparent=True)

#plt.ylabel(r'$N(\epsilon,\tau)$')
#plt.savefig('../L1_L2.png',transparent = True)



