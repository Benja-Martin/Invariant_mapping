"""
has to be executed by Abaqus' internal interpreter, to automate simulations and extract data.
This script breaks down into three steps and requires modification by the user. The first step is to run all the
simulations. The second step is to project the calculated values for the Gauss point invariants onto the mesh nodes.
The third step is to extract the data at the node of interest specified by the user. The modifications to be made
by the user are minor: the maximum and minimum values of vertical displacements and torsion angles, and their
associated steps, the path to the .cae file, the name of the initial job, the name of the .odb files to be created, the
name of the specimen, the IDs of the nodes from which the values of macroscopic stresses and invariants will be
extracted, the location of the .odb files and the name of the .csv file where the data will be saved. The user can also
choose which steps will be performed.
WARNING : some versions of Abaqus may not support special or accented characters 
"""
### Importing modules
from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
from odbAccess import *
import numpy as np
executeOnCaeStartup()
print('Importation des modules : OK')

#####################################################################
#####################################################################
#####################################################################

### Simulation step 
    # Vertical displacement min, max and associated step
U_min = -2
U_max = 10
U_pas = 0.1
    # Torsion min, max and associated step
T_min = np.deg2rad(0)
T_max = np.deg2rad(100)
T_pas = np.deg2rad(1)
    # Path for the .cae file
path_cae = XXXX
    # Initial job name
init_job = XXXX
    # Current job name
simu_job = XXXX

### Projection step
    # Sample name
nom_eprouvette = XXXX
	# Node ID and associated element ID for invariants extraction
node_surf_label = XXXX
element_surf_label = XXXX
	# Node ID and associated element ID for inputs extraction
node_input_label = XXXX
element_input_label = XXXX
    # Repository for .odb file 
monRepertoire = XXXX

### Data writing step
    # File where data will be saved
data_save_file = XXXX +'\carte_'+nom_eprouvette+'.csv'

### Etapes a faire
    # Simulations
simu_statut = True
    # Projection
projection_statut = True
    # Ecriture
ecriture_statut = True

#####################################################################
#####################################################################
#####################################################################

if simu_statut:
    ### Useful variables
        # Creating lists of displacement and torsion values
    U_liste = np.arange(U_min, U_max+U_pas/2, U_pas)
    T_liste = np.arange(T_min, T_max+T_pas/2, T_pas)
        # Number of simulations
    N = len(T_liste)
        # Opening .cae file
    openMdb(pathName=path_cae)    
    print('File opening '+path_cae+' : OK')
        # Reset initial conditions to U2=0 and UR2=0
    mdb.models['Model-1'].boundaryConditions['Deplacement'].setValues(amplitude=UNSET, u2=0)
    mdb.models['Model-1'].boundaryConditions['precharge'].setValues(amplitude=UNSET, ur2=0)
        # Time increment modification 
    time_increment = np.round( U_pas/(U_max-U_min) , 3)
    mdb.models['Model-1'].steps['Step-1'].setValues(initialInc=time_increment, minInc=10**-5, maxInc=time_increment)
    print('Simulations to do : '+str(N))
        # Running simulations
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
#####################################################################
#####################################################################

if projection_statut:
    ### Recovering .odb files
        # Initializing the list of .odb files
    fichiers = []
        # Browse all directory files
    for file in os.listdir(monRepertoire):
        # Check if the file ends with '.odb'.
        if file.endswith('.odb'):
            # Add file to list of .odb files
            fichiers.append(os.path.join(monRepertoire, file))
    N = len(fichiers)

    ### Creation of subfields K2 and K3 from UVARM2 and UVARM3
    error = []
    for i,f in enumerate(fichiers):
        try:
            odb = session.openOdb(name=f, readOnly=FALSE)
            step = odb.steps['Step-1']
            for k in range(len(step.frames)):
                frame = step.frames[k]
                try:
                        # Subfield K2 from UVARM2
                    sourceField=frame.fieldOutputs['UVARM2']
                    subField=sourceField.getSubset(position=ELEMENT_NODAL)
                    newField=frame.FieldOutput(name='K2', field=subField)
                except:
                    pass
                try:
                        # Subfield K3 from UVARM3
                    sourceField=frame.fieldOutputs['UVARM3']
                    subField=sourceField.getSubset(position=ELEMENT_NODAL)
                    newField=frame.FieldOutput(name='K3', field=subField)
                except:
                    pass
            odb.save()
            odb.close()
        except:
            error.append(f)
        # Progress 
        print('Projection de K2 et K3 sur les noeuds : '+ str(i+1) + '/' + str(N))
    print('Projections finies : il y a eu '+str(len(error))+' erreur(s)')
    print(error)
        
#####################################################################
#####################################################################
#####################################################################

if ecriture_statut:
    ### Recovering .odb files
        # Initialisation de la liste des fichiers .odb
    fichiers = []
        # Browse all directory files
    for file in os.listdir(monRepertoire):
        # Check if the file ends with '.odb'.
        if file.endswith('.odb'):
            # Add file to list of .odb files
            fichiers.append(os.path.join(monRepertoire, file))
    N = len(fichiers)
    ### Data recovery
        # Opening/Creating the file in which results will be saved
    H = open(data_save_file, 'a')
    H.write('U,T,K2,K3\n')
        # Recuperation of indexes where data must be recovered 
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
        # Data recovery
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
            print('Data writing : ' + str(count+1) + '/' + str(len(fichiers)))
        except:
            N_erreur_ecriture += 1
            print('Erreur')
    H.close()
    print('Data writing : '+str(N_erreur_ecriture)+' error(s)')

#####################################################################
#####################################################################
#####################################################################

print(' ')
print('THE END')
