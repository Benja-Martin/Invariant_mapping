"""
This script makes the interpolation of K2 and K3 using data from the csv_file.
"""
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tools
import random
import math 

    # .csv file containing data
csv_file = XXXX

    # Initial specimen height
L = XXXX

    # Interpolation and graphing limits
lmbda_min = 0.94
lmbda_max = 1.3
tau_min = 0.00
tau_max = 0.045

    # Iso-values for invariants
K2_max = 1.0 
K2_pas = 0.1
levels_K2 = np.arange(0, K2_max+K2_pas/2, K2_pas)
levels_K3 = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    # Titre général de la figure
suptitle = ''

    # inteprolation and plotting status
statut_interpo = True
statut_affichage = True

x = np.linspace(lmbda_min, lmbda_max, 100)
y = np.linspace(tau_min, tau_max, 100)
x, y = np.meshgrid(x, y)

if statut_interpo:
        # Collecting data
    data = pd.read_csv(csv_file)

        # Conversion from pandas df to numpy array
    U = np.array(data['U'])
    T = np.array(data['T'])
    K2 = np.array(data['K2'])
    K3 = np.array(data['K3'])

        # building lmbda and tau
    lmbda = 1+U/L
    tau = T/(L+U)

        # interpolating K2 and K3 surfaces
    print('K2 interpolation in progress')
    z_K2 = Rbf(lmbda, tau, K2, smooth=0.1, function='multiquadric')
    K2_interpo = z_K2(x, y)
    print('K3 interpolation in progress')
    z_K3 = Rbf(lmbda, tau, K3, smooth=0.1, function='multiquadric')
    K3_interpo = z_K3(x, y)

if statut_affichage:
    print('Plotting in progress')
        # Figure creation
    fig = plt.figure(figsize=(12,5))
    fig.suptitle(suptitle)
    
        # Plotting of K2
    ax_K2 = fig.add_subplot(121)
    contour_K2 = ax_K2.contourf(x, y, K2_interpo, levels=levels_K2, cmap='BuPu')
    cbar_K2 = fig.colorbar(contour_K2, ax=ax_K2)
    cbar_K2.set_ticks(levels_K2)
    ax_K2.set_xlabel(r'$\lambda$')
    ax_K2.set_ylabel(r'$\tau$ [rad.mm$^{-1}$]')
    ax_K2.set_title(r'$K_2$')
    ax_K2.set_xlim(lmbda_min, lmbda_max)
    ax_K2.set_ylim(tau_min, tau_max)
    
        # Plotting of K3
    ax_K3 = fig.add_subplot(122)
    contour_K3 = ax_K3.contourf(x, y, K3_interpo, levels=levels_K3, cmap='coolwarm')
    cbar_K3 = fig.colorbar(contour_K3, ax=ax_K3)
    cbar_K3.set_ticks(levels_K3)
    ax_K3.set_xlabel(r'$\lambda$')
    ax_K3.set_ylabel(r'$\tau$ [rad.mm$^{-1}$]')
    ax_K3.set_title(r'$K_3$')
    ax_K3.set_xlim(lmbda_min, lmbda_max)
    ax_K3.set_ylim(tau_min, tau_max)
    fig.tight_layout()
