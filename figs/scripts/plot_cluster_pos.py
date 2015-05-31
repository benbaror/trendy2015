from matplotlib import pyplot as plt
from numpy import pi,sin,cos
from matplotlib.patches import Ellipse
import matplotlib as mpl
import argparse
import mpld3

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




rcParams['font.size'] = 18
rcParams['axes.labelsize'] = 18
rcParams['xtick.labelsize'] = 18 
rcParams['ytick.labelsize'] = 18 
rcParams['legend.fontsize'] = 18 
#rcParams['font.family'] = 'serif'  
#rcParams['font.serif'] = ['Computer Modern Roman']  
#rcParams['font.serif'] = ['Times New Roman']  
rcParams['text.usetex'] = False
rcParams['figure.figsize'] = 7.3, 4.2
#rcParams['figure.figsize'] = 8.0, 6.0
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



def plot_cluster_pos(ecc, fname):
    
    a = 1
    b = a*(1-ecc)/(1+ecc)
    xe = 0
    ye = -a*ecc
    e = Ellipse((0,0), 2*b, 2*a)
    phi = pi/4 - pi/10
    xc =  b*cos(phi)
    yc =  a*sin(phi)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')


    ax.add_patch(e)
    e.set_clip_box(ax.bbox)
    e.set_facecolor([1,1,1])
    e.set_ec('w')
    e.set_fc('none')
    e.set_lw(1)

    plt.plot(xc,yc,'ow',ms = 10)
    plt.text(xc-0.1, yc-0.2, 'Cluster',fontsize = 11,color = 'w')

    plt.plot(xe,ye,'ow',ms = 10)
    plt.text(xe-0.5, ye - 0.2, 'Galactic Center',fontsize = 11,color = 'w')

    dphi = pi/40
    plt.arrow(b*cos(phi+dphi), 
              a*sin(phi+dphi), 
              -b*sin(phi+dphi)*0.0001, 
              a*cos(phi+dphi)*0.0001,
              width = 0.001,
              head_width = 0.04,
              head_starts_at_zero = True,
              fill = False,
              overhang = 0.9,
              color = 'w')

    phis = pi/2
    xs = xc + cos(phis)*a/5.
    ys = yc + sin(phis)*a/5.

    plt.plot(xs, ys, '*w', ms = 10)
    plt.text(xs-0.1, ys+0.1, 'Star',fontsize = 11,color = 'w')


    plt.plot([xe,xc],[ye,yc],'--w')
    plt.text((b*cos(phi)*0.5)*0.6+0.1, (a*sin(phi)*0.1-0.05), '$\mathbf{R}$',color = 'w')

    plt.plot([xe,xs],[ye,ys],'--w')
    plt.text((xs+xe)/2, (ys+ye)/2+0.1, '$\mathbf{x}$',color = 'w')

    plt.plot([xc,xs],[yc,ys],':w')
    plt.text((xc+xs)/2+0.05, (yc+ys)/2-0.01, '$\mathbf{r}$',color = 'w')

    plt.arrow(xc, yc,  (xc-xe)*.5, (yc-ye)*.5, 
              color = 'w', width = 0.001, head_width = 0.03)
    plt.arrow(xc, yc, -(yc-ye)*.5, (xc-xe)*.5, 
              color = 'w', width = 0.001, head_width = 0.03)

    plt.text(xc + (xc-xe)*.5+0.03, yc  +  (yc-ye)*.5 - 0.02, '$x$',color = 'w')
    plt.text(xc - (yc-ye)*.5-0.05, yc + (xc-xe)*.5+0.05, '$y$',color = 'w')



    ax.set_ylim((ye-(1-ecc)*a)*1.4, (ye+(1+ecc)*a)*1.4)
    ax.set_xlim(-a*1.4, a*1.4)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    set_foregroundcolor(ax,'w')
    set_backgroundcolor(ax,'k')

    plt.savefig(fname, bbox_inches = 'tight',transparent = True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot the cluster position')
    parser.add_argument('ecc', type=float, help='eccentricity')
    parser.add_argument('fname', help='Save figure to fname')
    args = parser.parse_args()
    plot_cluster_pos(args.ecc, args.fname)

# plot_cluster_pos(0.0,'circ')
# plot_cluster_pos(0.4,'ellip')
