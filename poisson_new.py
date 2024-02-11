# -*- coding: utf-8 -*-
"""Poisson2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aeWHuVyIU1m1SDPK7W84Z0jntXjdYn1c
"""

"""# **CALCULAMOS LA MATRIZ DE RIGIDEZ Y EL VECTOR COLUMNA**"""
import numpy as np

def area_tr(P):
  #Fórmula de Heron para el área del elemento triangular
  l1= np.sqrt( (P[0,0]-P[1,0])**2 + (P[0,1] - P[1,1])**2 + (P[0,2] - P[1,2])**2)
  l2= np.sqrt( (P[1,0]-P[2,0])**2 + (P[1,1] - P[2,1])**2 + (P[1,2] - P[2,2])**2)
  l3= np.sqrt( (P[2,0]-P[0,0])**2 + (P[2,1] - P[0,1])**2 + (P[2,2] - P[0,2])**2)
  
  l=np.sort(np.array([l1, l2, l3])) #array en el que ordenamos de menor a mayor los lados
  a= l[2]
  b= l[1]
  c= l[0]
  area=1/4*np.sqrt((a+(b+c))*(c-(a-b))*(c+(a-b))*(a+(b-c)))
  return area
 
def stiffness_matrix(vertices, triangles):
  nvert= vertices.shape[0]
  ntri= triangles.shape[0]
  K= np.zeros((nvert,nvert)) #matriz de rigidez

  for e in range(0, ntri):
    P0= vertices[triangles[e,0],:]
    P1= vertices[triangles[e,1],:]
    P2= vertices[triangles[e,2],:]
    P= np.array([P0, P1, P2])

    area=area_tr(P)

    P_chi= P1-P0   #vector tangente primera coordenada de la parametrización del triángulo
    P_eta= P2-P0   #vector tangente segunda coordenada de la parametrización del triángulo
    nu= 1/(2*area)*np.cross(P_chi, P_eta) #normal unitaria del triángulo
    A= np.array([P_chi, P_eta, nu], dtype=np.float64)
    detA= np.linalg.det(A)

    dcov_phi= np.zeros((3,3)) #gradiente tangencial/ derivada covariante
    dcov_phi[0,:]= 1/detA * np.array([(P_eta[2]-P_chi[2])*nu[1]+(P_chi[1]-P_eta[1])*nu[2], (P_chi[2]-P_eta[2])*nu[0]+(P_eta[0]-P_chi[0])*nu[2], (P_eta[1]-P_chi[1])*nu[0]+(P_chi[0]-P_eta[0])*nu[1]])
    dcov_phi[1,:]= 1/detA * np.array([P_eta[1]*nu[2]-P_eta[2]*nu[1], P_eta[2]*nu[0]-P_eta[0]*nu[2], P_eta[0]*nu[1]-P_eta[1]*nu[0]])
    dcov_phi[2,:]= 1/detA * np.array([P_chi[2]*nu[1]-P_chi[1]*nu[2], P_chi[0]*nu[2]-P_chi[2]*nu[0], P_chi[1]*nu[0]-P_chi[0]*nu[1]])
    for i in range(0,3):
      for j in range(i,3):
        K[triangles[e,i],triangles[e,j]]=K[triangles[e,i],triangles[e,j]]+area*(np.dot(dcov_phi[i,:], dcov_phi[j,:]))
        K[triangles[e,j],triangles[e,i]]=K[triangles[e,i],triangles[e,j]]
  return K

def right_side(F_h, vertices, triangles):
  nvert= vertices.shape[0]
  ntri= triangles.shape[0]
  F= np.zeros(nvert, dtype=np.float64) #vector columna
  for e in range(0, ntri):
    P0= vertices[triangles[e,0],:]
    P1= vertices[triangles[e,1],:]
    P2= vertices[triangles[e,2],:]
    P= np.array([P0, P1, P2])
    x_T = 1/3*P0 + 1/3*P1 + 1/3*P2
    area=area_tr(P)

    for i in range(0,3):
      #Aproximación de la integral F_h*phi_i en el elemento
      F[triangles[e,i]]=F[triangles[e,i]]+area*1/3*F_h(x_T)
  return F

def poisson_SFEM(F_h, vertices, triangles):
  nvert= vertices.shape[0]
  ntri= triangles.shape[0]
  K= stiffness_matrix(vertices, triangles) #matriz de rigidez
  F= right_side(F_h, vertices, triangles) #vector columna
  b= np.zeros(nvert) #vector que usaremos para imponer la condición de media nula

  for e in range(0, ntri):
    for i in range(0,3):
      P0= vertices[triangles[e,0],:]
      P1= vertices[triangles[e,1],:]
      P2= vertices[triangles[e,2],:]
      P= np.array([P0, P1, P2])

      area=area_tr(P)
      b[triangles[e,i]]=b[triangles[e,i]]+area*1/3
      
  #Imponemos la condición de media nula
  K_new=np.zeros((nvert+1,nvert+1))
  K_new[0:nvert,0:nvert]=K
  K_new[nvert,0:nvert]=b
  for i in range(0,nvert+1):
    K_new[i,nvert]=np.sum(K_new[i,0:nvert])

  F_new=np.zeros(nvert+1)
  F_new[0:nvert]=F
  
  #Resolvemos el sistema
  sol1=np.linalg.solve(K_new,F_new)
  constant = sol1[nvert]
  sol2=np.zeros(nvert)
  for i in range(0,nvert):
    sol2[i]=sol1[i]+constant

  return sol2

