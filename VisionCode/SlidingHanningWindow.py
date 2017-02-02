from scipy import stats
from scipy import linalg
import numpy as np
import matplotlib.pyplot as plt
N = 1996
threshold = 20
breakinto = 8
loop =int(N/threshold)
windowlen = 400
x = [0 for h in range(0,N)]
w = [0 for h in range(0,N)]
a = [0 for h in range(0,threshold)]
b = [0 for h in range(0,threshold)]
e = [0 for h in range(0,threshold)]
windows = [0 for h in range(0,breakinto*windowlen)]
window = [0 for h in range(0,windowlen)]
x2 = [0 for h in range(0,breakinto*windowlen)]
x3 = [0 for h in range(0,windowlen)]
z = np.linspace(0,2*np.pi,N)
y = np.sin(z) + np.random.random(N) * 0.009
for g in range(0,N):
    x[g] = g
for g in range(0,breakinto*windowlen):
    x2[g] = g
for c in range(0,loop):
    for d in range(0, threshold):
        a[d] = y[d+threshold*c]
        b[d] = x[d+threshold*c]
    slope, intercept, r_value, p_value, std_err = stats.linregress(b,a)
    for f in range(0, threshold):
        e[f] = slope*(f+threshold*c) + intercept
        w[f+threshold*c] = e[f]

for j in range(0,breakinto):
    for k in range(0,windowlen):
        window[k] = w[k + int(windowlen-171.429)*j] * 0.5 * (1 - np.cos((2 * np.pi * k)/ (N - 1)));
        x3[k] = k + int(windowlen-171.429)*j
        a = np.cov(x3)
        e_vals, e_vecs = linalg.eig(A)

    plt.plot(x3,window)
plt.plot(x,w)
plt.plot(x,y)
plt.show()



