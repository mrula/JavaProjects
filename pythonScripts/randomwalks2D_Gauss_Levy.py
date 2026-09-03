# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 12:14:02 2025

@author: larsen
"""

### 2D random walk and Lévy flight

import numpy as np
import matplotlib.pyplot as plt
import scipy

# 2D domain
x = np.linspace(-1.0, 1.0, 200)
y = x

# Number of markers (particles)
n = 10000

# Initial location of markers. n rows (# of markers), two columns (x and y location)
minit = np.zeros((n,2))

## Draw 'nsteps' random step sizes from a given distribution (either Gaussian or Lévy alpha-stable)
nsteps = 1000

#%% Random walk from normal Gaussian steps

# Draw steps in x direction
xsteps = np.random.normal(loc=np.zeros((n,nsteps)), scale=np.ones((n,nsteps))*1e-2, size=(n,nsteps))
xtotstep = np.sum(xsteps, axis=1)

# Draw steps in y direction
ysteps = np.random.normal(loc=np.zeros((n,nsteps)), scale=np.ones((n,nsteps))*1e-2, size=(n,nsteps))
ytotstep = np.sum(ysteps, axis=1)

mRW = minit + np.array([xtotstep, ytotstep]).T

plt.figure()
plt.scatter(mRW[:,0], mRW[:,1])
plt.title('Random walk')


#%% Lévy flight from Lévy alpha-stable steps

from scipy.stats import levy_stable, norm

# Lévy alpha-stable distribution parameters
alpha = 1.8
beta  = 0.0

# Draw steps in x direction
# xsteps = np.minimum(np.maximum(levy_stable.rvs(alpha, beta, size=(n,nsteps)), -10*np.ones((n,nsteps))), 10*np.ones((n,nsteps)))
rsteps = levy_stable.rvs(alpha, beta, size=(n,nsteps))

# Draw steps in y direction
# ysteps = np.minimum(np.maximum(levy_stable.rvs(alpha, beta, size=(n,nsteps)), -10*np.ones((n,nsteps))), 10*np.ones((n,nsteps)))
phisteps = np.random.uniform(low=0.0, high=2*np.pi, size=(n,nsteps))

# Convert to Cartesian coordinates
xsteps = rsteps*np.cos(phisteps)
ysteps = rsteps*np.sin(phisteps)

xtotstep = np.sum(xsteps, axis=1)
ytotstep = np.sum(ysteps, axis=1)

mLF = minit + np.array([xtotstep, ytotstep]).T

plt.figure()
plt.scatter(mLF[:,0], mLF[:,1])
plt.title('Lévy flight')


#%%
# Plot Lévy alpha-stable distribution pdf versus normal distribution
plt.figure()
plt.plot(np.linspace(-10, 10, 1000), levy_stable.pdf(np.linspace(-10, 10, 1000), alpha, beta))
plt.plot(np.linspace(-10, 10, 1000), levy_stable.pdf(np.linspace(-10, 10, 1000), 2, beta))
plt.plot(np.linspace(-10, 10, 1000), norm.pdf(np.linspace(-10, 10, 1000), loc=0, scale=np.sqrt(2)))
plt.legend(('Lévy alpha-stable, alpha=1.8', 'Lévy alpha stable, alpha=2', 'Normal, variance sqrt(2)'))
plt.yscale('log')


#%% Follow only a few markers

# Number of markers (particles)
n = 100000

## Draw 'nsteps' random step sizes from a given distribution (either Gaussian or Lévy alpha-stable)
nsteps = 100

#%% Random walk from normal Gaussian steps

# Initial location of markers. n rows (# of markers)
xlocs = np.zeros((n,1))
ylocs = np.zeros((n,1))

for i in range(nsteps):
    # Draw steps in x direction
    xstep = np.random.normal(loc=np.zeros((n,1)), scale=np.ones((n,1))*np.sqrt(2), size=(n,1))
    xstep = np.random.normal(loc=np.zeros((n,1)), scale=np.ones((n,1)), size=(n,1))
    xlocs = np.concatenate((xlocs, xlocs[:,-1].reshape((n,1))+xstep), axis=1)
    # Draw steps in y direction
    ystep = np.random.normal(loc=np.zeros((n,1)), scale=np.ones((n,1))*np.sqrt(2), size=(n,1))
    ystep = np.random.normal(loc=np.zeros((n,1)), scale=np.ones((n,1)), size=(n,1))
    ylocs = np.concatenate((ylocs, ylocs[:,-1].reshape((n,1))+ystep), axis=1)

fig, ax = plt.subplots()
ax.plot(xlocs[0,:].T, ylocs[0,:].T)
ax.set_title('Random walk')
ax.set_xlabel('x', size=12)
ax.set_ylabel('y', size=12)
ax.set_aspect('equal')
ax.set_xlim([-20, 20])
ax.set_ylim([-20, 20])
plt.tight_layout()

# Evaluate mean squared distance from origin
msqd = np.mean((xlocs - xlocs[:,0].reshape((n,1)))**2 + (ylocs - ylocs[:,0].reshape((n,1)))**2, axis=0)

# Plot mean squared distance with respect to time
plt.figure()
plt.plot(np.linspace(1,len(msqd),len(msqd)), msqd, '-o')
plt.plot(np.linspace(1,len(msqd),len(msqd)), np.linspace(1,len(msqd),len(msqd))*2*np.sqrt(2)**2, '-')
plt.plot(np.linspace(1,len(msqd),len(msqd)), np.linspace(1,len(msqd),len(msqd))*2, '-')


#%% Lévy flight from Lévy alpha-stable steps

from scipy.stats import levy_stable

# Initial location of markers
xlocs = np.zeros((n,1))
ylocs = np.zeros((n,1))

# Lévy alpha-stable distribution parameters
alpha = 1.5
beta  = 0.0

for i in range(nsteps):
    # Draw steps in x direction
    # xsteps = np.minimum(np.maximum(levy_stable.rvs(alpha, beta, size=(n,nsteps)), -10*np.ones((n,nsteps))), 10*np.ones((n,nsteps)))
    rstep = levy_stable.rvs(alpha, beta, size=(n,1))

    # Draw steps in y direction
    # ysteps = np.minimum(np.maximum(levy_stable.rvs(alpha, beta, size=(n,nsteps)), -10*np.ones((n,nsteps))), 10*np.ones((n,nsteps)))
    phistep = np.random.uniform(low=0.0, high=2*np.pi, size=(n,1))

    # Convert to Cartesian coordinates
    xstep = rstep*np.cos(phistep)
    ystep = rstep*np.sin(phistep)
    
    # Take step
    xlocs = np.concatenate((xlocs, xlocs[:,-1].reshape((n,1))+xstep), axis=1)
    ylocs = np.concatenate((ylocs, ylocs[:,-1].reshape((n,1))+ystep), axis=1)

fig, ax = plt.subplots()
ax.plot(xlocs[0,:].T, ylocs[0,:].T)
ax.set_title('Lévy flight')
ax.set_xlabel('x', size=12)
ax.set_ylabel('y', size=12)
ax.set_aspect('equal')
ax.set_xlim([-20, 20])
ax.set_ylim([-20, 20])
plt.tight_layout()

# Evaluate mean squared distance
# msqd = np.mean(np.cumsum(np.diff(xlocs, axis=1)**2 + np.diff(ylocs, axis=1)**2, axis=1), axis=0)
msqd = np.mean((xlocs - xlocs[:,0].reshape((n,1)))**2 + (ylocs - ylocs[:,0].reshape((n,1)))**2, axis=0)

# Plot mean squared distance with respect to time
plt.figure()
plt.plot(np.linspace(1,len(msqd),len(msqd)), msqd, '-o')
plt.plot(np.linspace(1,len(msqd),len(msqd)), 2*np.pi*(np.linspace(1,len(msqd),len(msqd)))**(2/alpha), '-') # 2/alpha from Effenberger et al 2024 A&A, also from Levy flights wiki