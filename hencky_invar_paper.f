!DEC$ ATTRIBUTES ALIAS:"uvarm"::UVARM
!!! Subroutine Abaqus permettant de calculer les invariants K_i
!!! du tenseur de Hencky definis par Criscione et al. a partir 
!!! des expressions theoriques sans faire d'hypothese d'incompressibilite.
!!! cf. "Criscione et al. 2000, An invariant basis for natural strain which
!!! yields orthogonal stress response terms in isotropic hyperelasticity"
!!! 
!!! Abaqus subroutine for calculating K_i invariants
!!! of the Hencky tensor defined by Criscione et al. from 
!!! theoretical expressions without making any incompressibility assumptions.
!!! cf. "Criscione et al. 2000, An invariant basis for natural strain which
!!! yields orthogonal stress response terms in isotropic hyperelasticity"
      SUBROUTINE UVARM(UVAR,DIRECT,T,TIME,
     1 DTIME,CMNAME,ORNAME, NUVARM,NOEL,
     2 NPT,LAYER,KSPT,KSTEP,KINC,NDI,NSHR,
     3 COORD,JMAC,JMATYP,MATLAYO,LACCFLA) 
C
      INCLUDE 'ABA_PARAM.INC'
C
      CHARACTER*80 CMNAME,ORNAME
      CHARACTER*3 FLGRAY(15)
      DIMENSION UVAR(NUVARM),DIRECT(3,3)
      DIMENSION T(3,3),TIME(2)
      DIMENSION ARRAY(15),JARRAY(15)
      DIMENSION JMAC(*),JMATYP(*),COORD(*)
      DIMENSION HENCK(6), HENCK_DEV(6), PE(3),PE_DEV(3), ANPE(3,3)
      INTEGER LSTR, NSHR, NDIR	  
      REAL K1, K2, K3
C
!!! Assign 'LE' to HENCK
        CALL GETVRM('LE',ARRAY,JARRAY,FLGRAY,
     1 JRCD,JMAC,JMATYP,MATLAYO,LACCFLA)
C
!!! Hencky strain tensor
      HENCK(1) = ARRAY(1) 
      HENCK(2) = ARRAY(2)
      HENCK(3) = ARRAY(3)
      HENCK(4) = ARRAY(4)
      HENCK(5) = ARRAY(5)
      HENCK(6) = ARRAY(6)
      HENCK(7) = ARRAY(4) !Symmetric tensor
      HENCK(8) = ARRAY(5)
      HENCK(9) = ARRAY(6)
C	  
!!! Parameters for the function SPRIND
      NDIR = 3
      NSHR = 3
      LSTR = 2 ! 2 for the eigenvalues of a
               ! strain tensor
!!! SPRIND is used to compute the eigenvalues 
!!! of a tensor. The result is assigned to PE
      CALL SPRIND(HENCK,PE,ANPE,LSTR,NDIR,NSHR)
C	  
!!! Compute the Ki using the principal
!!! extensions PE
      K1 = PE(1) + PE(2) + PE(3) 
c
!!! Compute the deviatoric part of H
      HENCK_DEV(1) = HENCK(1) - K1/3
      HENCK_DEV(2) = HENCK(2) - K1/3
      HENCK_DEV(3) = HENCK(3) - K1/3
      HENCK_DEV(4) = HENCK(4)
      HENCK_DEV(5) = HENCK(5)
      HENCK_DEV(6) = HENCK(6)
      HENCK_DEV(7) = HENCK(7)
      HENCK_DEV(8) = HENCK(8)
      HENCK_DEV(9) = HENCK(9)
!!! SPRIND is used to compute the eigenvalues 
!!! of a tensor. The result is assigned to PE
      CALL SPRIND(HENCK_DEV,PE_DEV,ANPE,LSTR,NDIR,NSHR)
c
      K2 = ((PE_DEV(1))**2 + (PE_DEV(2))**2 + 
     1     (PE_DEV(3))**2)**0.5
      K3 = 3*(6**0.5)*PE_DEV(1)*PE_DEV(2)*
     1     PE_DEV(3)/(K2**3)	  
C	  
!!! RESULTS
!!! K1, K2, K3
      UVAR(1) = K1
      UVAR(2) = K2
      UVAR(3) = K3
C
      RETURN
      END
	  