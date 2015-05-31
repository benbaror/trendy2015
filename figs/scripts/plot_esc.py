import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
sys.path.append('../../../code')
import esc
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

reload(esc)


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




def generate_orbits(E_Ec, xL_max, n, neg_x = False):
    t = np.linspace(0,2*np.pi,1000)

    S1 = esc.Stars(E_Ec,xL_max = xL_max,n=10000, linear = 0.0, neg_x = neg_x)
    r = np.random.rand(S1._n); r = r/r.sum()
    w = S1.wight0/S1.wight0.sum()
    ix = np.where(r<w)[0]
    print ix.size

    x = np.linspace(-1.5,1.5,1000)
    y = esc.get_ymax(x-1,E_Ec,0)

    generate = True
    if generate:
        v = np.zeros([n,t.size,4])
        for i in xrange(n):
            v[i,:,:] = esc.integrate(t,S1.vec0[ix[i]], Dfun = esc.Jac)

    ix = np.where(abs(esc.calc_E(v[:,-1,:])*2/9. + E_Ec) < 1e-9)[0]
              
    v = v[ix,:,:]
    n = ix.size
    print 'n = {}'.format(n)
    return v


# v = generate_orbits(0.99,1.0,100, neg_x = True)
# esc_type = ['p_esc' if np.all(np.abs(v[i,:,0])<1.0) else 'r_esc' if np.any(np.abs(v[i,-1,0])>1.0) else 'f_esc' for i in xrange(v.shape[0])]
# print 'real =  {}, potential = {}, fake = {}'.format(esc_type.count('r_esc'),esc_type.count('p_esc'),esc_type.count('f_esc'))


# i_f_esc = np.where(np.array(esc_type) == 'f_esc')[0]
# i_p_esc = np.where(np.array(esc_type) == 'p_esc')[0]
# i_r_esc = np.where(np.array(esc_type) == 'r_esc')[0]

# fig, ax = plt.subplots()


# for i in i_p_esc[:5]:
#     x,y = v[i,:,:2].T
#     ax.plot(x,y,lw = 1.5)

# x = np.linspace(-1.5,1.5,1000)
# y = esc.get_ymax(x-1,E_Ec,0)
# ax.plot(x,y,'--w',x,-y,'--w')
# ymax0 = esc.get_ymax(0,E_Ec,0)
# ax.plot([1.0,1.0],[-ymax0,ymax0],':w')
# ax.plot([-1.0,-1.0],[-ymax0,ymax0],':w')
# ax.set_xlim(-1.1,1.1)
# ax.set_ylim(-1.0,1.0)
# set_foregroundcolor(ax,'w')
# set_backgroundcolor(ax,'k')

# #plt.ylabel(r'$N(\epsilon,\tau)$')
# plt.savefig('../p_esc.eps',transparent = True)

# fig, ax = plt.subplots()

# ix = np.where(v[i_r_esc,-1,0]>1.5)[0]
# print ix.size
# for i in i_r_esc[ix[:5]]:
#     x,y = v[i,:,:2].T
#     if x[-1] > 1.5:
#         ax.plot(x,y,lw = 1.5)

# x = np.linspace(-1.5,1.5,1000)
# y = esc.get_ymax(x-1,E_Ec,0)
# ax.plot(x,y,'--w',x,-y,'--w')
# ymax0 = esc.get_ymax(0,E_Ec,0)
# ax.plot([1.0,1.0],[-ymax0,ymax0],':w')
# ax.plot([-1.0,-1.0],[-ymax0,ymax0],':w')
# ax.set_xlim(0.5,1.5)
# ax.set_ylim(-1.0,1.0)
# set_foregroundcolor(ax,'w')
# set_backgroundcolor(ax,'k')

# #plt.ylabel(r'$N(\epsilon,\tau)$')
# plt.savefig('../r_esc.eps',transparent = True)

xmin = 0.8
xmax = 1.3

E_Ec = 0.99

fig, ax = plt.subplots()
v = generate_orbits(E_Ec, 1.0, 100)
esc_type = ['p_esc' if np.all(np.abs(v[i,:,0])<1.0) else 'r_esc' if np.any(np.abs(v[i,-1,0])>1.0) else 'f_esc' for i in xrange(v.shape[0])]
print 'real =  {}, potential = {}, fake = {}'.format(esc_type.count('r_esc'),esc_type.count('p_esc'),esc_type.count('f_esc'))


i_f_esc = np.where(np.array(esc_type) == 'f_esc')[0]
i_p_esc = np.where(np.array(esc_type) == 'p_esc')[0]
i_r_esc = np.where(np.array(esc_type) == 'r_esc')[0]

ix = np.where(v[i_r_esc,-1,0]>xmax)[0]
print ix.size
for i in i_r_esc[ix]:
     x,y = v[i,:,:2].T
     ax.plot(x[(x>xmin)*(x<xmax)], y[(x>xmin)*(x<xmax)] ,lw=1.5)

x = np.linspace(xmin,xmax,100)
y = esc.get_ymax(x-1,E_Ec,0)
ax.plot(x,y,'--w',x,-y,'--w')
ymax0 = esc.get_ymax(0,E_Ec,0)
ax.plot([1.0,1.0],[-ymax0,ymax0],':w')
ax.plot([-1.0,-1.0],[-ymax0,ymax0],':w')
plt.xlim(xmin, xmax)
plt.ylim(-y.max(), y.max())
ax.axes.get_yaxis().set_visible(False)
set_foregroundcolor(ax,'w')
set_backgroundcolor(ax,'k')
ax.arrow(0.9,0.5,0.2,0,color = 'g', lw = 2.0)
#plt.ylabel(r'$N(\epsilon,\tau)$')
plt.savefig('../r_esc.svg',transparent = True)
