
import numpy

class crystal:

  @staticmethod
  def make(crys_in):
    
    # defaults
    crys = { 
            'type': ['bcc'],
            'x': [0.0],
            'y': [0.0],
            'z': [0.0],
            'cx': [1],
            'cy': [1],
            'cz': [1],
            'a': [1.0],
            'b': [1.0],
            'c': [1.0],
            'alpha': [90.0],
            'beta': [90.0],
            'gamma': [90.0],
            'colour': ['#000000'],
            'r': 1,
            'lines_vertex': ['none','solid'],
            'lines_subcells': ['none','solid'],
            'lines_diag': ['none','solid'],
           } 
    
    for k in crys.keys(): 
      if(k in crys_in.keys()):
        crys[k] = crys_in[k]
    
    # Type
    ctype = crys['type'][0]
    
    # Corner
    x = float(crys['x'][0])
    y = float(crys['y'][0])
    z = float(crys['z'][0])
    
    # Side lengths
    a = float(crys['a'][0])
    b = float(crys['b'][0])
    c = float(crys['c'][0])
    
    # Side angles
    alpha = numpy.deg2rad(float(crys['alpha'][0]))
    beta = numpy.deg2rad(float(crys['beta'][0]))
    gamma = numpy.deg2rad(float(crys['gamma'][0]))
    
    # Crystal copies
    cx = int(crys['cx'][0])
    cy = int(crys['cy'][0])
    cz = int(crys['cz'][0])
    
    # Radius
    r = crys['r'][0]
    
    
    # Colour
    colour = crys['colour']    
    
    
    if(ctype == "sc"):
      atoms = crystal.make_sc(cx, cy, cz)
    elif(ctype == "bcc"):
      atoms = crystal.make_bcc(cx, cy, cz)
    elif(ctype == "fcc"):
      atoms = crystal.make_fcc(cx, cy, cz)
    elif(ctype == "ec"):
      atoms = crystal.make_ec(cx, cy, cz)
    elif(ctype == "zb"):
      atoms = crystal.make_zb(cx, cy, cz)
      
    atoms_xyz = []  
    for i in range(len(atoms)):
      x, y, z = crystal.ctransform(atoms[i][0], atoms[i][1], atoms[i][2], a, b, c, alpha, beta, gamma)
      atoms_xyz.append([x,y,z])
      
    min_r, max_r = crystal.neighbour_list(atoms_xyz) 
    if(r == 'auto'):
      r = 0.45 * min_r
    print(min_r, max_r, r)
      
    # Spheres
    cmd_lines = []
    for i in range(len(atoms)):
      #x, y, z = crystal.ctransform(atoms[i][0], atoms[i][1], atoms[i][2], a, b, c, alpha, beta, gamma)
      x, y, z = atoms_xyz[i][0], atoms_xyz[i][1], atoms_xyz[i][2]
      sphere_line = 'ball x=' + str(x) + ' y=' + str(y) + ' z=' + str(z) + ' r=' + str(r) + ' colour=' + colour[i % len(colour)]
      cmd_lines.append(sphere_line)  
      
    # Lines
    join_lines = crystal.make_lines(crys, atoms, atoms_xyz, cx, cy, cz, a, b, c)
    cmd_lines = cmd_lines + join_lines
      
    return cmd_lines

  def make_sc(cx, cy, cz):
    unit = [[0,0,0]]
    return crystal.expand(unit, cx, cy, cz)

  def make_bcc(cx, cy, cz):
    unit = [[0,0,0],[0.5,0.5,0.5]]
    return crystal.expand(unit, cx, cy, cz)
    
  def make_fcc(cx, cy, cz):
    unit = [[0,0,0],[0.5,0.5,0.0],[0.5,0.0,0.5],[0.0,0.5,0.5]]
    return crystal.expand(unit, cx, cy, cz)
    
  def make_ec(cx, cy, cz):
    unit = [[0,0,0],[0.5,0.5,0]]
    return crystal.expand(unit, cx, cy, cz)
    
  def make_zb(cx, cy, cz):
    unit = [[0,0,0],[0.5,0.5,0.0],[0.5,0.0,0.5],[0.0,0.5,0.5],[0.25,0.25,0.25],[0.75,0.75,0.25],[0.25,0.75,0.75],[0.75,0.25,0.75]]
    return crystal.expand(unit, cx, cy, cz)
    
  def expand(unit, cx, cy, cz):
    cx_loops = cx
    cy_loops = cy
    cz_loops = cz
    surround = True
    if(surround):
      cx_loops = cx + 1
      cy_loops = cy + 1
      cz_loops = cz + 1
    atoms = []    
    for i in range(cx_loops):
      for j in range(cy_loops):
        for k in range(cz_loops):
          for atom in unit:
            x = round((i + atom[0]) * (1 / cx), 8)
            y = round((j + atom[1]) * (1 / cy), 8)
            z = round(1.0 - (k + atom[2]) * (1 / cz), 8)
            
            if(x <= 1.0 and y <= 1.0 and z <= 1.0 and x >= 0.0 and y >= 0.0 and z >= 0.0):
              atoms.append([x, y, z])
    for i in range(len(atoms)):
      for j in range(3):
        atoms[i][j] = atoms[i][j]
    return atoms

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

  def neighbour_list(atoms):
    min_r = None
    max_r = None
    for i in range(len(atoms)):
      for j in range(i+1, len(atoms)):
        r = numpy.sqrt((atoms[i][0] - atoms[j][0])**2 + (atoms[i][1] - atoms[j][1])**2 + (atoms[i][2] - atoms[j][2])**2)
        if(min_r == None or min_r > r):
          min_r = r
        if(max_r == None or max_r < r):
          max_r = r
    return min_r, max_r

  def make_lines(crys, atoms, atoms_xyz, cx, cy, cz, a, b, c):
   
    vertex_large_on, vertex_large_weight, vertex_large_type, vertex_large_f = crystal.line_details(crys['lines_vertex'])
    vertex_small_on, vertex_small_weight, vertex_small_type, vertex_small_f = crystal.line_details(crys['lines_subcells'])
    diag_on, diag_weight, diag_type, diag_f = crystal.line_details(crys['lines_diag'])
  
    cmd_lines = []
  
    cell_diag = numpy.sqrt((a/cx)**2 + (b/cy)**2 + (c/cz)**2)
  
    nl = []
    nl_close = []
    nl_ortho = []
    nl_vertex_small = []
    nl_vertex_small_inner = []
    nl_vertex_large = []
    nl_diagonal = []
    nl_diagonal_short = []
    
    # Build neighbour list
    rcut_sq = (a/cx)**2 + (b/cy)**2 + (c/cz)**2
    for i in range(len(atoms)-1):
      for j in range(i+1, len(atoms)):
        rsq = (atoms[i][0] - atoms[j][0])**2 + (atoms[i][1] - atoms[j][1])**2 + (atoms[i][2] - atoms[j][2])**2
        if(rsq > 0.0 and rsq <= rcut_sq):
          r = numpy.sqrt(rsq)      
          nl.append([r, atoms[i], atoms[j], atoms_xyz[i], atoms_xyz[j]])
          
    # Nearby Neighbours
    for i in range(len(nl)):
      if(nl[i][0] <= 1.05 * cell_diag):
        nl_close.append(nl[i])          
    
    # Orthogonal
    for i in range(len(nl_close)):
      if(crystal.ortho(nl_close[i][3], nl_close[i][4])):
        nl_ortho.append(nl_close[i])
    
    # vertex (smaller sub cells)
    for i in range(len(nl_ortho)):
      nx = a * (min(numpy.floor(0.5 * cx * (nl_ortho[i][3][0] + nl_ortho[i][4][0])), cx-1) / cx)
      ny = b * (min(numpy.floor(0.5 * cy * (nl_ortho[i][3][1] + nl_ortho[i][4][1])), cy-1) / cy)
      nz = c * (min(numpy.floor(0.5 * cz * (nl_ortho[i][3][2] + nl_ortho[i][4][2])), cz-1) / cz)
      if(crystal.vertex(nl_ortho[i][3], nl_ortho[i][4],nx,ny,nz,a/cx,b/cy,c/cz)):
        nl_vertex_small.append(nl_ortho[i])
    
    # vertex (smaller sub cells inner)
    for i in range(len(nl_ortho)):
      nx = a * (min(numpy.floor(0.5 * cx * (nl_ortho[i][3][0] + nl_ortho[i][4][0])), cx-1) / cx)
      ny = b * (min(numpy.floor(0.5 * cy * (nl_ortho[i][3][1] + nl_ortho[i][4][1])), cy-1) / cy)
      nz = c * (min(numpy.floor(0.5 * cz * (nl_ortho[i][3][2] + nl_ortho[i][4][2])), cz-1) / cz)
      if(crystal.vertex(nl_ortho[i][3], nl_ortho[i][4],nx,ny,nz,a/cx,b/cy,c/cz)):
        if(not crystal.vertex(nl_ortho[i][3], nl_ortho[i][4],0,0,0,1,1,1)):
          nl_vertex_small_inner.append(nl_ortho[i])
    
    # vertex (large cell)
    for i in range(len(nl_ortho)):
      if(crystal.vertex(nl_ortho[i][3], nl_ortho[i][4],0,0,0,1,1,1)):
        nl_vertex_large.append(nl_ortho[i])       
    
    # diag
    for i in range(len(nl_close)):
      if(not crystal.ortho(nl_close[i][3], nl_close[i][4])):
        nl_diagonal.append(nl_close[i])
    
    # diag
    for i in range(len(nl_close)):
      if(not crystal.ortho(nl_close[i][3], nl_close[i][4]) and nl_close[i][0] <= diag_f * cell_diag):
        nl_diagonal_short.append(nl_close[i])
    
    if(vertex_large_on):
      cmd_lines = crystal.add_lines(cmd_lines, nl_vertex_large, vertex_large_type, vertex_large_weight)
    if(vertex_small_on):
      cmd_lines = crystal.add_lines(cmd_lines, nl_vertex_small_inner, vertex_small_type, vertex_small_weight)
    if(diag_on):
      cmd_lines = crystal.add_lines(cmd_lines, nl_diagonal_short, diag_type, diag_weight)

    
    
    
    return cmd_lines
    
    
    
    
    
  def ortho(xyz_a, xyz_b):
    is_ortho = False
    if(abs(xyz_a[0] - xyz_b[0]) <= 1.0e-5 and abs(xyz_a[1] - xyz_b[1]) <= 1.0e-5):
      is_ortho = True
    elif(abs(xyz_a[0] - xyz_b[0]) <= 1.0e-5 and abs(xyz_a[2] - xyz_b[2]) <= 1.0e-5):
      is_ortho = True
    elif(abs(xyz_a[1] - xyz_b[1]) <= 1.0e-5 and abs(xyz_a[2] - xyz_b[2]) <= 1.0e-5):
      is_ortho = True    
    return is_ortho
    
    
  def vertex(xyz_a, xyz_b, ox, oy, oz, a, b, c):
    corners = [
      [ox, oy, oz],
      [ox + a, oy, oz],
      [ox, oy + b, oz],
      [ox, oy, oz + c],
      [ox + a, oy + b, oz],
      [ox + a, oy, oz + c],
      [ox, oy + b, oz + c],
      [ox + a, oy + b, oz + c]]   
       
    is_vertex = False      
    if(abs(xyz_a[0] - xyz_b[0]) <= 1.0e-5 and abs(xyz_a[1] - xyz_b[1]) <= 1.0e-5):
      is_vertex = True
      if(not(abs(xyz_a[0] - ox) <= 1.0e-5 or abs(xyz_a[0] - (ox + a)) <= 1.0e-5)):
        is_vertex = False
      if(not(abs(xyz_a[1] - oy) <= 1.0e-5 or abs(xyz_a[1] - (oy + b)) <= 1.0e-5)):
        is_vertex = False
    if(abs(xyz_a[0] - xyz_b[0]) <= 1.0e-5 and abs(xyz_a[2] - xyz_b[2]) <= 1.0e-5):
      is_vertex = True
      if(not(abs(xyz_a[0] - ox) <= 1.0e-5 or abs(xyz_a[0] - (ox + a)) <= 1.0e-5)):
        is_vertex = False
      if(not(abs(xyz_a[2] - oz) <= 1.0e-5 or abs(xyz_a[2] - (oz + c)) <= 1.0e-5)):
        is_vertex = False 
    if(abs(xyz_a[1] - xyz_b[1]) <= 1.0e-5 and abs(xyz_a[2] - xyz_b[2]) <= 1.0e-5):
      is_vertex = True
      if(not(abs(xyz_a[1] - oy) <= 1.0e-5 or abs(xyz_a[1] - (oy + b)) <= 1.0e-5)):
        is_vertex = False
      if(not(abs(xyz_a[2] - oz) <= 1.0e-5 or abs(xyz_a[2] - (oz + c)) <= 1.0e-5)):
        is_vertex = False 
      
    #print(corners)
      
    return is_vertex    
        
    
  def add_lines(cmd_lines, pairs, type, weight):
    for pair in pairs:
      xa = str(pair[3][0])
      ya = str(pair[3][1])
      za = str(pair[3][2])
      xb = str(pair[4][0])
      yb = str(pair[4][1])
      zb = str(pair[4][2])
      join_line = 'line xa=' + str(xa) + ' xb=' + str(xb) + ' ya=' + str(ya) + ' yb=' + str(yb) + ' za=' + str(za) + ' zb=' + str(zb) + ' colour=#000022 type=' + type + ' line_weight="' + weight + '"'
      cmd_lines.append(join_line) 
   
    return cmd_lines
    
    
    
  def line_details(details):
    ds = []
    for d in details:
      ds.append(d.strip().lower())
      
    if('none' in ds):
      on = False
      weight = ''
      type = ''
      f = 0.5
    else:
      on = True
      weight = 'thin'
      type = 'solid'
      f = 0.5
      if('thin' in ds):
        weight = 'thin'
      elif('very thin' in ds):
        weight = 'very thin'
      elif('thick' in ds):
        weight = 'thick'
      elif('very thick' in ds):
        weight = 'very thick'
      elif('ultra thick' in ds):
        weight = 'ultra thick'
      if('solid' in ds):
        type = 'solid'
      elif('dashed' in ds):
        type = 'dashed'
      elif('dotted' in ds):
        type = 'dotted' 
      for d in ds:
        try:
          f = float(d)
          break
        except:
          pass
        
    return on, weight, type, f
        
    
    
    
    """
    
    # Draw Outer 
    draw_outer = True
    if(draw_outer):
      for pair in shell_lines:
      
        xa = str(pair[3][0])
        ya = str(pair[3][1])
        za = str(pair[3][2])
        xb = str(pair[4][0])
        yb = str(pair[4][1])
        zb = str(pair[4][2])
        
        join_line = 'line xa=' + str(xa) + ' xb=' + str(xb) + ' ya=' + str(ya) + ' yb=' + str(yb) + ' za=' + str(za) + ' zb=' + str(zb) + ' colour=#000022 type=dashed line_weight="thick"'
        cmd_lines.append(join_line) 
        #print(pair)
    """  
    
    
    """
    cmd_lines = []    
    for i in range(len(nl)):
      for j in range(len(nl[i])):
        xa = str(nl[i][j][3][0])
        ya = str(nl[i][j][3][1])
        za = str(nl[i][j][3][2])
        xb = str(nl[i][j][4][0])
        yb = str(nl[i][j][4][1])
        zb = str(nl[i][j][4][2])
        
        if(nl[i][j][5] == True and nl[i][j][0] <= 1.8 * ij_min[i]):          
          if(nl[i][j][6]):
            if((abs(1 - nl[i][j][3][2]) <= 0.01) and (abs(1 - nl[i][j][4][2]) <= 0.01)):
              join_line = 'line xa=' + xa + ' xb=' + xb + ' ya=' + ya + ' yb=' + yb + ' za=' + za + ' zb=' + zb + ' colour=#000022 type=solid line_weight="ultra thick"'
              cmd_lines.append(join_line) 
            else:
              join_line = 'line xa=' + xa + ' xb=' + xb + ' ya=' + ya + ' yb=' + yb + ' za=' + za + ' zb=' + zb + ' colour=#000022 type=solid line_weight="thin"'
              cmd_lines.append(join_line) 
          else:  
            join_line = 'line xa=' + xa + ' xb=' + xb + ' ya=' + ya + ' yb=' + yb + ' za=' + za + ' zb=' + zb + ' colour=#000022 type=dashed line_weight="thick"'
            cmd_lines.append(join_line) 
        #if(nl[i][j][5] == False and nl[i][j][0] <= 1.05 * ij_min_na[i]):
        #(abs(nl[i][j][0] - cell_diag) > (0.05 * cell_diag))
        if(nl[i][j][5] == False and (nl[i][j][0] <= 1.05 * ij_min_na[i]) and nl[i][j][0] < 0.7 * cell_diag):
          #print(ij_min_na[i], nl[i][j][0], cell_diag)
          join_line = 'line xa=' + xa + ' xb=' + xb + ' ya=' + ya + ' yb=' + yb + ' za=' + za + ' zb=' + zb + ' colour=#000022 type=dashed line_weight="thin"'
          #cmd_lines.append(join_line) 
    """  
    """  
        xa = atom_j[3][0]
        ya = atom_j[3][1]
        za = atom_j[3][2]
        xb = atom_j[4][0]
        yb = atom_j[4][1]
        zb = atom_j[4][2]
        
        axis_line = False
        if(abs(xa - xb) <= 1.0e-5 and abs(ya - yb) <= 1.0e-5):
          axis_line = True
        elif(abs(xa - xb) <= 1.0e-5 and abs(za - zb) <= 1.0e-5):
          axis_line = True
        elif(abs(ya - yb) <= 1.0e-5 and abs(za - zb) <= 1.0e-5):
          axis_line = True
          
        xa = str(xa)
        ya = str(ya)
        za = str(za)
        xb = str(xb)
        yb = str(yb)
        zb = str(zb)
        
        if(axis_line):
          join_line = 'line xa=' + xa + ' xb=' + xb + ' ya=' + ya + ' yb=' + yb + ' za=' + za + ' zb=' + zb + ' colour=#000066 type=solid'
          cmd_lines.append(join_line) 
    """
    
    """
    for pair in nl:
      xa = str(pair[2][0])
      ya = str(pair[2][1])
      za = str(pair[2][2])
      xb = str(pair[3][0])
      yb = str(pair[3][1])
      zb = str(pair[3][2])
      
      print(xa, ya, za, xb, yb, zb)
      
      axis_line = False
      if(abs(pair[2][0] - pair[3][0]) <= 1.0e-5 and abs(pair[2][1] - pair[3][1]) <= 1.0e-5):
        axis_line = True
      elif(abs(pair[2][0] - pair[3][0]) <= 1.0e-5 and abs(pair[2][2] - pair[3][2]) <= 1.0e-5):
        axis_line = True
      elif(abs(pair[2][1] - pair[3][1]) <= 1.0e-5 and abs(pair[2][2] - pair[3][2]) <= 1.0e-5):
        axis_line = True
    
      line_type = 'dashed'
      if(axis_line):
        line_type = 'solid'
        
        
      join_line = 'line xa=' + xa + ' xb=' + xb + ' ya=' + ya + ' yb=' + yb + ' za=' + za + ' zb=' + zb + ' colour=#000066 type=' + line_type
      cmd_lines.append(join_line) 
    """
    
    
    
    