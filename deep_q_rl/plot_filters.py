""" Utility to plot the first layer of convolutions learned by
the Deep q-network.

Usage:

plot_filters.py PICKLED_NN_FILE
"""

import sys
import matplotlib.pyplot as plt
import cPickle

net_file = open(sys.argv[1], 'r')
network = cPickle.load(net_file)
print network
layer = int(sys.argv[2])
w = network.q_layers[layer].W.get_value()
count = 1
for f in range(w.shape[3]):
    for c in range(w.shape[0]):
        plt.subplot(w.shape[3], w.shape[0], count)
        img = w[c, :, :, f]
        plt.imshow(img, vmin=img.min(), vmax=img.max(),
                   interpolation='none', cmap='gray')
        plt.xticks(())
        plt.yticks(())
        count += 1
#Till the time the plt.show() doesn't work
plt.savefig(sys.argv[3]+".png")
import os
os.system("eog "+sys.argv[3]+".png")
#The correct one
#plt.show()