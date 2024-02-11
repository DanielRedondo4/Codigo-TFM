from cmath import exp
import numpy as np
import matplotlib.pyplot as plt

import trmesh
import poisson
import poisson_new
import heat
import heat_new
import plot


#Función del problema de Poisson discretizado
def F_h(a):
  norm = a[0]**2 + a[1]**2 + a[2]**2
  return (6/norm)*a[0]*a[1]

#Solución exacta de poisson con f
def u_ex(a):
    return a[0]*a[1]

def f_h(t,a):
    return 0

def u0(x , y, z):
   return x*y

#Dato inicial calor homogéneo mancuerna

def u0_mancuerna1(x,y,z):
   return np.sin(3*np.pi*z)

def u0_mancuerna(x,y,z):
   return int(not((-1/3<=z<=1/3) or (2/3<= z) or (z<=-2/3)))

#Calor no homogéneo
def fh_fuente_calor(t,a):
    return int(a[2]>=3/4)
  
   
def calor_inicial(x,y,z):
   return 0

def fuente_calor_toro(t,a):
   x_min = 1/4*np.cos(np.pi/3)
   x_max = 3/4*np.cos(np.pi/6)
   y_min = 1/4*np.sin(np.pi/6)
   y_max = 3/4*np.sin(np.pi/3)
   return int((x_min<=a[0]<=x_max) and (y_min<=a[1]<=y_max) and (-1/4<=a[2]<=1/4))

def fuente_calor_mancuerna(t,a):
   return int(-1/5<=a[2]<=1/5)

#Curvas generatrices de superficies de revolución
   
def esfera(theta):
  return np.sin(theta), np.cos(theta)

def toro(theta):
  return 1/2+1/4*np.cos(theta), 1/4*np.sin(theta)

def dumbbell_surface(theta, r=1/2):
    return np.sqrt(1/4+3/4*(theta-1)**2- (theta-1)**4), theta-1

vertices, triangles= trmesh.tr_revolsrf(b= 2, g=0, ntheta=50, nphi=50, curve=dumbbell_surface)

'''
#TEST POISSON

values = poisson.poisson_SFEM(F_h=F_h, vertices= vertices, triangles= triangles)
plot.sol(vertices= vertices, triangles= triangles, values= values, title= 'solución aproximada normalizada')

#Calculamos los valores de la solución exacta
values_exact=np.zeros(vertices.shape[0])
pos=0
for vertice in vertices:
  values_exact[pos]=u_ex(vertice)
  pos=pos+1
plot.sol(vertices= vertices, triangles= triangles, values= values_exact, title= 'solución exacta normalizada')
plt.show()
'''
'''
#TEST POISSON NEW

values = poisson_new.poisson_SFEM(F_h=F_h, vertices= vertices, triangles= triangles)
plot.sol(vertices= vertices, triangles= triangles, values= values, title= 'u_h_mean_new')

#Calculamos los valores de la solución exacta
values_exact=np.zeros(vertices.shape[0])
pos=0
for vertice in vertices:
  values_exact[pos]=u_ex(vertice)
  pos=pos+1
plot.sol(vertices= vertices, triangles= triangles, values= values_exact, title= 'u_mean')
plt.show()
'''

'''
#TEST CALOR

u= heat.heat_SFEM(intervalo=(0,1), dt=0.01, F_h= f_h, u0= u0,
                   vertices= vertices, triangles= triangles )
#print('sol:',u)
#print('shape:', u.shape)
#print('valor máximo', np.amax(u))
#print('valor mínimo', np.amin(u))

#Saca una figura por cada valor de t que le des
t_values= np.array([0, 0.2, 0.4])
plot.u_tvalues(vertices= vertices, triangles= triangles, 
               t_values= t_values, u=u, intervalo=(0,1))

#Saca video (se crea una vez cierres las figuras anteriores)
#plot.video_t_sol(vertices= vertices, triangles= triangles, 
                 #u= u, intervalo=(0,1), dt= 0.01, title= 'u_h(t)' )

'''

#TEST CALOR NEW

u_new= heat_new.heat_SFEM(intervalo=(0,1), dt=0.01, F_h= f_h, u0= u0_mancuerna1,
                   vertices= vertices, triangles= triangles)

#Saca una figura por cada valor de t que le des
t_values= np.array([0,0.02,0.1])
plot.u_tvalues(vertices= vertices, triangles= triangles, 
               t_values= t_values, u=u_new, intervalo=(0,1))
plt.show()

'''
#Saca video (se crea una vez cierres las figuras anteriores)
plot.video_t_sol(vertices= vertices, triangles= triangles, 
                 u= u_new, intervalo=(0,1), dt= 0.01, title= 'u_h_new(t)' )
'''