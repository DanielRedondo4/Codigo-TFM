"""PLOT DE LA SOLUCIÓN NUMÉRICA"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib import animation
from matplotlib.cm import ScalarMappable
from matplotlib.colors import CenteredNorm
from IPython.display import Video

def sol(vertices, triangles, values, title, ax_limit=[-1,1], deg=(20,45)):
    # Calculamos el valor medio en la cara de cada triángulo
    face_values = np.mean(values[triangles], axis=1)
    
    u_min = np.min(values)
    u_max = np.max(values)

    #Normalizamos las medias
    normed_means= np.where(face_values<=0, face_values, face_values/np.abs(u_max) )
    if u_min<0:
        normed_means= np.where(normed_means>=0, normed_means, normed_means/np.abs(u_min))

    # Creamos la figura
    fig = plt.figure()

    # Creamos el plot 3D
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(title)

    # Creamos una Poly3DCollection 
    triangular_mesh = [vertices[triangle] for triangle in triangles]
    triangular_collection = Poly3DCollection(triangular_mesh)

    # Definimos el color map 
    cmap = plt.get_cmap('inferno')  
    norm = CenteredNorm(vcenter=0)

    # Creamos un ScalarMappable que mapea valores a colores
    sm = ScalarMappable(cmap=cmap, norm=norm)

    # Añadimos la barra de color al plot
    cbar = fig.colorbar(sm, ax=ax, pad=0.1) 

    # Establecemos los colores de cada cara basados en el valor medio de los valores
    # normalizdos de cada vértice
    triangular_collection.set_facecolor(cmap(norm(normed_means)))
    ax.add_collection(triangular_collection)

    # Nombramos los ejes
    ax.set_xlabel('X') 
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Límites de los ejes
    ax.set_xlim(ax_limit)
    ax.set_ylim(ax_limit)
    ax.set_zlim(ax_limit)
    
    # Rotamos el plot
    ax.view_init(elev=deg[0], azim=deg[1])

    return fig

def video_t_sol(vertices, triangles, u, title, intervalo, dt, ax_limit=[-1,1], interval=140):
    u_min = np.min(u)
    u_max = np.max(u)
    face_values= np.mean(u[0,triangles], axis=1)

    #Normalizamos las medias
    normed_means= np.where(face_values<=0, face_values, face_values/np.abs(u_max) )
    if u_min<0:
        normed_means= np.where(normed_means>=0, normed_means, normed_means/np.abs(u_min))
   
    # Creamos la figura para hacer un plot 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Iniciamos el cronómetro
    text = ax.text(-1, -0.75, 1.75, '', ha='center', va='center', fontsize=12)
    time = intervalo[0]  # Replace with your time variable
    text.set_text(f't = {time:.2f}')


    # Creamos una Poly3DCollection 
    triangular_mesh = [vertices[triangle] for triangle in triangles]
    triangular_collection = Poly3DCollection(triangular_mesh)

    # Definimos el color map 
    cmap = plt.get_cmap('inferno')  
    norm = CenteredNorm(vcenter=0)

    # Creamos un ScalarMappable que mapea valores a colores
    sm = ScalarMappable(cmap=cmap, norm=norm)

    # Añadimos la barra de color al plot
    cbar = fig.colorbar(sm, ax=ax, pad=0.1)  

    # Establecemos los colores de cada cara basados en el valor medio de los valores
    # normalizdos de cada vértice
    triangular_collection.set_facecolor(cmap(norm(normed_means)))
    ax.add_collection(triangular_collection)

    # Nombre de los ejes y título
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Límites de los ejes
    ax.set_xlim(ax_limit)
    ax.set_ylim(ax_limit)
    ax.set_zlim(ax_limit)

    def update_colors(frame, triangular_collection, u):
        face_values= np.mean(u[frame,triangles], axis=1)
        #Normalizamos las medias
        normed_means= np.where(face_values<=0, face_values, face_values/np.abs(u_max) )
        if u_min<0:
            normed_means= np.where(normed_means>=0, normed_means, normed_means/np.abs(u_min))

        triangular_collection.set_facecolor(cmap(norm(normed_means)))
        ax.add_collection(triangular_collection)
        time = intervalo[0]+ frame * dt  
        text.set_text(f't = {time:.2f}')
    
    #Creamos la animación
    M= u.shape[0]
    anim = animation.FuncAnimation(fig=fig, func=update_colors, frames=M, 
                                   fargs=(triangular_collection, u), interval= interval)
    
    anim.save('animation.mp4', writer='ffmpeg')
    video_path = 'animation.mp4'  # Replace with the path to your saved video file
    video = Video(video_path, embed=True)
    return video



def u_tvalues(vertices, triangles, t_values, u, intervalo
              , ax_limit=[-1,1], deg=(20,45)):
    M= u.shape[0]
    t_total=np.linspace(intervalo[0], intervalo[1], M)
    t_values= np.sort(t_values)
    u_min = np.min(u)
    u_max = np.max(u)
    pos=0
    
    for t in t_values:
        while t_total[pos]< t:
            pos=pos+1
    
        face_values= np.mean(u[pos,triangles], axis=1)

        #Normalizamos las medias
        normed_means= np.where(face_values<=0, face_values, face_values/np.abs(u_max) )
        if u_min<0:
            normed_means= np.where(normed_means>=0, normed_means, normed_means/np.abs(u_min))
    
        # Creamos la figura para hacer un plot 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Creamos una Poly3DCollection 
        triangular_mesh = [vertices[triangle] for triangle in triangles]
        triangular_collection = Poly3DCollection(triangular_mesh)

        # Definimos el color map 
        cmap = plt.get_cmap('inferno')  
        norm = CenteredNorm(vcenter=0)

        # Creamos un ScalarMappable que mapea valores a colores
        sm = ScalarMappable(cmap=cmap, norm=norm)

        # Añadimos la barra de color al plot
        cbar = fig.colorbar(sm, ax=ax, pad=0.1)  

        # Establecemos los colores de cada cara basados en el valor medio de los valores
        # normalizdos de cada vértice
        triangular_collection.set_facecolor(cmap(norm(normed_means)))
        ax.add_collection(triangular_collection)

        # Nombre de los ejes y título
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
  
        # Límites de los ejes
        ax.set_xlim(ax_limit)
        ax.set_ylim(ax_limit)
        ax.set_zlim(ax_limit)
        ax.set_title(f't = {t:.2f}')

        # Rotamos el plot
        ax.view_init(elev=deg[0], azim=deg[1])

        

            
