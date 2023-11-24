"""
Script Python permettant de faire des simulations multiples sur 
une eprouvette de type AE2 dans le SBR caracterise, de projecter 
les invariants K2 et K3 sur les noeuds et d'extraire et d'ecrire 
les donnees qui nous interessent. 
"""
### Import des modules 
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from odbAccess import *
import numpy as np
executeOnCaeStartup()
print('Importation des modules : OK')

#####################################################################

### Donnees des simulations
    # Deplacemements qui seront imposes
U_min = -2
U_max = 10
U_pas = 0.1
    # Torsion qui seront imposees
T_min = np.deg2rad(0)
T_max = np.deg2rad(100)
T_pas = np.deg2rad(1)
    # Chemin vers le fichier .cae
path_cae = r'D:\Comparaison LDC\ArrudaBoyce\L1_M01\AE2_AB_L1_M01.cae'
    # Nom du job initial
init_job = 'Job-1'
simu_job = 'Job-AE2_L1_M01_'

### Projection K2 et K3
    # Nom de l'eprouvette
nom_eprouvette = 'AE2_L1_M01_'
	# Noeud en surface de la section nominale et element associe
node_surf_label = 1
element_surf_label = 1
	# Noeud sur la surface superieure et element associe
node_input_label = 11853
element_input_label = 3848
    # Repertoire ou sont les .odb
monRepertoire = r'D:\Comparaison LDC\ArrudaBoyce\L1_M01\Simulations'

### Ecriture des donnees
    # Fichier ou les donnees seront sauvegardees
data_save_file = r'D:\Comparaison LDC\ArrudaBoyce\L1_M01\carte_'+nom_eprouvette+'.csv'

### Etapes a faire
    # Simulations
simu_statut = False
    # Projection
projection_statut = False
    # Ecriture
ecriture_statut = True


#####################################################################

if simu_statut:
    ### Simulations mutliples
        # Construction des listes des valeurs de deplacement et de torsion
    U_liste = np.arange(U_min, U_max+U_pas/2, U_pas)
    T_liste = np.arange(T_min, T_max+T_pas/2, T_pas)
        # Nombre de simulation
    N = len(T_liste)
        # Ouverture du fichier CAE
    openMdb(pathName=path_cae)    
    print('Ouverture du fichier '+path_cae+' : OK')
        # Reinitialisation des conditions initiales a U2=0 et UR2=0
    mdb.models['Model-1'].boundaryConditions['Deplacement'].setValues(amplitude=UNSET, u2=0)
    mdb.models['Model-1'].boundaryConditions['precharge'].setValues(amplitude=UNSET, ur2=0)
        # Modification de l'increment de temps
    time_increment = np.round( U_pas/(U_max-U_min) , 3)
    mdb.models['Model-1'].steps['Step-1'].setValues(initialInc=time_increment, minInc=10**-5, maxInc=time_increment)
    
        # Enchainement des simulations
    i = 0
    for t in T_liste:
        mdb.models['Model-1'].boundaryConditions['precharge'].setValues(amplitude=UNSET, ur2=t, u2=U_min)
        mdb.models['Model-1'].boundaryConditions['Deplacement'].setValues(amplitude=UNSET, ur2=t, u2=U_max)
        mdb.jobs.changeKey(fromName=init_job, toName=simu_job+str(i))
        mdb.jobs[simu_job+str(i)].submit(consistencyChecking=OFF)
        mdb.jobs[simu_job+str(i)].waitForCompletion()
        mdb.jobs.changeKey(fromName=simu_job+str(i), toName=init_job)
        i += 1
        print('Simulations : ' + str(i) + '/' + str(N))
        
#####################################################################

if projection_statut:
    ### Recuperation des fichiers .odb
        # Initialisation de la liste des fichiers .odb
    fichiers = []
        # Parcours de tous les fichiersdu repertoire
    for file in os.listdir(monRepertoire):
        # Verification si le fichier se termine par '.odb'
        if file.endswith('.odb'):
            # Ajout du fichier a la liste des fichiers .odb
            fichiers.append(os.path.join(monRepertoire, file))
    N = len(fichiers)

    ### Creation des subfield K2 et K3 a partir des UVARM2 et UVARM3
    error = []
    for i,f in enumerate(fichiers):
        try:
            odb = session.openOdb(name=f, readOnly=FALSE)
            step = odb.steps['Step-1']
            for k in range(len(step.frames)):
                frame = step.frames[k]
                try:
                        # Subfield K2 a partir de UVARM2
                    sourceField=frame.fieldOutputs['UVARM2']
                    subField=sourceField.getSubset(position=ELEMENT_NODAL)
                    newField=frame.FieldOutput(name='K2', field=subField)
                except:
                    pass
                try:
                        # Subfield K3 a partir de UVARM3
                    sourceField=frame.fieldOutputs['UVARM3']
                    subField=sourceField.getSubset(position=ELEMENT_NODAL)
                    newField=frame.FieldOutput(name='K3', field=subField)
                except:
                    pass
            odb.save()
            odb.close()
        except:
            error.append(f)
        # Avancement 
        print('Projection de K2 et K3 sur les noeuds : '+ str(i+1) + '/' + str(N))
    print('Projections finies : il y a eu '+str(len(error))+' erreur(s)')
    print(error)
        
#####################################################################

if ecriture_statut:
    ### Recuperation des fichiers .odb
        # Initialisation de la liste des fichiers .odb
    fichiers = []
        # Parcours de tous les fichiersdu repertoire
    for file in os.listdir(monRepertoire):
        # Verification si le fichier se termine par '.odb'
        if file.endswith('.odb'):
            # Ajout du fichier a la liste des fichiers .odb
            fichiers.append(os.path.join(monRepertoire, file))
    N = len(fichiers)
    ### Recuperation des donnees
        # Ouverture/Creation du fichier dans lequel seront sauvegarde les resultats
    H = open(data_save_file, 'a')
    H.write('U,T,K2,K3\n')
        # Recuperation des indices ou il faut recuperer les donnees 
    ff = session.openOdb(fichiers[0])
    step  = ff.steps['Step-1']
    K2  = ff.steps['Step-1'].frames[0].fieldOutputs['K2']
    U  = ff.steps['Step-1'].frames[0].fieldOutputs['U']
    indice_input = 0
    indice_donnees = 0
    for i in range(len(U.values)):
        if U.values[i].nodeLabel==node_input_label:
            indice_input = i
    for i in range(len(K2.values)):
        if K2.values[i].elementLabel==element_surf_label:
            if K2.values[i].nodeLabel==node_surf_label:
                indice_donnees = i
    ff.close()
        # Recuperation des donnees
    N_erreur_ecriture = 0
    for count, f in enumerate(fichiers):
        try:
            ff = session.openOdb(f)
            step  = ff.steps['Step-1']
            for k in range(1, len(step.frames)):
                U2  = ff.steps['Step-1'].frames[k].fieldOutputs['U'].values[indice_input].data[1]
                UR2 = ff.steps['Step-1'].frames[k].fieldOutputs['UR'].values[indice_input].data[0]
                K2  = ff.steps['Step-1'].frames[k].fieldOutputs['K2'].values[indice_donnees].data
                K3  = ff.steps['Step-1'].frames[k].fieldOutputs['K3'].values[indice_donnees].data
                H.write(str(U2)+','+str(UR2)+','+str(K2)+','+str(K3)+'\n')
            ff.close()
            print('Ecriture des donnees : ' + str(count+1) + '/' + str(len(fichiers)))
        except:
            N_erreur_ecriture += 1
            print('Erreur')
    H.close()
    print('Ecriture des donnees : '+str(N_erreur_ecriture)+' erreur(s)')

############################

print(' ')
print('FINI')
