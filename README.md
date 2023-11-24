#  Cartographie des invariants (French version, English and Spanish versions below)
Dans ce répertoire se trouvent les outils utilisés pour réaliser la cartographie des invariants K2 et K3. 
Plusieurs fichiers sont à disposition :
  1 - hencky_invar_paper.f
      Une routine UVARM écrite en Fortran pour calculer les invariants K1 ; K2 et K3 du tenseur de Hencky et de son déviateur
      en tout point de Gauss du maillage éléments finis. Aucune hypothèse n'est faite sur l'incompressibilité du matériau il
      est donc possible d'utiliser ce script autant pour un élastomère incompressible que pour une mousse fortement compressible. 
      Ce script est une UVARM pour Abaqus et doit être implémenter dans le Job pour pouvoir être utilisée.
  2 - Simulations.py
      Script Python qui doit êter exécuté par le compilateur interne d'Abaqus. Il permet d'automatiser les simulations et d'extraire
      les données. Le script se décompose en trois étapes qui peuvent êter activée ou non selon les besoins de l'utilisateur. La première
      étape permet d'enchaîner les simulations. La deuxième étape permet de projecter les valeurs des invariants depuis les points de 
      Gauss sur les noeuds du maillage. La troisième étape récupère les valeurs au niveaux des noeuds d'intérêt. 
      L'utilisateur doit spécifier plusieurs choses au début du script : les valeurs minimales et maximale de déplcament vertical et
      d'angle de torsion ainsi que les pas associés, les chemins vers le fichier .cae et versle répertoire contenant les .odb, le nom
      de l'éprouvette, du job initial, des jobs courants et le nom du fichier .csv qui sera créé pour stocker les données.
      L'utilisateur doit aussi saisir l'ID du noeud et un élément associé pour définir là où seront extraites les valeurs des invariants
      et l'ID et un élement associé pour définir où seront extraites les valeurs de déplacement et de rotation. Par exemple pour une
      éprouvette AE2 les invariants seront extraits sur la surface de la section nominale et les déplacements/rotations seront extraites
      sur la face supérieure de l'éprouvette. 
  3 - Interpolation.py
      Script Python qui permet d'exploiter les données contenues dans le fichier .csv obtenu à la fin de l'étape précédente. Ce script
      fait appel au module scipy.optimize et à la fonction Rbf() qui permet d'interpoler une surface à partir de liste 1D en utilisant 
      les fonctions de base radiale. L'inteprolation est, par défaut dans ce script, réalisée en utilisant les fonction multiquadratiques.

#  Mapping of invariants (English version, Spanish version below)
This repository contains the tools used to map K2 and K3 invariants. Several files are available:
  1 - hencky_invar_paper.f
      A UVARM routine written in Fortran to calculate the invariants K1; K2 and K3 from the Hencky tensor and its
      deviator at any Gauss point of the nite element mesh.
  2 - Simulations.py
      A script written in Python and executed by Abaqus' internal interpreter, to automate simulations and extract data.
      This script breaks down into three steps and requires modication by the user. The first step is to run all the
      simulations. The second step is to project the calculated values for the Gauss point invariants onto the mesh nodes.
      The third step is to extract the data at the node of interest specified by the user. The modications to be made
      by the user are minor: the maximum and minimum values of vertical displacements and torsion angles, and their
      associated steps, the path to the .cae file, the name of the initial job, the name of the . odb files to be created, the
      name of the specimen, the IDs of the nodes from which the values of macroscopic stresses and invariants will be
      extracted, the location of the .odb files and the name of the .csv file where the data will be saved. The user can also
      choose which steps will be performed. In the case of this work, the invariant values are extracted at the level of the
      nominal section surface, and the load values are extracted at the level of the specimen top face.
  3 - Interpolation.py
      A script written in Python using the .csv le created in the previous step extracts the data and uses an interpolation
      function to create the surfaces associated with each invariant and project it into the λ − τ plane. Interpolation is
      performed using the multiquadratic radial-based functions implemented in Python's Scipy.interpolate module.

#  Cartografia de invariantes (Spanish version - Traduction made with DeepL at deep.com)
Este repositorio contiene las herramientas utilizadas para mapear invariantes K2 y K3. Hay varios archivos disponibles:
  1 - hencky_invar_paper.f
      Una rutina UVARM escrita en Fortran para calcular los invariantes K1, K2 y K3 a partir del tensor de Hencky y su
      desviador en cualquier punto de Gauss de la malla de elementos nitos.
  2 - Simulations.py
      Un script escrito en Python y ejecutado por el intérprete interno de Abaqus, para automatizar simulaciones y extraer datos.
      Este script se divide en tres pasos y requiere modificación por parte del usuario. El primer paso es ejecutar todas las simulaciones.
      El segundo paso es proyectar los valores calculados para los invariantes del punto de Gauss en los nodos de la malla. El tercer paso
      consiste en extraer los datos en el nodo de interés especificado por el usuario. Las modificaciones a realizar por el usuario son menores:
      los valores máximos y mínimos de desplazamientos verticales y ángulos de torsión, y sus pasos asociados, la ruta al .cae le, el nombre del
      trabajo inicial, el nombre de los .odb les a crear, el nombre del espécimen, los IDs de los nodos de los que se extraerán los valores de
      tensiones macroscópicas e invariantes, la ubicación de los .odb les y el nombre del .csv le donde se guardarán los datos. El usuario
      también puede elegir qué pasos se llevarán a cabo. En el caso de este trabajo, los valores de las invariantes se extraen a nivel de la
      superficie nominal de la sección, y los valores de las cargas se extraen a nivel de la cara superior de la probeta.
  3 - Interpolation.py
       Un script escrito en Python utilizando el .csv le creado en el paso anterior extrae los datos y utiliza una función de interpolación para
       crear las superficies asociadas a cada invariante y proyectarlas en el plano λ - τ. La interpolación se realiza utilizando las funciones
       multicuadráticas de base radial implementadas en el módulo Scipy.interpolate de Python.      
