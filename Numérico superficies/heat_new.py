import numpy as np
import poisson_new 

def area_tr(P):
  #Fórmula de Heron para el área del elemento triangular
  l1= np.sqrt((P[0,0]-P[1,0])**2 + (P[0,1] - P[1,1])**2 + (P[0,2] - P[1,2])**2)
  l2= np.sqrt((P[1,0]-P[2,0])**2 + (P[1,1] - P[2,1])**2 + (P[1,2] - P[2,2])**2)
  l3= np.sqrt((P[2,0]-P[0,0])**2 + (P[2,1] - P[0,1])**2 + (P[2,2] - P[0,2])**2)
  
  l=np.sort(np.array([l1, l2, l3])) #array en el que ordenamos de menor a mayor los lados
  a= l[2]
  b= l[1]
  c= l[0]
  area=1/4*np.sqrt((a+(b+c))*(c-(a-b))*(c+(a-b))*(a+(b-c)))
  return area

def mass_matrix(vertices, triangles):
    nvert= vertices.shape[0]
    ntri= triangles.shape[0]
    M= np.zeros((nvert, nvert))
    for e in range(0, ntri):
        P0= vertices[triangles[e,0],:]
        P1= vertices[triangles[e,1],:]
        P2= vertices[triangles[e,2],:]
        P= np.array([P0, P1, P2])

        area= area_tr(P)

        for i in range(0,3):
            for j in range(i,3):
                if i==j:
                    M_el= area*(1/6)
                else:
                    M_el= area*(1/12)
                M[triangles[e,i],triangles[e,j]]=M[triangles[e,i],triangles[e,j]]+M_el
                M[triangles[e,j],triangles[e,i]]=M[triangles[e,i],triangles[e,j]]

    return M

def right_side(dt, t_j, M, u, F_h, vertices, triangles):
    nvert= vertices.shape[0]
    ntri= triangles.shape[0]
    F= np.zeros(nvert)
    right= np.zeros(nvert)
    for e in range(0, ntri):
        P0= vertices[triangles[e,0],:]
        P1= vertices[triangles[e,1],:]
        P2= vertices[triangles[e,2],:]
        P= np.array([P0, P1, P2])
        x_T = 1/3*P0 + 1/3*P1 + 1/3*P2
        area=area_tr(P)

        for i in range(0,3):
            #Aproximación de la integral F_h*phi_i en el elemento
            F[triangles[e,i]]=F[triangles[e,i]]+area*(1/3)*F_h(t_j, x_T)
    
    right= np.dot(M,u) + dt*F
    return right


def heat_SFEM(intervalo,  dt, F_h, u0, vertices, triangles):
    nvert= vertices.shape[0]
    ntri= triangles.shape[0]
    N=int((intervalo[1]-intervalo[0])/dt)
    u=np.zeros((N+1,nvert))
    u[0,:]=np.vectorize(u0)(vertices[:, 0], vertices[:, 1], vertices[:, 2])

    M= mass_matrix(vertices, triangles) #matriz de masa  
    K= poisson_new.stiffness_matrix(vertices, triangles) #matriz de rigidez
    A= M + dt * K
    for m in range(0,N):
        t= intervalo[0]+(m+1)*dt
        right= right_side(dt, t, M, u[m,:], F_h, vertices, triangles) #lado derecho
        u[m+1, :]= np.linalg.solve(A,right)

    return u
