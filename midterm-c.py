"""
@author: Merve AKSU
"""

import os, time
import numpy as np
import matplotlib.pyplot as plt


def foil_coordinates(filename):

  with open(filename) as f:
    content = f.readlines()
    
  arr = []

  for i in content:

    column = i.strip().split()
    
    if len(column) == 2:
    
      try:    
        x,y = float(column[0]), float(column[1])
        arr.append([x,y])
      except:
        pass
   
  return np.array(arr)

for root, dir, files in os.walk("Normalized Airfoil Dataset/"):
  
  for i,j in enumerate(files):
    new_filename = 'Normalized Airfoil Dataset/' + j  
    arr = foil_coordinates(new_filename)
    x, y = arr[:,0], arr[:,1]
    
#PART C
    def define_panels(x, y, N=40):
        # PANELS
        N = 40  
        
        Radius = (x.max() - x.min()) / 2  # radius of the circle
        x_center = (x.max() + x.min()) / 2  # x-coord of the center
        circle = x_center + Radius * np.cos(np.linspace(0.0, 2 * np.pi, N + 1)) # define x-coord of the circle points
           
        x_ends = np.copy(circle)  # projection of the x-coord on the surface
        y_ends = np.empty_like(x_ends)  # initialization of the y-coord Numpy array
              
        # INTERPOLATION :
        # computes the y-coordinate of end-points
        P = 0
        for i in range(N):
                while P < len(x) - 1:
                    if (x[P] <= x_ends[i] <= x[P + 1]) or (x[P + 1] <= x_ends[i] <= x[P]):
                        break
                    else:
                        P =P + 1
                a = (y[P + 1] - y[P]) / (x[P + 1] - x[P])
                b = y[P + 1] - a * x[P + 1]
                y_ends[i] = a * x_ends[i] + b
                y_ends[N] = y_ends[0]
              
        a1=(y[int((len(y)-1)/2)+1] - y[int((len(y)-1)/2)]) / (x[int((len(y)-1)/2)+1] - x[int((len(y)-1)/2)])
        b1= 1*(y[int((len(y)-1)/2) + 1] - a1 * x[int((len(y)-1)/2) + 1])
        y_ends[int((N/2)+1)]= a1 * x_ends[int((N/2)+1)] + b1
        
        np.append(x_ends,0)
        np.append(y_ends,0)
        
        # NORMALS :
        
        theta = []
        length = []
        midx_ends,midy_ends = [], []
        # Midpoints and length of each panels:
        for z in range(N):
            length.append(np.sqrt((x_ends[z+1]-x_ends[z])**2+(y_ends[z+1]-y_ends[z])**2))   
            midx_ends.append((x_ends[z+1]+x_ends[z])/2)
            midy_ends.append((y_ends[z+1]+y_ends[z])/2)
            
        # Angles:
        for j in range (N):
                
            if x_ends[j+1]-x_ends[j] > 0:
                
                theta.append(np.pi+np.arccos(-(y_ends[j+1]-y_ends[j])/length[j]))
            else:         
                theta.append(np.arccos((y_ends[j+1]-y_ends[j])/length[j]))
         
        return x_ends,y_ends,midx_ends,midy_ends,theta
     
    def cusp_poınt(x_ends,y_ends,N=40):
            
            p1=(y_ends[2]-y_ends[1])/(x_ends[2]-x_ends[1])
            p2=(y_ends[N]-y_ends[N-1])/(x_ends[N]-x_ends[N-1])
            angle=abs((p1-p2)/(1+(p1*p2)))
            if angle<=np.deg2rad(10):
                trailing ='CUSP'
            else:
                trailing ='POINTED'
            return angle,trailing     
    
    # PLOTS :
    #    CALL FROM FUNCTIONS:
    x_ends,y_ends,midx_ends,midy_ends,theta = define_panels(x, y, N=40)
    angle,trailing = cusp_poınt(x_ends,y_ends,N=40)
    # Airfoil Plot:
    
    plt.figure()
    plt.title(files[i].replace('.dat',' '))
    plt.plot(x, y, color='k', linestyle='-', linewidth=2)
    plt.axes().set_aspect(1,'datalim')
    plt.grid(True)
    plt.xlabel('Xc', fontsize=10)
    plt.ylabel('Yc', fontsize=10)
    plt.text(0.3,-0.2,'Trailing Edge= %s'%trailing)
            
    # Panels
    plt.plot(x,y,'-')
    plt.plot(x_ends,y_ends,'o')
    #Normals:
    plt.quiver(midx_ends,midy_ends,np.cos(theta),np.sin(theta),scale = 20 )
    figure_folder = 'Figures-Part-C/' 
    plt.savefig(figure_folder+files[i].replace('.dat',' ') + '.jpg')
    plt.show()
    time.sleep(0.1)


      