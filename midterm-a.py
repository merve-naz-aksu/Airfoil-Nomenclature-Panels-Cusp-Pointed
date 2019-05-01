
"""
@author: Merve AKSU
"""
import os
import numpy as np

def foil_coordinates(filename):

  with open(filename) as f:
    content = f.readlines()
#   readlines is reading the contents of the file line-by-line.
    
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

# os.walk : It allows you to walk down a directory tree structure.
for root, dir, files in os.walk("Airfoils/"):
  
  for i,j in enumerate(files):
#Enumerate() method adds a counter to an iterable and returns it in a form of enumerate object. 
#This enumerate object can then be used directly in for loops or be converted into a list of tuples using list() method.    
    filename = 'Airfoils/' + j
    
    new_filename = 'Normalized Airfoil Dataset/' + j
    arr = foil_coordinates(filename)
    
    x, y = arr[:,0], arr[:,1]
               
#PART A :

    x[0] = 1.0
    y[0] = 0.0
    x[-1] = 1.0
    y[-1]=0.0
    np.savetxt(new_filename,arr)
    
