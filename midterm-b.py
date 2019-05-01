
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
               
    def airfoil_nomenclature(x,y):                             
    # CHORD :
       ay = abs(y)
       x_point =  [x.max(),x.min()]
       y_point =  [y[0],ay.min()]      
    # MEAN CAMBER LINE:       
       mx,my=[],[]
       mcx,mcy=[],[]
    # Midpoints
       for j in range (len(x)-1):  
        
           mx.append((x[j]+x[j-1])/2)
           my.append((y[j]+y[j-1])/2)
           
       for j in range (len(x)-1):
         
            mcx.append((mx[j]+mx[1-j])/2)
            mcy.append((my[j]+my[1-j])/2)
           
       thickness = []           
    # MAX THICNESS :
            
       for t in range (len(x)-1):
            
            thickness.append(my[1-t]-my[t])
            max_thickness=max(thickness)            # Maximum thickness value
            mt_point=thickness.index(max_thickness) # Maximum thickness point
            
       max_thickx=[mx[mt_point],mx[1-mt_point]]
       max_thicky=[my[mt_point],my[1-mt_point]]
                
#       print ('Maximum Thickness:',max_thickness,'%')
       return x_point,y_point,mcx,mcy,max_thickx, max_thicky,max_thickness
          
    # CALL FROM FUNCTIONS:
    x_point,y_point,mcx,mcy, max_thickx, max_thicky,max_thickness = airfoil_nomenclature(x,y)
    # PLOTS :
    # Airfoil Plot:
    
    plt.figure()
    plt.title(files[i].replace('.dat',' '))
    plt.text(0.2,0.3,'Maximum Thickness = %f'%(max_thickness*100))
    plt.plot(x, y, color='k', linestyle='-', linewidth=2)
    plt.axes().set_aspect(1,'datalim')
    plt.grid(True)
    plt.xlabel('Xc', fontsize=10)
    plt.ylabel('Yc', fontsize=10)
    
            
    #Mean camber line, chord, thickness
    plt.plot(x_point,y_point,'y-')
    plt.plot(mcx,mcy,'r')
    plt.plot(max_thickx,max_thicky,'m') 
    figure_folder = 'Figures-Part-B/' 
    plt.savefig(figure_folder+files[i].replace('.dat',' ') + '.jpg')
    plt.show()
    time.sleep(0.1)

    