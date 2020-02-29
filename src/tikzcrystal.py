######################################################
#  Ben Palmer University of Birmingham 2020
#  Free to use
######################################################

import numpy
import os
import sys
import operator
from read import read
from colours import colours
from crystal import crystal
from grid import grid

class tikzcrystal:

  def __init__(self):
    self.build = True
    self.latex = ''
    self.latex_colour = ''
    self.latex_background = ''
    self.latex_content = ''
    self.data = []
    self.colours_set = []
    self.space = {'a':5, 'b':5, 'c':5, 'alpha':90, 'beta':90, 'gamma':90, 'gx': 4, 'gy': 4, 'gz': 4, 'zdepth': 1.0, 'zscale': 0.8, 'rx': 0, 'ry': 0, 'rz': 0}
    self.grid = [] 
    self.zballscale = 0.5
    self.cmd_name = 'printtikzcrystal'
    self.cmd_prefix = ''

  def main(self):
  
    # Load
    self.data = read.read_file("input.in")
         
    # Space
    if('space' in self.data.keys() and len(self.data['space']) == 1):
      self.space['a'] = float(self.data['space'][0]['a'][0])
      self.space['b'] = float(self.data['space'][0]['b'][0])
      self.space['c'] = float(self.data['space'][0]['c'][0])
      self.space['alpha'] = float(self.data['space'][0]['alpha'][0])
      self.space['beta'] = float(self.data['space'][0]['beta'][0])
      self.space['gamma'] = float(self.data['space'][0]['gamma'][0])
      self.space['gx'] = int(self.data['space'][0]['gx'][0])
      self.space['gy'] = int(self.data['space'][0]['gy'][0])
      self.space['gz'] = int(self.data['space'][0]['gz'][0])
      self.space['background'] = self.data['space'][0]['background'][0]
      self.space['zdepth'] = float(self.data['space'][0]['zdepth'][0])
      self.space['zscale'] = float(self.data['space'][0]['zscale'][0])
      
      if('rotate' in self.data['space'][0].keys()):
        self.space['rx'] = float(self.data['space'][0]['rotate'][0]) / 57.295779513
        self.space['ry'] = float(self.data['space'][0]['rotate'][1]) / 57.295779513
        self.space['rz'] = float(self.data['space'][0]['rotate'][2]) / 57.295779513
   
    # Grid
    if('grid' in self.data.keys() and len(self.data['grid']) >= 1):
      for g in self.data['grid']:
        new_grid = grid.default()
     
        new_grid['make'] = True
        if('cx' in g.keys()):
          new_grid['cx'] = int(g['cx'][0])
        if('cy' in g.keys()):
          new_grid['cy'] = int(g['cy'][0])
        if('cz' in g.keys()):
          new_grid['cz'] = int(g['cz'][0])
        if('alpha' in g.keys()):
          new_grid['alpha'] = float(g['alpha'][0]) / 57.295779513
        if('beta' in g.keys()):
          new_grid['beta'] = float(g['beta'][0]) / 57.295779513
        if('gamma' in g.keys()):
          new_grid['gamma'] = float(g['gamma'][0]) / 57.295779513
        if('a' in g.keys()):
          new_grid['a'] = float(g['a'][0])
        if('b' in g.keys()):
          new_grid['b'] = float(g['b'][0])
        if('c' in g.keys()):
          new_grid['c'] = float(g['c'][0])
        if('gridtype' in g.keys()):
          new_grid['gridtype'] = g['gridtype'][0]
        
        if('lines' in g.keys()):
          new_grid['lines'] = line.read_details(g['lines'])
        else:        
          new_grid['lines'] = line.read_details('')
          
        
        self.grid.append(new_grid)

      
      """
      self.grid['make'] = True
      if('cx' in self.data['grid'][0].keys()):
        self.grid['cx'] = int(self.data['grid'][0]['cx'][0])
      if('cy' in self.data['grid'][0].keys()):
        self.grid['cy'] = int(self.data['grid'][0]['cy'][0])
      if('cz' in self.data['grid'][0].keys()):
        self.grid['cz'] = int(self.data['grid'][0]['cz'][0])
      if('alpha' in self.data['grid'][0].keys()):
        self.grid['alpha'] = float(self.data['grid'][0]['alpha'][0]) / 57.295779513
      if('beta' in self.data['grid'][0].keys()):
        self.grid['beta'] = float(self.data['grid'][0]['beta'][0]) / 57.295779513
      if('gamma' in self.data['grid'][0].keys()):
        self.grid['gamma'] = float(self.data['grid'][0]['gamma'][0]) / 57.295779513
      if('a' in self.data['grid'][0].keys()):
        self.grid['a'] = float(self.data['grid'][0]['a'][0])
      if('b' in self.data['grid'][0].keys()):
        self.grid['b'] = float(self.data['grid'][0]['b'][0])
      if('c' in self.data['grid'][0].keys()):
        self.grid['c'] = float(self.data['grid'][0]['c'][0])
      """  
          
    
    # Command Name
    if('tikzcommands' in self.data.keys() and len(self.data['tikzcommands']) == 1):
      self.cmd_name = self.data['tikzcommands'][0]['cmd_name'][0]
    
    # Prefix
    if('tikzcommands' in self.data.keys() and len(self.data['tikzcommands']) == 1):
      if('tex_prefix' in self.data['tikzcommands'][0].keys() and len(self.data['tikzcommands'][0]['tex_prefix']) == 1):
        self.cmd_prefix = self.data['tikzcommands'][0]['tex_prefix'][0]

    
    # Background 
    self.background()

    # Make Crystal
    self.make_crystal()
    
    self.make_grid()
    
    # Sort out colours
    self.colours()
    
        
    self.draw()
    self.out()


  def colours(self):
    for key in self.data.keys():
      for i in range(len(self.data[key])):
        if('colour' in self.data[key][i].keys()):
          self.data[key][i]['colour_key'] = []
          for j in range(len(self.data[key][i]['colour'])):
            colour_key, r, g, b, line = colours.to_latex(self.data[key][i]['colour'][j])
            if(colour_key not in self.colours_set):
              self.colours_set.append(colour_key)
              self.latex_colour += line + '\n'
            self.data[key][i]['colour_key'].append(colour_key)


  def background(self):
    if('space' not in self.data.keys()):
      return ''
      
    if(self.space['background'].strip().upper() == 'NONE'):
      return ''
  
    # Make Axis
    self.make_axis()
    self.make_colour_background()
    """
    # Start Command
    self.latex_background += '%% DRAW LINE\n'
    self.latex_background += '\\newcommand{\\tikzcrystalbackground}[0]{\n'
  
    # Get Corners
    xa, ya, za = self.transform_space(0,0,0)  
    xb, yb, zb = self.transform_space(0,0,1)
    xc, yc, zc = self.transform_space(1,0,1)
    xd, yd, zd = self.transform_space(1,0,0)
    xe, ye, ze = self.transform_space(0,1,0)
    xf, yf, zf = self.transform_space(0,1,1)
    xg, yg, zg = self.transform_space(1,1,1)
    xh, yh, zh = self.transform_space(1,1,0)
    a = self.latex_coord(xa, ya, za)
    b = self.latex_coord(xb, yb, zb)
    c = self.latex_coord(xc, yc, zc)
    d = self.latex_coord(xd, yd, zd)
    e = self.latex_coord(xe, ye, ze)
    f = self.latex_coord(xf, yf, zf)
    g = self.latex_coord(xg, yg, zg)
    h = self.latex_coord(xh, yh, zh)
    
    # FILLS
    self.latex_background += '\\fill[' + colour1+'!30,opacity=1.0] ' + a + ' -- ' + b + ' -- ' + c + ' -- ' + d + ' -- cycle;     %% bottom square\n'
    self.latex_background += '\\fill[' + colour1+'!10,opacity=1.0] ' + a + ' -- ' + d + ' -- ' + h + ' -- ' + e + ' -- cycle;     %% rear square\n'
    self.latex_background += '\\fill[' + colour1+'!15,opacity=1.0] ' + a + ' -- ' + b + ' -- ' + f + ' -- ' + e + ' -- cycle;     %% side square\n'
    
    # OUTLINE
    self.latex_background += '\\draw[] '+a+' -- '+e+' -- '+f+' -- '+g+' -- '+c+' -- '+d+' -- '+a+'; \n'
    
    # DASHED/HIDEN LINES
    self.latex_background += '\\draw[dashed] ' + a + ' -- ' + b + '; \n'
    self.latex_background += '\\draw[dashed] ' + a + ' -- ' + d + '; \n' 
    self.latex_background += '\\draw[dashed] ' + a + ' -- ' + e + '; \n'
    
    # GRIDS X
    if(self.space['gx']>0):
      for i in range(self.space['gx'] - 1):
        x = (i + 1) / self.space['gx']
        xa, ya, za = self.transform_space(x,0,1) 
        xb, yb, zb = self.transform_space(x,0,0) 
        xc, yc, zc = self.transform_space(x,1,0) 
        a = self.latex_coord(xa, ya, za)
        b = self.latex_coord(xb, yb, zb)
        c = self.latex_coord(xc, yc, zc)
        self.latex_background += '\\draw[dashed,gray,very thin] ' + a + ' -- ' + b + ' -- ' + c + '; \n'    
    
    # GRIDS Y
    if(self.space['gy']>0):
      for i in range(self.space['gy'] - 1):
        y = (i + 1) / self.space['gy']
        xa, ya, za = self.transform_space(0,y,1) 
        xb, yb, zb = self.transform_space(0,y,0) 
        xc, yc, zc = self.transform_space(1,y,0) 
        a = self.latex_coord(xa, ya, za)
        b = self.latex_coord(xb, yb, zb)
        c = self.latex_coord(xc, yc, zc)
        self.latex_background += '\\draw[dashed,gray,very thin] ' + a + ' -- ' + b + ' -- ' + c + '; \n'
    
    # GRIDS Z
    if(self.space['gz']>0):
      for i in range(self.space['gz'] - 1):
        z = (i + 1) / self.space['gz']
        xa, ya, za = self.transform_space(0,1,z) 
        xb, yb, zb = self.transform_space(0,0,z) 
        xc, yc, zc = self.transform_space(1,0,z) 
        a = self.latex_coord(xa, ya, za)
        b = self.latex_coord(xb, yb, zb)
        c = self.latex_coord(xc, yc, zc)
        self.latex_background += '\\draw[dashed,gray,very thin] ' + a + ' -- ' + b + ' -- ' + c + '; \n'
    

    
    # End Command
    self.latex_background += '}\n'
    """ 

    
  def draw(self):
    # Start command
    self.latex_content = '\\newcommand{\\' + self.cmd_prefix + self.cmd_name + '}[0]{\n'
  
    layers = []    
    command = ('line','ball','circle','fill',)
    
    for c in command:
      if(c in self.data.keys()):      
        for i in range(len(self.data[c])):
          o = self.data[c][i]        
          z = 0.0
          if('z' in o.keys()):
            z = round(float(o['z'][0]),5)
          elif('za' in o.keys()):
            z = round(min(float(o['za'][0]),float(o['zb'][0])),5)
          l = 10  # Default layer
          if('layer' in o.keys()):
            l = int(o['layer'][0])
          layers.append([o,i,l,self.space['zdepth']*z])
    
    # Sort
    layers = sorted(layers, key=operator.itemgetter(2, 3))  
    
    # Draw
    for l in layers:
      cmd = l[0]
      if(cmd['COMMAND'].lower().strip() == 'ball'):
        self.latex_content += self.draw_ball(cmd)
      if(cmd['COMMAND'].lower().strip() == 'line'):
        self.latex_content += self.draw_line(cmd)
      if(cmd['COMMAND'].lower().strip() == 'fill'):
        self.latex_content += self.draw_fill(cmd)
      
    # End command
    self.latex_content += '}\n'
    return ''
    
    
    
    
    
    
  def draw_ball(self, cmd):   
    if(cmd['COMMAND'].lower().strip() != 'ball'):
      return ''
      
    out = ''
      
    # Defaults
    p = tikzcrystal.tikz_item()
    p = self.readit(p, cmd)
    
    p['x'] = float(p['x'])
    p['y'] = float(p['y'])
    p['z'] = float(p['z'])
    p['r'] = float(p['r'])
    
    x = round(float(p['x']),5)
    y = round(float(p['y']),5)
    z = round(float(p['z']),5)  
    r = round(float(p['r']),5)
    
    
    z_scale = self.space['zscale'] ** (1.0 - z)
      
    if(p['spacetransform']):    
      x, y, z = self.transform_space(x, y, z, 5)  
    
    out += '\\tikzdrawatom{' + p['colour_key'] + '}{' + str(x) + '}{' + str(y) + '}{' + str(self.space['zdepth']*z) + '}{' + str(z_scale*r) + '} \n'
    
    return out
    
    
  def draw_line(self, cmd):   
    if(cmd['COMMAND'].lower().strip() != 'line'):
      return ''
      
    out = ''
      
    # Defaults
    p = tikzcrystal.tikz_item()
         
    p = self.readit(p, cmd)
    p['xa'] = float(p['xa'])
    p['ya'] = float(p['ya'])
    p['za'] = float(p['za'])
    p['xb'] = float(p['xb'])
    p['yb'] = float(p['yb'])
    p['zb'] = float(p['zb'])
    
    xa = float(p['xa'])
    ya = float(p['ya'])
    za = self.space['zdepth'] * float(p['za'])  
    xb = float(p['xb'])
    yb = float(p['yb'])
    zb = self.space['zdepth'] * float(p['zb'])  
      
    if(p['spacetransform']):    
      xa, ya, za = self.transform_space(xa, ya, za)
      xb, yb, zb = self.transform_space(xb, yb, zb)
    
    # Get Coords
    a = self.latex_coord(xa, ya, za)
    b = self.latex_coord(xb, yb, zb)
      
    out += '\\draw[' + p['type'] + ', ' + p['colour_key'] + ', ' + p['line_weight'] + '] ' + a + ' -- ' + b + '; \n'
      
    return out
    
  def draw_arc(self, cmd):   
    if(cmd['COMMAND'].lower().strip() != 'arc'):
      return ''      
    out = ''  
    
    out += '\\draw[' + p['colour_key'] + '] (0,0) arc (70:120:1); \n'
    
    
    
    
  def draw_fill(self, cmd):   
    if(cmd['COMMAND'].lower().strip() != 'fill'):
      return ''  
      
    out = ''
    
    # Defaults
    p = tikzcrystal.tikz_item()
    p = self.readit(p, cmd)
    
    xa, ya, za = float(p['xa']), float(p['ya']), self.space['zdepth'] * float(p['za'])
    xb, yb, zb = float(p['xb']), float(p['yb']), self.space['zdepth'] * float(p['zb'])
    xc, yc, zc = float(p['xc']), float(p['yc']), self.space['zdepth'] * float(p['zc'])
    xd, yd, zd = float(p['xd']), float(p['yd']), self.space['zdepth'] * float(p['zd'])
    
    if(p['spacetransform']):    
      xa, ya, za = self.transform_space(xa, ya, za)
      xb, yb, zb = self.transform_space(xb, yb, zb)
      xc, yc, zc = self.transform_space(xc, yc, zc)
      xd, yd, zd = self.transform_space(xd, yd, zd)
    
    # Get Coords
    a = self.latex_coord(xa, ya, za)
    b = self.latex_coord(xb, yb, zb)
    c = self.latex_coord(xc, yc, zc)
    d = self.latex_coord(xd, yd, zd)
    
    out += '\\fill[' + p['colour_key'] + '!' + p['shade'] + ',opacity=1.0] ' + a + ' -- ' + b + ' -- ' + c + ' -- ' + d + ' -- cycle;     %% bottom square\n'
    
    return out
    
    
  def tikz_item():  
    return {
      'x': 0.0, 'y': 0.0, 'z': 0.0,
      'xa': 0.0, 'ya': 0.0, 'za': 0.0, 
      'xb': 0.0, 'yb': 0.0, 'zb': 0.0, 
      'xc': 0.0, 'yc': 0.0, 'zc': 0.0, 
      'xd': 0.0, 'yd': 0.0, 'zd': 0.0, 
      'r': 0.1,
      'colour': '#000000', 'colour_key': '', 
      'shade': 100,
      'spacetransform': True,
      'type':  'solid',
      'line_weight': 'thin',
    }
    

  def readit(self, default, inp):
    for k in default.keys():
      if k in inp.keys():
        if(len(inp[k]) == 1):
          default[k] = inp[k][0]
        else:
          default[k] = inp[k]
    return default


  def out(self):
  
    # Add Colours
    self.latex += self.latex_colour + "\n" 
    
    # Define drawing commands
    self.latex += """ 
%% DRAW LINE
\\newcommand{\\tikzdrawline}[7]{
\\draw[#1] (#2,#4,#3) -- (#5,#7,#6);  
}
%% DRAW BALL
\\newcommand{\\tikzdrawatom}[5]{%
\\filldraw[ball color=#1] (#2,#3,#4) circle[radius=#5];
}  
"""

    # Add Background
    #self.latex += self.latex_background + "\n" 
    
    
    self.latex += self.latex_content + "\n"

    # WRITE OUT TEST
    
    fh = open("out.tex", 'w')
    
    fh.write("""\\documentclass[11pt,twoside]{article}
%% Tikz package
\\usepackage{tikz}
\\usepackage{tikz-dimline}
\\usetikzlibrary{shapes,arrows,3d}
\\usetikzlibrary{math}
\\pagestyle{plain}
""")    

    fh.write(self.latex)
    
    fh.write("""\\begin{document}
\\begin{tikzpicture}
""")
    fh.write("\\" + self.cmd_name + "{}\n")
    fh.write("""\\end{tikzpicture} 
\\end{document}
""")  
    fh.close()
    
    # Run Latex
    if(self.build):
      cmd = "pdflatex out.tex"
      os.system(cmd)


  def make_crystal(self):
    if('crystal' not in self.data.keys() or len(self.data['crystal']) == 0):
      return ''
    for c in self.data['crystal']:
      cmd = crystal.make(c)
      if(len(cmd)>0):
        for line in cmd:
          self.data = read.read_line(self.data, line)
          
          
  def make_grid(self):
    cmd = grid.make(self.grid)
    if(len(cmd)>0):
      for line in cmd:
        self.data = read.read_line(self.data, line)
    
          
    
  def make_axis(self):
  
    if(self.space['background'].strip().upper() != 'AXIS'):
      return ''

    xa, ya, za = 0, 0, 0
    xb, yb, zb = 1, 0, 0 
    line = 'line colour=#000000 type=dashed layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
    
    xa, ya, za = 0, 0, 0
    xb, yb, zb = 0, 1, 0 
    line = 'line colour=#000000 type=dashed layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
  
    xa, ya, za = 0, 0, 0
    xb, yb, zb = 0, 0, 1
    line = 'line colour=#000000 type=dashed layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
    
    xa, ya, za = 0, 0, 0
    xb, yb, zb = 0, 0, 1  
    xc, yc, zc = 0, 1, 1  
    xd, yd, zd = 0, 1, 0
    line =  'fill layer=1 colour=#336699 shade=10 '
    line += 'xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' '
    line += 'xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ' '
    line += 'xc=' + str(xc) + ' yc=' + str(yc) + ' zc=' + str(zc) + ' '
    line += 'xd=' + str(xd) + ' yd=' + str(yd) + ' zd=' + str(zd) + ' '
    self.data = read.read_line(self.data, line)
    
    xa, ya, za = 0, 0, 0
    xb, yb, zb = 0, 1, 0  
    xc, yc, zc = 1, 1, 0  
    xd, yd, zd = 1, 0, 0  
    line =  'fill layer=1 colour=#336699 shade=15 '
    line += 'xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' '
    line += 'xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ' '
    line += 'xc=' + str(xc) + ' yc=' + str(yc) + ' zc=' + str(zc) + ' '
    line += 'xd=' + str(xd) + ' yd=' + str(yd) + ' zd=' + str(zd) + ' '    
    self.data = read.read_line(self.data, line)
    
    xa, ya, za = 0, 0, 0
    xb, yb, zb = 1, 0, 0  
    xc, yc, zc = 1, 0, 1  
    xd, yd, zd = 0, 0, 1
    line =  'fill layer=1 colour=#336699 shade=30 '
    line += 'xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' '
    line += 'xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ' '
    line += 'xc=' + str(xc) + ' yc=' + str(yc) + ' zc=' + str(zc) + ' '
    line += 'xd=' + str(xd) + ' yd=' + str(yd) + ' zd=' + str(zd) + ' '    
    self.data = read.read_line(self.data, line)
  
    xa, ya, za = 1, 0, 0
    xb, yb, zb = 1, 0, 1  
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
  
    xa, ya, za = 1, 0, 1
    xb, yb, zb = 0, 0, 1  
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
  
    xa, ya, za = 0, 0, 1
    xb, yb, zb = 0, 1, 1  
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
  
    xa, ya, za = 0, 1, 1
    xb, yb, zb = 0, 1, 0
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
  
    xa, ya, za = 0, 1, 0
    xb, yb, zb = 1, 1, 0  
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
  
    xa, ya, za = 1, 1, 0
    xb, yb, zb = 1, 0, 0  
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
    
    
  
    xa, ya, za = 1, 1, 1
    xb, yb, zb = 1, 0, 1 
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)  

    xa, ya, za = 1, 1, 1
    xb, yb, zb = 0, 1, 1  
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)  

    xa, ya, za = 1, 1, 1
    xb, yb, zb = 1, 1, 0  
    line = 'line colour=#000000 type=solid layer=2 xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ''
    self.data = read.read_line(self.data, line)
    

         
    
  def make_colour_background(self):
  
    if(self.space['background'].strip().upper() != 'COLOUR'):
      return ''

   
    xa, ya, za = 0, 0, 0
    xb, yb, zb = 0, 0, 1  
    xc, yc, zc = 0, 1, 1  
    xd, yd, zd = 0, 1, 0
    line =  'fill layer=1 colour=#336699 shade=10 '
    line += 'xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' '
    line += 'xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ' '
    line += 'xc=' + str(xc) + ' yc=' + str(yc) + ' zc=' + str(zc) + ' '
    line += 'xd=' + str(xd) + ' yd=' + str(yd) + ' zd=' + str(zd) + ' '
    self.data = read.read_line(self.data, line)
    
    xa, ya, za = 0, 0, 0
    xb, yb, zb = 0, 1, 0  
    xc, yc, zc = 1, 1, 0  
    xd, yd, zd = 1, 0, 0  
    line =  'fill layer=1 colour=#336699 shade=15 '
    line += 'xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' '
    line += 'xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ' '
    line += 'xc=' + str(xc) + ' yc=' + str(yc) + ' zc=' + str(zc) + ' '
    line += 'xd=' + str(xd) + ' yd=' + str(yd) + ' zd=' + str(zd) + ' '    
    self.data = read.read_line(self.data, line)
    
    xa, ya, za = 0, 0, 0
    xb, yb, zb = 1, 0, 0  
    xc, yc, zc = 1, 0, 1  
    xd, yd, zd = 0, 0, 1
    line =  'fill layer=1 colour=#336699 shade=30 '
    line += 'xa=' + str(xa) + ' ya=' + str(ya) + ' za=' + str(za) + ' '
    line += 'xb=' + str(xb) + ' yb=' + str(yb) + ' zb=' + str(zb) + ' '
    line += 'xc=' + str(xc) + ' yc=' + str(yc) + ' zc=' + str(zc) + ' '
    line += 'xd=' + str(xd) + ' yd=' + str(yd) + ' zd=' + str(zd) + ' '    
    self.data = read.read_line(self.data, line)
  
    
    
  
  def transform_space(self, x, y, z, round_p = 8):
  
    a = self.space['a']
    b = self.space['b']
    c = self.space['c']
    
    rx = self.space['rx']
    ry = self.space['ry']
    rz = self.space['rz']
  
    alpha = self.space['alpha']
    beta = self.space['beta']
    gamma = self.space['gamma']
  
    x, y, z = self.transform(x, y, z, a, b, c, alpha, beta, gamma, round_p)    
    x, y, z = self.rotate(x, y, z, rx, ry, rz)
  
    return x, y, z


  def transform(self, x, y, z, a, b, c, alpha, beta, gamma, round_p = 8):
  
    alpha = numpy.deg2rad(alpha)
    beta = numpy.deg2rad(beta)
    gamma = numpy.deg2rad(gamma)
  
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

    return round(yvec[0], round_p), round(yvec[1], round_p), round(yvec[2], round_p)
    
    
  def rotate(self, x, y, z, rx, ry, rz, round_p = 8):
    """
    rx_mat = numpy.zeros((3,3,),)
    rx_mat[0,0] = 1
    rx_mat[0,1] = 0
    rx_mat[0,2] = 0
    rx_mat[1,0] = 0
    rx_mat[1,1] = numpy.cos(rx)
    rx_mat[1,2] = -numpy.sin(rx)
    rx_mat[2,0] = 0
    rx_mat[2,1] = numpy.sin(rx)
    rx_mat[2,2] = numpy.cos(rx)
    
    ry_mat = numpy.zeros((3,3,),)
    ry_mat[0,0] = numpy.cos(ry)
    ry_mat[0,1] = 0
    ry_mat[0,2] = numpy.sin(ry)
    ry_mat[1,0] = 0
    ry_mat[1,1] = 1
    ry_mat[1,2] = 0
    ry_mat[2,0] = -numpy.sin(rx)
    ry_mat[2,1] = 0
    ry_mat[2,2] = numpy.cos(rx)
    
    rz_mat = numpy.zeros((3,3,),)
    rz_mat[0,0] = numpy.cos(rz)
    rz_mat[0,1] = -numpy.sin(ry)
    rz_mat[0,2] = 0
    rz_mat[1,0] = numpy.sin(rx)
    rz_mat[1,1] = numpy.cos(rx)
    rz_mat[1,2] = 0
    rz_mat[2,0] = 0
    rz_mat[2,1] = 0
    rz_mat[2,2] = 1
    
    m = numpy.matmul(rz_mat, ry_mat)
    m = numpy.matmul(m, rx_mat)
    """
    
    m = numpy.zeros((3,3,),)
    m[0,0] = numpy.cos(rz) * numpy.cos(ry)
    m[0,1] = numpy.cos(rz) * numpy.sin(ry) * numpy.sin(rx) - numpy.sin(rz) * numpy.cos(rx)
    m[0,2] = numpy.cos(rz) * numpy.sin(ry) * numpy.cos(rx) + numpy.sin(rz) * numpy.sin(rx)
    m[1,0] = numpy.sin(rz) * numpy.cos(ry) 
    m[1,1] = numpy.sin(rz) * numpy.sin(ry) + numpy.cos(rz) * numpy.cos(rx)
    m[1,2] = numpy.sin(rz) * numpy.sin(ry) * numpy.cos(rx) - numpy.cos(rz) * numpy.sin(rx)
    m[2,0] = -numpy.sin(ry)
    m[2,1] = numpy.cos(ry) * numpy.sin(rx)
    m[2,2] = numpy.cos(ry) * numpy.cos(rx)    
    
    a = numpy.zeros((3,),)
    a[0] = x
    a[1] = y
    a[2] = z
    
    b = numpy.matmul(m, a)
    
    return round(b[0], round_p), round(b[1], round_p), round(b[2], round_p)
    
  
  def latex_coord(self, x, y, z):  
    return '(' + str(round(x,5)) + ',' + str(round(y,5)) + ',' + str(round(z,5)) + ')'

