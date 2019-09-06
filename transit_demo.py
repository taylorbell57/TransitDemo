import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import cv2
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1.axes_divider import make_axes_area_auto_adjustable
import time as timepk

# setup
x = np.arange(0,640)
y = np.arange(0,480)
x, y = np.meshgrid(x, y)
xc = np.median(x)
yc = np.median(y)

rad = 70
bool_mask = np.sqrt((x-xc)**2+(y-yc)**2) < rad
mask = bool_mask.astype(float)*0.75 + 0.25

theta = np.linspace(0, 2*np.pi)
x_ring = rad*np.cos(theta)+xc
y_ring = rad*np.sin(theta)+yc

    
# animation function.  This is called sequentially
def animate(i, vc, im, line, fig, axes, times, sums, bool_mask):
    rval, frame = vc.read()
    frame = frame.sum(axis=2)[:,::-1]
    im.set_array(frame*mask)
    times.append(i)
    sums.append(np.mean(frame*bool_mask))
    line.set_data(times, sums/sums[0])
    axes[1].set_xlim(i-240, i)
#     axes[1].set_ylim(0.9*np.min(sums/np.max(sums)), 1.1)
    fig.canvas.draw()
    return im

def align(time=np.inf):
    try:
        vc = cv2.VideoCapture(0)

        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False

        fig, ax = plt.subplots(nrows=1, ncols=1)

        ax.plot(x_ring, y_ring, c='r', lw=5)
        frame = frame.sum(axis=2)[:,::-1]
        im = ax.imshow(frame*mask, cmap='bone')
        ax.set_xticks([])
        ax.set_yticks([])

        i = 0
        while rval and i<time:
            i += 1
            rval, frame = vc.read()
            frame = frame.sum(axis=2)[:,::-1]
            im.set_array(frame*mask)
            fig.canvas.draw()

        plt.show()
        plt.close()
            
        vc = None
    except:
        rval, frame = vc.read()
        frame = frame.sum(axis=2)[:,::-1]
        im.set_array(frame*mask)
        fig.canvas.draw()
        
        plt.show()
        plt.close()
        
        vc = None
    
def demonstrate(time=np.inf):
    try:
        vc = cv2.VideoCapture(0)

        if vc.isOpened(): # try to get the first frame
            rval, frame = vc.read()
        else:
            rval = False

            
        frame = frame.sum(axis=2)[:,::-1]
        sums = [np.mean(frame*bool_mask)]
        times = [0]

        fig = plt.figure(figsize=(8.5,11/2))
        fig.subplots_adjust(left=0.25, right=0.75)
        gs = gridspec.GridSpec(5, 1)
        ax = plt.subplot(gs[0:-2, 0])
        ax1 = plt.subplot(gs[-2:, 0])
        axes = [ax, ax1]

        axes[0].plot(x_ring, y_ring, c='r', lw=5)
        im = axes[0].imshow(frame*mask, cmap='bone')
        axes[0].set_xticks([])
        axes[0].set_yticks([])

        line, = axes[1].plot(times, sums)
        axes[1].set_ylim(-240, 0)
        axes[1].set_ylim(0.75, 1.1)
#         axes[1].set_ylim(0.9*np.min(sums/np.max(sums)), 1.1)
        axes[1].set_ylabel('Relative Flux')
        axes[1].set_xlabel('Times (seconds)')
        ax2 = axes[1].twinx()
        ax2.set_yticks(axes[1].get_yticks())
        ax2.set_ylim(axes[1].get_ylim())
        

        i = 0
        while rval and i<time:
            i += 1
            im = animate(i, vc, im, line, fig, axes, times, sums, bool_mask)

        plt.show()
        plt.close()

        vc = None
    except:
        if len(times)>len(sums):
            times = times[:-1]
        animate(i, vc, im, line, fig, axes, times, sums, bool_mask)
        
        plt.show()
        plt.close()
        
        vc = None