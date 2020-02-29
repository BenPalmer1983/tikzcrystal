######################################################
#  Ben Palmer University of Birmingham 2020
#  Free to use
######################################################

import numpy
from pwscf_output import pwscf_output
from file_type import file_type

class grid:


  @staticmethod
  def make(g_list):
    cmd_lines = []
    for g in g_list:
      grid.make_inner(g, cmd_lines)
    return cmd_lines
  
  @staticmethod
  def make_inner(g, cmd_lines):
  
    cx = g['cx']
    cy = g['cy']
    cz = g['cz']
    
    a = g['a']
    b = g['b']
    c = g['c']
    alpha = g['alpha']
    beta = g['beta']
    gamma = g['gamma']
        
    print(g['lines'])    
    if(g['lines']['on'] == False): 
      return cmd_lines
      
    colour = g['lines']['colour']
    weight = g['lines']['weight']
    type = g['lines']['type']
    
    
    for i in range(cx+1):
      for j in range(cy+1):
        x = i * (1.0 / cx)
        y = j * (1.0 / cy)
        za = 0.0
        zb = 1.0  
        if(g['gridtype'] == 'all' or (g['gridtype'] == 'inner' and not(x == 0.0 or x == 1.0 or y == 0.0 or y == 1.0)) or (g['gridtype'] == 'outer' and (x == 0.0 or x == 1.0 or y == 0.0 or y == 1.0))):      
          x, y, za = grid.ctransform(x,y,za, a,b,c, alpha, beta, gamma)
          x, y, zb = grid.ctransform(x,y,zb, a,b,c, alpha, beta, gamma)        
          join_line = 'line xa=' + str(x) + ' xb=' + str(x) + ' ya=' + str(y) + ' yb=' + str(y) + ' za=' + str(za) + ' zb=' + str(zb) + ' colour='+colour+' type=' + type + ' line_weight="' + weight + '"'
          cmd_lines.append(join_line)  
    for i in range(cx+1):
      for j in range(cz+1):
        x = i * (1.0 / cx)
        z = j * (1.0 / cz)
        ya = 0.0
        yb = 1.0    
        if(g['gridtype'] == 'all' or (g['gridtype'] == 'inner' and not(x == 0.0 or x == 1.0 or z == 0.0 or z == 1.0)) or (g['gridtype'] == 'outer' and (x == 0.0 or x == 1.0 or z == 0.0 or z == 1.0))):      
          x, ya, za = grid.ctransform(x,ya,z, a,b,c, alpha, beta, gamma)
          x, yb, zb = grid.ctransform(x,yb,z, a,b,c, alpha, beta, gamma)        
          join_line = 'line xa=' + str(x) + ' xb=' + str(x) + ' ya=' + str(ya) + ' yb=' + str(yb) + ' za=' + str(z) + ' zb=' + str(z) + ' colour='+colour+' type=' + type + ' line_weight="' + weight + '"'
          cmd_lines.append(join_line)  
    for i in range(cy+1):
      for j in range(cz+1):
        y = i * (1.0 / cy)
        z = j * (1.0 / cz)
        xa = 0.0
        xb = 1.0      
        if(g['gridtype'] == 'all' or (g['gridtype'] == 'inner' and not(y == 0.0 or y == 1.0 or z == 0.0 or z == 1.0)) or (g['gridtype'] == 'outer' and (y == 0.0 or y == 1.0 or z == 0.0 or z == 1.0))):      
          xa, y, z = grid.ctransform(xa,y,z, a,b,c, alpha, beta, gamma)
          xb, y, z = grid.ctransform(xb,y,z, a,b,c, alpha, beta, gamma)        
          join_line = 'line xa=' + str(xa) + ' xb=' + str(xb) + ' ya=' + str(y) + ' yb=' + str(y) + ' za=' + str(z) + ' zb=' + str(z) + ' colour='+colour+' type=' + type + ' line_weight="' + weight + '"'
          cmd_lines.append(join_line)         
    
    return cmd_lines


  @staticmethod
  def ctransform(x,y,z, a,b,c, alpha, beta, gamma):
    M = numpy.zeros((3,3,),)

    M[0,0] = a * numpy.sin(beta)
    M[0,1] = b * numpy.sin(alpha) * numpy.cos(gamma)
    M[0,2] = 0
    M[1,0] = 0
    M[1,1] = b * numpy.sin(alpha) * numpy.sin(gamma)
    M[1,2] = 0
    M[2,0] = a * numpy.cos(beta)
    M[2,1] = b * numpy.cos(alpha)
    M[2,2] = c

    xvec = numpy.zeros((3,),)
    xvec[0] = x
    xvec[1] = y
    xvec[2] = z

    yvec = numpy.matmul(M, xvec)

    return round(yvec[0],7), round(yvec[1],7), round(yvec[2],7)
    
    
    
  def default():
    return {
            'make': False, 
            'a': 1, 'b': 1, 'c': 1, 
            'alpha': 1.570796327, 'beta': 1.570796327, 'gamma': 1.570796327, 
            'cx': 1, 'cy': 1, 'cz': 1, 
            'colour': '#000000', 'type': 'solid', 'weight': 'thin', 
            'gridtype': 'all',
            }