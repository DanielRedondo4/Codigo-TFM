"""
Triangulación para superficies de revolución homeomorfas a una esfera o un toro
"""
import numpy as np
from scipy.spatial import Delaunay

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def surface_of_revolution(theta, phi, curve):
    x = curve(theta)[0] * np.cos(phi)
    y = curve(theta)[0] * np.sin(phi)
    z = curve(theta)[1]
    return x, y, z

#Función que recibe el índice de un punto, una lista de índices y nos crea una
#triangulación
def pegado1(ind_polo, indices):
  tr=np.zeros((indices.shape[0], 3))
  pos=0
  for i in range(0, indices.shape[0]-1):
    tr[pos,:]=np.array([indices[i], indices[i+1], ind_polo])
    pos=pos+1
  tr[indices.shape[0]-1,:]=np.array([indices[0], indices[indices.shape[0]-1], ind_polo])
  return tr

#Función que recibe dos listas de índices de igual tamaño
#y nos crea una triangulación entre estos
def pegado2(ind1, ind2):
  tr=np.zeros((2*(ind1.shape[0]-1),3))
  for i in range(0, ind1.shape[0]-1):
    tr[2*i,:]= np.array([ind2[i], ind2[i+1], ind1[i]])
    tr[2*i+1,:]= np.array([ind1[i], ind2[i+1], ind1[i+1]])
  return tr

#Función que nos crea una triangulación para la superficie de revolución cuyo dominio
#es de la forma [0,b]x[0,2*pi]. Los parámetros de entrada son:
#b: extremo derecho del intervalo donde se mueve el parámetro theta
#g: el género de la superficie
#ntheta: número de valores entre 0 y b (incluidos) que toma theta
#nphi: número de valores entre 0 y 2*pi (incluidos) que toma phi
#curve: parametrización de la curva generatriz
def tr_revolsrf(b, g, ntheta, nphi, curve):
  Rec= np.array([[0, b],[0, 2*np.pi]]) #Rectángulo [0,b]x[0,2*pi] (Dominio de la paremetrización)
  theta= np.linspace(Rec[0,0], Rec[0,1], ntheta)
  phi= np.linspace(Rec[1,0], Rec[1,1], nphi)
  if g==0:
    #Malla de puntos donde la parametrización es biyectiva (0,b)x[0,2pi)
    theta_int= theta[1:ntheta-1]
    phi_int= phi[0:nphi-1]
    THETA_INT, PHI_INT=np.meshgrid(theta_int,phi_int)
  else:
    #Malla de puntos donde la parametrización es biyectiva [0,b)x[0,2pi)
    theta_int= theta[0:ntheta-1]
    phi_int= phi[0:nphi-1]
    THETA_INT, PHI_INT=np.meshgrid(theta_int,phi_int)


  #Malla triangular para los puntos anteriores
  points2D=np.vstack([THETA_INT.flatten(), PHI_INT.flatten()]).T
  tri = Delaunay(points2D)
  triangles=tri.simplices

  #Calculamos los correspondientes puntos en la superficie
  x_int, y_int, z_int = surface_of_revolution(THETA_INT, PHI_INT, curve)
  vertices=np.vstack((x_int.flatten(),y_int.flatten(),z_int.flatten())).T


  if g==0:
    #Incluimos los vértices correspondientes a los valores theta=0,pi (polos)
    x_1, y_1, z_1 = surface_of_revolution(0, 0, curve)
    x_2, y_2, z_2 = surface_of_revolution(b, 0, curve)
    polo1= np.array([x_1, y_1, z_1])
    polo2= np.array([x_2, y_2, z_2])
    polo1_ind= int(vertices.shape[0])
    polo2_ind= int(polo1_ind+1)
    b_points= np.array([polo1, polo2])
    vertices=np.append(vertices, b_points, axis=0)

    #Incluimos los triángulos correspondientes a los polos
    indices1= (ntheta-2)*np.arange(0, nphi-1)
    indices2= np.arange(ntheta-3, (ntheta-2)*(ntheta-1), ntheta-2)
    tri1= pegado1(polo1_ind, indices1)
    triangles= np.append(triangles, tri1, axis=0)
    tri2= pegado1(polo2_ind, indices2)
    triangles= np.append(triangles, tri2, axis=0)

    #Incluimos los triángulos formados por los puntos del último meridiano y del
    #meridiano inicial
    ind1= np.arange(0, ntheta-2)
    ind2= np.arange((ntheta-2)*(nphi-2), (ntheta-2)*(nphi-1))
    tri3=pegado2(ind1, ind2)
    triangles= np.append(triangles, tri3, axis=0)

  else:
    #Incluimos los triángulos formados por los puntos theta=0, 3pi/2, 0<=phi<2pi
    ind1= np.arange(ntheta-2, (ntheta-1)*(ntheta-1), ntheta-1 )
    ind2= (ntheta-1)*np.arange(0, nphi-1)
    tri=pegado2(ind1, ind2)
    triangles= np.append(triangles, tri, axis=0)

    #Incluimos
    ind1= np.arange((nphi-2)*(ntheta-1), (ntheta-1)*(ntheta-1))
    ind2= np.arange(0, ntheta-1)
    tri=pegado2(ind1, ind2)
    triangles= np.append(triangles, tri, axis=0)

    #Incluimos
    ind1= np.array([(nphi-2)*(ntheta-1), (ntheta-1)*(ntheta-1)-1])
    ind2= np.array([0, ntheta-2])
    tri=pegado2(ind1, ind2)
    triangles= np.append(triangles, tri, axis=0)

  triangles=triangles.astype('int32')
  return vertices, triangles

'''
#Para testear el código de la triangulación de superficies de revolución:

def dumbbell_surface(theta, r=1/2):
    return np.sqrt(1/4+3/4*(theta-1)**2- (theta-1)**4), theta-1 

def esfera(theta):
  return np.sin(theta), np.cos(theta)

def toro(theta):
  return 1/2+1/4*np.cos(theta), 1/4*np.sin(theta)

vertices, triangles = tr_revolsrf(np.pi, 0, 4, 4, esfera)

# Creamos el plot 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Creamos una Poly3DCollection para las caras triangulares
facecolors='blue'
triangular_mesh = [vertices[triangle] for triangle in triangles]
ax.add_collection3d(Poly3DCollection(triangular_mesh, facecolors=facecolors, linewidths=0.25, edgecolors='black', alpha=1))

# Nombramos los ejes
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Límites de los ejes
ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

# Desactivar la enumeración de los ejes x, y, z
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Rota el plot
ax.view_init(elev=30, azim=0)  

# Mostramos el plot
plt.show()

'''