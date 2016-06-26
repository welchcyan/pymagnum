from scipy.cluster.vq import *
import numpy as np
from matplotlib import pyplot as plt

class1 = 1.5 * np.random.randn(100, 2)

class2 = np.random.randn(100, 2) + np.array([8, 8])

features = np.vstack((class1, class2))
centroids, variance = kmeans(features, 2)
code, distance = vq(features, centroids)
plt.figure()

ndx = np.where(code == 1)[0]
plt.plot(features[ndx, 0], features[ndx, 1], '*')

ndx = np.where(code == 0)[0]
plt.plot(features[ndx, 0], features[ndx, 1], 'r.')

plt.plot(centroids[:, 0], centroids[:, 1], 'go')

plt.axis('off')
plt.show()
