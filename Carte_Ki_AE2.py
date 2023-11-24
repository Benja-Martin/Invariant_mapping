"""
Script Python permettant d'avoir la cartographie de notre éprouvette de géométrie AE2
Il y a deux étapes qui peuvent être effectuées ou non selon la variable statut_xxx
La première étape est l'interpolation des surfaces K2 et K3 
La deuxième étape est l'affichage de la cartographie. Il est possible d'afficher les données 
brutes et les données d'interpolation.
L'utilisateur peut changer :
    les limites du graphique avec les variables lmbda_min, lmbda_max, tau_min et tau_max
    les iso-K2 et iso-K3 avec les listes levels_K2 et levels_K3
    les valeurs de K3 qui doivent être interpolées avec K3_valeurs et tol_fit
Pour éviter des problèmes de mémoire et de temps de calcul seule une partie de la base de données est utilisée
et la variable pas permet de gérer la proportion de la base de données qui est utilisée. 
Attention à la forme du jeu de données, ici il est supposé qu'il est de la forme suivante :
U,T,K2,K3
x,x,x,x
x,x,x,x
...
x,x,x,x
La fonction d'interpolations des K3 gFunction n'est pas forcement la plus pertiente elle peut être adaptée selon les besoins    
"""
#%%
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tools
import random
import math 

    # Fonction d'interpolation des iso-K3
def gFunction(x, a, b, c, d, e):
    return a*np.log(x)**b+c*(x-1)**d
# def gFunction(x, a, b, c, d):
#     return a*np.log(x)**b+c*np.sqrt(x)**d
# Fonction qui réduit la taille des listes en prenant des points tous les pas
def reduce(L, pas=10):
    L_red = []
    for k in range(0, len(L), pas):
        L_red.append(L[k])
    return np.asarray(L_red)

# Hauteur initiale de l'éprouvette
L = 30

pas = 1
    # Limites de l'interpolation et du graphique
lmbda_min = 0.94
lmbda_max = 1.3
tau_min = 0.00
tau_max = 0.045
    # Iso-valeurs pour les interpolations
levels_K2 = [np.round(0.2*k,1) for k in range(0, 12+1)]
levels_K3 = [np.round(0.1*k, 1) for k in range(-10, 10+1)]
    # Titre général de la figure
suptitle = 'Cartographie AE2'
    # Affichage des iso-K3 : valeur, tolerance, lmbda_max pour le tracer
K3_valeurs = [[1, 10**-3, 1.35]]
tol_fit = 0.0001
    # Affichage des données brutes associées aux iso-K3
affichage_data_brute = False
affichage_data_interpo = False

statut_interpo = False
statut_affichage = True

x = np.linspace(lmbda_min, lmbda_max, 100)
y = np.linspace(tau_min, tau_max, 100)
x, y = np.meshgrid(x, y)

if statut_interpo:
    # Récupération des données 
    data = pd.read_csv(r'D:\Comparaison LDC\ArrudaBoyce\L1_M01\carte_AE2_L1_M01.csv')

    # Conversion des données en np.array
    U = np.array(data['U'])
    T = np.array(data['T'])
    K2 = np.array(data['K2'])
    K3 = np.array(data['K3'])

    # Construction des listes lmbda et tau
    lmbda = 1+U/L
    tau = T/(L+U)
    # Fusionner les quatre listes d'origine et les lmbda et tau en une seule liste de tuples
    liste_tuples = list(zip(U, T, K2, K3, lmbda, tau))

    # Trier la liste de tuples en fonction du premier élément de chaque tuple
    liste_tuples_triee = sorted(liste_tuples, key=lambda x: x[0])

    # Supprimer les tuples identiques
    # Eliminer les tuples dont les deux premières entrées sont identiques et si K3 est NaN
    liste_tuples_triee_filtree = []
    for i in range(len(liste_tuples_triee)):
        if not(math.isnan(liste_tuples_triee[i][3])):
            if i == 0 or liste_tuples_triee[i][:2] != liste_tuples_triee[i-1][:2]:
                liste_tuples_triee_filtree.append(liste_tuples_triee[i])
    # Séparer la liste triée et filtrée en quatre listes distinctes
    U_triee, T_triee, K2_triee, K3_triee, lmbda_triee, tau_triee = zip(*liste_tuples_triee_filtree)
    print('Doublons éliminés')

    ### Mélange les quatres listes en gardant les tuples dans le même ordre
    fusion = list(zip(U_triee, T_triee, K2_triee, K3_triee, lmbda_triee, tau_triee))
    random.shuffle(fusion)
    U_random, T_random, K2_random, K3_random, lmbda_random, tau_random = zip(*fusion)
    print('Tuples de données mélangés')


    # Réduction de la taille des listes
    U_red = reduce(U_random, pas)
    T_red = reduce(T_random, pas)
    K2_red = reduce(K2_random, pas)
    K3_red = reduce(K3_random, pas)
    lmbda_red = reduce(lmbda_random, pas)
    tau_red = reduce(tau_random, pas)
    print(f'Reduction du jeu de données à {np.round(len(U_red)/len(U_random)*100, 2)}%')


    # Interpolation des surfaces K2 et K3
    print('Interpolation des $K_2$')
    z_K2 = Rbf(lmbda_red, tau_red, K2_red, smooth=0.1, function='multiquadric')
    print('Interpolation des $K_3$')
    z_K3 = Rbf(lmbda_red, tau_red, K3_red, smooth=0.1, function='multiquadric')

    print('Affichage en cours')
    # Affichage des surfaces
    levels_K2 = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6]
    levels_K3 = [-1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    K2_interpo = z_K2(x, y)
    K3_interpo = z_K3(x, y)
    

if statut_affichage:
    ### Affichage de la cartographie
    print('Affichage en cours')
    fig = plt.figure(figsize=(12,10))
    fig.suptitle(suptitle)
        # Affichage des K2
    ax_K2 = fig.add_subplot(221)
    ax_K2.contourf(x,  y, K2_interpo, levels=levels_K2, cmap='BuPu')
    ax_K2.contourf(x, -y, K2_interpo, levels=levels_K2, cmap='BuPu')
    contour_K2 = ax_K2.contourf(x, y, K2_interpo, levels=levels_K2, cmap='BuPu')
    cbar_K2 = fig.colorbar(contour_K2, ax=ax_K2)
    tick_locations = levels_K2
    cbar_K2.set_ticks(tick_locations)
    ax_K2.set_xlabel(r'$\lambda$')
    ax_K2.set_ylabel(r'$\tau$ (rad.mm$^{-1}$)')
    ax_K2.set_title(r'$K_2$')
    ax_K2.set_xlim(lmbda_min, lmbda_max)
    ax_K2.set_ylim(tau_min, tau_max)
        # Affichage des K3
    ax_K3 = fig.add_subplot(222)
    contour_K3 = ax_K3.contourf(x, y, K3_interpo, levels=levels_K3, cmap='coolwarm')
    contour_K3 = ax_K3.contourf(x,-y, K3_interpo, levels=levels_K3, cmap='coolwarm')
    cbar_K3 = fig.colorbar(contour_K3, ax=ax_K3)
    cbar_K3.set_ticks(levels_K3)
    ax_K3.set_xlabel(r'$\lambda$')
    ax_K3.set_ylabel(r'$\tau$ (rad.mm$^{-1}$)')
    ax_K3.set_title(r'$K_3$')
    ax_K3.set_xlim(lmbda_min, lmbda_max)
    ax_K3.set_ylim(tau_min, tau_max)
        # Affichage de la cartographie générale
    ax_carto = fig.add_subplot(212)
    contour_K3_carto = ax_carto.contourf(x, y, K3_interpo, levels=levels_K3, cmap='coolwarm')
    contour_K2_carto = ax_carto.contour(x, y, K2_interpo, levels=levels_K2, colors='black', alpha=0.5)
    contour_K3_carto = ax_carto.contourf(x, -y, K3_interpo, levels=levels_K3, cmap='coolwarm')
    contour_K2_carto = ax_carto.contour(x, -y, K2_interpo, levels=levels_K2, colors='black', alpha=0.5)
    cbar_K3_carto = fig.colorbar(contour_K3_carto, ax=ax_carto)
    cbar_K3_carto.set_ticks(levels_K3)
    cbar_K3_carto.set_label('$K_3$', fontsize=15)
    ax_carto.set_title('Cartographie générale')
    ax_carto.set_xlim(lmbda_min, lmbda_max)
    ax_carto.set_ylim(tau_min, tau_max)
    ax_carto.set_xlabel(r'$\lambda$')
    ax_carto.set_ylabel(r'$\tau$ (rad.mm$^{-1}$)')
        # Affichage des iso-K3
    for val, tol, lmbda_max in K3_valeurs:
            # Récupération des données brutes
        if affichage_data_brute:
            lmbda_indices = []
            tau_indices = []
            for k in range(len(U)):
                if val-tol <= K3[k] and K3[k] <= val+tol:
                    lmbda_indices.append(lmbda[k])
                    tau_indices.append(tau[k])
            ax_carto.plot(lmbda_indices, tau_indices, '.g')
            # Fitting avec les données de l'interpolation
        try:
            indices = np.where(np.abs(K3_interpo-val) <= tol)
            popt, _ = tools.Fitting(gFunction, x[indices], y[indices], maxfev=10**6)
            lmbda_fit = np.linspace(1, lmbda_max, 51)
            ax_carto.plot(lmbda_fit, gFunction(lmbda_fit, *popt), '--k', linewidth=4)
            ax_K3.plot(lmbda_fit, gFunction(lmbda_fit, *popt), '--k', linewidth=4)
            if affichage_data_interpo:
                ax_carto.plot(x[indices], y[indices], '.b')
            print('Les coefficients associés à K3='+str(val)+'sont :')
            print(popt)
        except:
            pass
        # Textes pour les iso-K3 affichées
            # Graphique iso-K3
    # ax_K3.text(1.13, 0.014, '$K_3=1$')
    # ax_K3.text(1.02, 0.070, '$K_3=0$')
    #         # Graphique carto générale
    # ax_carto.text(1.13, 0.014, '$K_3=1$')
    # ax_carto.text(1.02, 0.070, '$K_3=0$')

    ax_carto.set_xlim(lmbda_min, lmbda_max)
    ax_K3.set_xlim(lmbda_min, lmbda_max)
    ax_K2.set_xlim(lmbda_min, lmbda_max)

    fig.tight_layout()
    
#%%
tau_fit = gFunction(lmbda_fit, *popt)
ax_carto.plot(lmbda_fit, tau_fit, '.g')


