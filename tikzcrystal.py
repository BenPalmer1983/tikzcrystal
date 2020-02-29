######################################################
#  TIKZCRYSTAL
######################################################
#  Ben Palmer University of Birmingham 2020
#  Free to use
######################################################


#!/bin/python3
########################################################################
import os
import datetime
import re
import sys
import numpy
import operator

###########################################
#  CLASS tikzcrysta
###########################################
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

###########################################
#  CLASS rea
###########################################
class read:
  
  @staticmethod
  def read_file(file_path):
    input = {}
    fh = open(file_path, 'r')
    for line in fh:
      input = read.read_line(input, line)
    fh.close()
    return input
    
  @staticmethod
  def read_line(input, line):
    line = line.strip()
    if(len(line) > 0 and line[0] != "#"):
      cmd, data = read.get_fields_dict(line)
      if(cmd not in input.keys()):
        input[cmd] = []
      input[cmd].append(data)
    return input
        
  @staticmethod  
  def get_fields_dict(line): 
    fields = read.split_by(line, ' ')    
    dict = {}    
    dict['COMMAND'] = fields[0]
    
    for field in fields:
      f = field.split("=")
      if(len(f) == 2):
        fb = read.split_by(f[1], ',')
        fkey = f[0].lower()
        
        if(fkey in dict.keys()):
          if(dict[fkey][0] != fkey):
            temp = dict[fkey]
            dict[fkey] = [fkey, temp]
            if(len(fb) == 1):
              dict[fkey].append([f[1]])
            elif(len(fb) > 1):
              dict[fkey].append(fb)
          else:       
            if(len(fb) == 1):
              dict[fkey].append([f[1]])
            elif(len(fb) > 1):
              dict[fkey].append(fb)
        else:  
          if(len(fb) == 1):
            dict[fkey] = [f[1]]
          elif(len(fb) > 1):
            dict[fkey] = fb
    
    return fields[0], dict
          
  @staticmethod  
  def split_by(line, sep=' ', ignore_double_sep=True):
    last_char = None
    in_quotes = 0
    fields = []
    temp_line = ""
    
    for char in line:
      if(char == "'" and in_quotes == 0 and last_char != "\\"):
        in_quotes = 1
      elif(char == "'" and in_quotes == 1 and last_char != "\\"):
        in_quotes = 0
      elif(char == '"' and in_quotes == 0 and last_char != "\\"):
        in_quotes = 2
      elif(char == '"' and in_quotes == 2 and last_char != "\\"):
        in_quotes = 0
      elif(in_quotes > 0):
        temp_line = temp_line + char
      elif(in_quotes == 0 and char != sep):
        temp_line = temp_line + char
      elif(char == sep and last_char == sep and ignore_double_sep):
        pass
      elif(char == sep):
        fields.append(temp_line)
        temp_line = "" 
    if(temp_line != ""):
      fields.append(temp_line)
    
    return fields

###########################################
#  CLASS colour
###########################################
class colours:

  def lighten(colour_in, d):
    colour_in = colour_in.replace('#','')
    r = int(colour_in[0:2],16)
    g = int(colour_in[2:4],16)
    b = int(colour_in[4:6],16)
    
    r = int(min(max(0,(1 + d) * r),255))
    g = int(min(max(0,(1 + d) * g),255))
    b = int(min(max(0,(1 + d) * b),255))
    
    if(r < 16):
      r = '0' + str(colours.dentohex(r))
    else:
      r = str(colours.dentohex(r))
      
    if(g < 16):
      g = '0' + str(colours.dentohex(g))
    else:
      g = str(colours.dentohex(g))
      
    if(b < 16):
      b = '0' + str(colours.dentohex(b))
    else:
      b = str(colours.dentohex(b))
    
    colour_out = '#' + r + g + b    
    
    return colour_out
    
  def dentohex(a):
    hexchars = "0123456789ABCDEF"
    output = ''
    if(a == 0):
      return '0'
    while(a > 0):
      b = a % 16
      a = int(numpy.floor(a / 16))
      output = hexchars[b] + output 
    return output
    
  def hextoden(a):
    b = 0
    hexchars = "0123456789ABCDEF"
    for i in range(len(a)):
      k = len(a) - (i + 1)
      n = 0
      for j in range(len(hexchars)):
        if(a[k].upper() == hexchars[j]):
          n = j
          break
      b = b + n * 16**i
    return b
    
  def to_latex(colour, prefix=''):
    if(len(colour) != 7 and colour[0] != "#"):
      return ''
    colour_key = colours.colour_key(colour)
    r,g,b = colours.rgb(colour)
    return colour_key, r, g, b, '\definecolor{'+colour_key+'}{RGB}{'+str(r)+','+str(g)+','+str(b)+'}'
  
  def rgb(colour):
    colour = colour.upper().strip()
    if(len(colour) != 7 and colour[0] != "#"):
      return 0,0,0
    return colours.hextoden(colour[1:3]),colours.hextoden(colour[3:5]), colours.hextoden(colour[5:7])
    
  def colour_key(colour):
    if(len(colour) != 7 and colour[0] != "#"):
      return ''
    return 'col_' + colour.replace('#','').lower()
  
###########################################
#  CLASS crysta
###########################################
class crystal:

  @staticmethod
  def make(crys_in):
    cmd_lines = []
    
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
            'lines_vertex': ['#000000','none','solid'],
            'lines_subcells': ['#000000','none','solid'],
            'lines_diag': ['#000000','none','solid'],
            'v': [],
            'i': [],
            'iline': [],
            'ilines': [],
            'vacancy': [],
            'interstitial': [],
            'interstitial_xyz': [],
            'file': None,
            'file_xyz': None,
           } 
           
    for k in crys.keys(): 
      if(k in crys_in.keys()):
        crys[k] = crys_in[k]
        
# Is the crystal in a file?
    crys = crystal.read_file(crys)    
        
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
    
# Read Vacancies
    if(len(crys['v']) >= 3):
      if(crys['v'][0] == 'v'):
        for v in crys['v']:
          if(len(v) >= 3):
            crys['vacancy'].append(v)
      else:
        v = crys['v']
        if(len(v) >= 3):
          crys['vacancy'].append(v)
          
# Interstitials
    if(len(crys['i']) >= 3):
      if(crys['i'][0] == 'i'):
        for interstitial_t in crys['i']:
          if(len(interstitial_t) >= 3):
            try:
              interstitial = [[None],[None],[None],[],[],[]]  # x y z colour lines/nolines key
              if(len(interstitial_t)>=3):
                interstitial[0] = float(interstitial_t[0])
                interstitial[1] = float(interstitial_t[1])
                interstitial[2] = float(interstitial_t[2])
              if(len(interstitial_t)>=4):
                interstitial[3] = str(interstitial_t[3])
              else:
                interstitial[3] = '#666666'
              if(len(interstitial_t)>=5):
                interstitial[4] = str(interstitial_t[4]).lower()
              else:
                interstitial[4] = 'nolines'
              if(len(interstitial_t)>=6):
                interstitial[5] = str(interstitial_t[5]).lower()
                if(interstitial[5] == 0 or interstitial[5] == 'none'):
                  interstitial[5] = None
              else:
                interstitial[5] = None
              crys['interstitial'].append(interstitial)    
            except:
              pass
      else:
        interstitial_t = crys['i']
        if(len(interstitial_t) >= 3):
          try:
            interstitial = [[],[],[],[],[],[]]  # x y z colour lines/nolines key
            if(len(interstitial_t)>=3):
              interstitial[0] = float(interstitial_t[0])
              interstitial[1] = float(interstitial_t[1])
              interstitial[2] = float(interstitial_t[2])              
            if(len(interstitial_t)>=4):
              interstitial[3] = str(interstitial_t[3])
            else:
              interstitial[3] = '#666666'
            if(len(interstitial_t)>=5):
              interstitial[4] = str(interstitial_t[4]).lower()
            else:
              interstitial[4] = 'nolines'
            if(len(interstitial_t)>=6):
              interstitial[5] = str(interstitial_t[5]).lower()
              if(interstitial[5] == 0 or interstitial[5] == 'none'):
                interstitial[5] = None
            else:
              interstitial[5] = None
            crys['interstitial'].append(interstitial)    
          except:
            pass      
            
# Interstitial Lines
    if(len(crys['iline']) >= 2):  
      if(crys['iline'][0] == 'iline'):
        for iline_t in crys['iline'][1:]:
          if(len(iline_t) >= 2 and iline_t[0] != 'iline'):
            try:
              iline = [[None],[None],[],[],[]]   # key1 key2 colour weight type 
              if(len(iline_t)>=2):
                iline[0] = iline_t[0]
                iline[1] = iline_t[1]
              if(len(iline_t)>=3):
                iline[2] = str(iline_t[2])
              else:
                iline[2] = '#666666'
              if(len(iline_t)>=4):
                iline[3] = str(iline_t[3])
              else:
                iline[3] = 'thin'
              if(len(iline_t)>=5):
                iline[4] = str(iline_t[4])
              else:
                iline[4] = 'solid'
              crys['ilines'].append(iline)    
            except:
              pass
      else:
        iline_t = crys['iline']
        if(len(iline_t) >= 2):
          try:
            iline = [[],[],[],[],[]]   # key1 key2 colour weight type 
            if(len(iline_t)>=2):
              iline[0] = iline_t[0]
              iline[1] = iline_t[1]         
            if(len(iline_t)>=3):
              iline[2] = str(iline_t[2])
            else:
              iline[2] = '#666666'
            if(len(iline_t)>=4):
              iline[3] = str(iline_t[3])
            else:
              iline[3] = 'thin'
            if(len(iline_t)>=5):
              iline[4] = str(iline_t[4])
            else:
              iline[4] = 'solid'
            crys['ilines'].append(iline)    
          except:
            pass    

# Make Crystal
    if(ctype == "sc"):
      atoms_t = crystal.make_sc(cx, cy, cz)
    elif(ctype == "bcc"):
      atoms_t = crystal.make_bcc(cx, cy, cz)
    elif(ctype == "fcc"):
      atoms_t = crystal.make_fcc(cx, cy, cz)
    elif(ctype == "ec"):
      atoms_t = crystal.make_ec(cx, cy, cz)
    elif(ctype == "zb"):
      atoms_t = crystal.make_zb(cx, cy, cz)
    elif(ctype == "file"):
      atoms_t = crys['file_atoms_expanded']
    else:
      return cmd_lines
      
# Make atoms and atoms_xyz lists
    atoms = []  
    atoms_xyz = []  
    atoms_colours = []  
    interstitial_xyz = []
    for i in range(len(atoms_t)):
      x, y, z = crystal.ctransform(atoms_t[i][0], atoms_t[i][1], atoms_t[i][2], a, b, c, alpha, beta, gamma)     
      this_colour = colour[i % len(colour)]
# Check for vacancies
      vacancy = False
      for v in crys['vacancy']:
        if(abs(x - float(v[0])) <= 1.0e-5 and abs(y - float(v[1])) <= 1.0e-5 and abs(z - float(v[2])) <= 1.0e-5):
          vacancy = True  
      if(vacancy == False):
        atoms.append(atoms_t[i])      
        atoms_xyz.append([x,y,z])
        atoms_colours.append(this_colour)
        
# Line Interstitials (these may have grid lines drawn to them)
    for i in crys['interstitial']:
      if(i[4].lower() == "lines"):
        x, y, z = crystal.ctransform(i[0], i[1], i[2], a, b, c, alpha, beta, gamma)   
        atoms.append([i[0], i[1], i[2]])    
        atoms_xyz.append([x,y,z])
        atoms_colours.append(i[3])
        try:
          interstitial_xyz.append([i[5],x,y,z])
        except:
          interstitial_xyz.append([None,x,y,z])
        
    min_r, max_r = crystal.neighbour_list(atoms_xyz) 
    if(r == 'auto'):
      r = 0.45 * min_r
      
# Spheres
    for i in range(len(atoms)):
      x, y, z = atoms_xyz[i][0], atoms_xyz[i][1], atoms_xyz[i][2]
      sphere_line = 'ball x=' + str(x) + ' y=' + str(y) + ' z=' + str(z) + ' r=' + str(r) + ' colour=' + atoms_colours[i]
      cmd_lines.append(sphere_line)  
      
# Non Line Interstitials (these don't have grid lines drawn to them)
    for i in crys['interstitial']:
      if(i[4].lower() != "lines"):
        x, y, z = crystal.ctransform(i[0], i[1], i[2], a, b, c, alpha, beta, gamma)   
        sphere_line = 'ball x=' + str(x) + ' y=' + str(y) + ' z=' + str(z) + ' r=' + str(r) + ' colour=' + i[3]
        cmd_lines.append(sphere_line)                 
        try:
          interstitial_xyz.append([i[5],x,y,z])
        except:
          interstitial_xyz.append([None,x,y,z])
        
# Store
    crys['interstitial_xyz'] = interstitial_xyz
      
# Lines
    join_lines = crystal.make_lines(crys, atoms, atoms_xyz, cx, cy, cz, a, b, c)
    cmd_lines = cmd_lines + join_lines
    
# Interstitial lines
    join_lines = crystal.make_interstitial_lines(crys, cx, cy, cz, a, b, c)
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
   
    vertex_large_on, vertex_large_colour, vertex_large_weight, vertex_large_type, vertex_large_f = crystal.line_details(crys['lines_vertex'])
    vertex_small_on, vertex_small_colour, vertex_small_weight, vertex_small_type, vertex_small_f = crystal.line_details(crys['lines_subcells'])
    diag_on, diag_colour, diag_weight, diag_type, diag_f = crystal.line_details(crys['lines_diag'])
  
    cmd_lines = []
  
    cell_diag = numpy.sqrt((a/cx)**2 + (b/cy)**2 + (c/cz)**2)
  
    nl = []
    nl_min = []
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
          
# Neighbours
    for i in range(len(atoms)):
      nl_min.append(None)
      for j in range(len(atoms)):     
        if(i != j):
          rsq = (atoms[i][0] - atoms[j][0])**2 + (atoms[i][1] - atoms[j][1])**2 + (atoms[i][2] - atoms[j][2])**2
          if(rsq > 0.0 and rsq <= rcut_sq):
            r = numpy.sqrt(rsq)  
            if((nl_min[i] == None) or (r <nl_min[i])):
              nl_min[i] = r

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
      cmd_lines = crystal.add_lines(cmd_lines, nl_vertex_large, vertex_large_type, vertex_large_weight, vertex_large_colour)
    if(vertex_small_on):
      cmd_lines = crystal.add_lines(cmd_lines, nl_vertex_small_inner, vertex_small_type, vertex_small_weight, vertex_small_colour)
    if(diag_on):
      cmd_lines = crystal.add_lines(cmd_lines, nl_diagonal_short, diag_type, diag_weight, diag_colour)
    
    return cmd_lines
    
  def make_interstitial_lines(crys, cx, cy, cz, a, b, c):
    cmd_lines = []
    lines = []
    for il in crys['ilines']:
      la = il[0]
      lb = il[1]
      colour = il[2]
      weight = il[3]
      type = il[4]
      
      for i in range(len(crys['interstitial_xyz'])):
        if(crys['interstitial_xyz'][i][0] == la):
          for j in range(len(crys['interstitial_xyz'])):
            if(crys['interstitial_xyz'][j][0] == lb):
              xa = crys['interstitial_xyz'][i][1]
              ya = crys['interstitial_xyz'][i][2]
              za = crys['interstitial_xyz'][i][3]
              xb = crys['interstitial_xyz'][j][1]
              yb = crys['interstitial_xyz'][j][2]
              zb = crys['interstitial_xyz'][j][3]
              if([xa,ya,za,xb,yb,zb] in lines or [xb,yb,zb,xa,ya,za] in lines):
                pass
              else:
                lines.append([xa,ya,za,xb,yb,zb])
                cmd_lines = crystal.add_lines_i(cmd_lines, [xa,ya,za], [xb,yb,zb], type, weight, colour)
     
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
        
  def add_lines(cmd_lines, pairs, type, weight, colour='#000022'):
    for pair in pairs:
      xa = str(pair[3][0])
      ya = str(pair[3][1])
      za = str(pair[3][2])
      xb = str(pair[4][0])
      yb = str(pair[4][1])
      zb = str(pair[4][2])
      join_line = 'line xa=' + str(xa) + ' xb=' + str(xb) + ' ya=' + str(ya) + ' yb=' + str(yb) + ' za=' + str(za) + ' zb=' + str(zb) + ' colour='+colour+' type=' + type + ' line_weight="' + weight + '"'
      cmd_lines.append(join_line)    
    return cmd_lines
    
  def add_lines_i(cmd_lines, a, b, type, weight, colour='#000022'):
    xa = str(a[0])
    ya = str(a[1])
    za = str(a[2])
    xb = str(b[0])
    yb = str(b[1])
    zb = str(b[2])
    join_line = 'line xa=' + str(xa) + ' xb=' + str(xb) + ' ya=' + str(ya) + ' yb=' + str(yb) + ' za=' + str(za) + ' zb=' + str(zb) + ' colour='+colour+' type=' + type + ' line_weight="' + weight + '"'
    cmd_lines.append(join_line)    
    return cmd_lines  
    
  def line_details(details):
    ds = []
    for d in details:
      ds.append(d.strip().lower())
      
    if('none' in ds):
      on = False
      colour = '#FFFFFF' 
      weight = ''
      type = ''
      f = 0.5
    else:
      on = True
      colour = '#000000' 
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
        if(len(d) == 7 and d[0] == '#'):
          colour = d[0:7] 
      for d in ds:
        try:
          f = float(d)
          break
        except:
          pass
    return on, colour, weight, type, f
  
  def read_file(crys):
    if('file' not in crys.keys()):
      return crys
    if(crys['file'] == None):
      return crys
    
    ft = file_type.check(crys['file'][0])
    
    if(ft == 'qe'):
      pw = pwscf_output(crys['file'][0])
      
      crys['type'][0] = 'file'
      crys['file_xyz'] = pw.get_crystal_positions()
      crys['file_xyz'] = crys['file_xyz'] % 1.0
      
      crys['a'][0] = 1.0
      crys['b'][0] = 1.0
      crys['c'][0] = 1.0
      crys['alpha'][0] = 90.0
      crys['beta'][0] = 90.0
      crys['gamma'][0] = 90.0
      
      crys['file_atoms'] = []
      for i in range(len(crys['file_xyz'])):
        crys['file_atoms'].append([crys['file_xyz'][i,0],crys['file_xyz'][i,1],crys['file_xyz'][i,2]])
      
      crys['file_atoms_expanded'] = crystal.expand(crys['file_atoms'], int(crys['cx'][0]), int(crys['cy'][0]), int(crys['cz'][0]))
      
      for i in range(len(crys['file_atoms_expanded'])):
        print((i+1),crys['file_atoms_expanded'][i][:])
#unit = [[0,0,0],[0.5,0.5,0.0],[0.5,0.0,0.5],[0.0,0.5,0.5]]
#return crystal.expand(unit, cx, cy, cz)
  
    return crys
  
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
    
###########################################
#  CLASS pwscf_outpu
###########################################
class pwscf_output:

  def __init__(self, file_in=None):
    self.reset()
    if(file_in != None):
      self.load(file_in)

  def reset(self):
  
    self.z = numpy.zeros((3,3))
    
# Important so store in it's own variable
    self.atom_count = 1    

# Control
    self.data = {
      "ok": False,
      "job_done": False,
      "error": False,
      "type": None,
      "summary": None,
      "mpi_processes": None,
      "threads_per_mpi_process": None,
      
      "scf_settings": None,      
      "crystals": [],
      "results": [],
      
      "initial_positions": None,   
      "total_energy": None,
      "density_full": None,
      "density": None,
      "stress": numpy.zeros((3,3)),
      "stress_sum": None,      
      "cpu_time": None,
      "wall_time": None,   
      "xyz": [],
      "angle": numpy.zeros((3,),)
    }
    
# Defaults
    self.xyz_units = 'evang'
    self.stress_units = 'gpa'

  def scf_settings(self):
    return {
    "bravais_lattice_index": None,
    "alat": None,
    "volume": None,
    "electrons": None, 
    "electrons_up": None, 
    "electrons_down": None, 
    "ecut_wfc": None, 
    "ecut_rho": None, 
    "convergence_threshold": None, 
    "mixing_beta": None, 
    "atomic_species": {},
    }
    
  def scf_crystal(self):
    return {
    "alat": 0.0,
    "cell_parameters": numpy.zeros((3,3)),
    "position_units": None,
    "atomic_labels": [],
    "atomic_positions": numpy.zeros((self.atom_count,3)),    
    "alat_adj": 0.0,
    "cell_parameters_adj": numpy.zeros((3,3)),
    "crystal_positions": numpy.zeros((self.atom_count,3)),
    }

  def scf_results(self):
    return {
    "energy": 0.0,
    "total_force": 0.0,
    "stress": numpy.zeros((3,3)),
    "forces": numpy.zeros((self.atom_count,3)),
    "f_on": False,
    "s_on": False,
    }

#  Load, and use in another program
  def load(self, file_name): 
  
# Load data from file
    data_file = self.load_from_file(file_name)
    self.d = data_file.split("\n") 
  
#print(self.d)
  
# Reset data store
    self.reset()
       
# Load
    self.load_status()
    self.load_type()
    self.load_count()
    self.load_cpuinfo()
    self.load_crystal()
    self.load_scf_settings()
    self.load_results()
    
#print(len(self.data['crystals']))
#print(len(self.data['results']))
    
#self.load_scf('final_scf')
#self.load_results('initial_scf')
#self.load_results('final_scf')
    
  def load_status(self):    
# OK
###################################
    self.data['ok'] = False
    counter = 0
    for line in self.d:
      line = line.strip()
      if(pwscf_output.compare(line, "JOB DONE.")):
        counter = counter + 1
      if(pwscf_output.compare(line, "Exit code:")):
        counter = counter - 1
      if(pwscf_output.compare(line, "convergence NOT achieved")):
        counter = counter - 1
    if(counter == 1):
      self.data['ok'] = True
  
  def load_type(self):
# Calc Type
###################################
    self.data['type'] = "SCF"
    for line in self.d:
      line = line.strip()
      if(line[0:23] == "A final scf calculation"):
        self.data['type'] = "VC-RELAX"
    
  def load_count(self):
    n = 0
    while(n < len(self.d)):
      n, line, line_uc = self.next_line(n, self.d)
      if(pwscf_output.compare(line, "number of atoms/cell      =")):
        count = pwscf_output.extract(line, "=", "", "i")  
        try:
          self.atom_count = int(count)
          return self.atom_count 
        except:
          return 0
          
  def load_cpuinfo(self):
    counter = 0
    n = 0
    while(n < len(self.d)):
      n, line, line_uc = self.next_line(n, self.d)
      if(line != ""):
        counter += 1
        if(counter == 1):
          self.data['summary'] = line
        else:
          if(pwscf_output.compare(line, "Number of MPI processes:")):
            self.data['mpi_processes'] = pwscf_output.extract(line, ":", "", "i") 
          elif(pwscf_output.compare(line, "Threads/MPI process:")):
            self.data['threads_per_mpi_process'] = pwscf_output.extract(line, ":", "", "i") 
   
  def load_scf_settings(self):
    self.data['scf_settings'] = self.scf_settings()  
    
    n = 0
    while(n < len(self.d)):
      n, line, line_uc = self.next_line(n, self.d)
      if(pwscf_output.compare(line, "bravais-lattice index     =")):
        self.data['scf_settings']['bravais_lattice_index'] = pwscf_output.extract(line, "=", "", "i") 
      elif(pwscf_output.compare(line, "lattice parameter (alat)  =")):
        self.data['scf_settings']['alat'] = pwscf_output.extract(line, "=", "a.u.", "f")  
      elif(pwscf_output.compare(line, "unit-cell volume          =")):
        self.data['scf_settings']['volume'] = pwscf_output.extract(line, "=", "(a.u.)^3", "f")     
      elif(pwscf_output.compare(line, "number of atoms/cell      =")):
        self.data['scf_settings']['nat'] = pwscf_output.extract(line, "=", "", "i")  
      elif(pwscf_output.compare(line, "number of atomic types    =")):
        self.data['scf_settings']['types'] = pwscf_output.extract(line, "=", "", "i")  
      elif(pwscf_output.compare(line, "number of electrons       =")):
        str_e = pwscf_output.extract(line, "=", "", "s")
        e, eu, ed = pwscf_output.electron_string(str_e)
        self.data['scf_settings']['electrons'] = e
        self.data['scf_settings']['electrons_up'] = eu
        self.data['scf_settings']['electrons_down'] = ed
      elif(pwscf_output.compare(line, "kinetic-energy cutoff     =")):
        self.data['scf_settings']['ecut_wfc'] = pwscf_output.extract(line, "=", "Ry", "f")  
      elif(pwscf_output.compare(line, "charge density cutoff     =")):
        self.data['scf_settings']['ecut_rho'] = pwscf_output.extract(line, "=", "Ry", "f")  
      elif(pwscf_output.compare(line, "convergence threshold     =")):
        self.data['scf_settings']['convergence_threshold'] = pwscf_output.extract(line, "=", "", "f")  
      elif(pwscf_output.compare(line, "mixing beta               =")):
        self.data['scf_settings']['mixing_beta'] = pwscf_output.extract(line, "=", "", "f")  
      elif(("atomic species" in line) and ("valence" in line) and ("mass" in line) and ("pseudopotential" in line)):
        loop = True
        while(loop):
          n, line, line_uc = self.next_line(n, self.d)
          if(line.strip() == ""):
            loop = False
          else:  
            line = pwscf_output.single_spaces(line).strip()
            line_arr = line.split(" ")
            self.data['scf_settings']['atomic_species'][line_arr[0]] = {}
            self.data['scf_settings']['atomic_species'][line_arr[0]]['valence'] = line_arr[1]
            self.data['scf_settings']['atomic_species'][line_arr[0]]['mass'] = line_arr[2]

# End of file/loop
        n = len(self.d)

###################################
# LOAD CRYSTALS FROM OUTPUT FILE
###################################

  def load_crystal(self):
# Make new list for crystals
    self.data['crystals'] = []
    
# FIRST
    n = 0
    crystal = self.scf_crystal()
    while(n < len(self.d)):
      n, line, line_uc = self.next_line(n, self.d)   
      if(line[0:10] == "celldm(1)="):
        crystal['alat'] = float(line[10:21].strip())
      elif(pwscf_output.compare(line.strip(), "crystal axes:")):
        for j in range(3):              
          n, line, line_uc = self.next_line(n, self.d)
          fields = pwscf_output.extract(line, "= (", ")", "s", " ")
          for i in range(len(fields)):
            crystal['cell_parameters'][j, i] = float(fields[i])
      elif(pwscf_output.compare(line.strip(), "Cartesian axes")):
        n, line, line_uc = self.next_line(n, self.d)
        n, line, line_uc = self.next_line(n, self.d)
        
# Unit
        crystal['position_units'] = "alat"
        
        loop = True 
        k = 0
        while(loop):
          n, line, line_uc = self.next_line(n, self.d)   
          if(line.strip() == ""):
            loop = False
          else:
            line_arr = line.split("tau(")
            label = line_arr[0][-15:].strip()
            crystal['atomic_labels'].append(label)
            
            coords = line_arr[1]
            x = float(coords[9:21])
            y = float(coords[22:33])
            z = float(coords[34:44])
            crystal['atomic_positions'][k, 0] = x
            crystal['atomic_positions'][k, 1] = y
            crystal['atomic_positions'][k, 2] = z 
            
# Increment
            k = k + 1
            
# Add/Save
        self.data['crystals'].append(crystal)
        n = len(self.d)
    
# MIDDLE
    n = 0
    while(n < len(self.d)):
      n, line, line_uc = self.next_line(n, self.d)   
      if(line[0:15] == "CELL_PARAMETERS"):
# Create
        crystal = self.scf_crystal()
        
# Get alat
        line_arr = line.split("=")
        line_arr = line_arr[1].split(")")
        crystal['alat'] = float(line_arr[0].strip())
        
#Cell Parameters
        for j in range(3):              
          n, line, line_uc = self.next_line(n, self.d)
          line = pwscf_output.single_spaces(line)
          fields = line.split(" ")
          for i in range(len(fields)):
            crystal['cell_parameters'][j, i] = float(fields[i])
      elif(line[0:16] == "ATOMIC_POSITIONS"):     
        
# Unit
        crystal['position_units'] = "crystal"
        
# Read Coords
        loop = True 
        k = 0
        while(loop):
          n, line, line_uc = self.next_line(n, self.d)   
          if(line.strip() == ""):
            loop = False
          elif(line.strip() == "End final coordinates"):
            loop = False
          else:
            line = pwscf_output.single_spaces(line)
            line_arr = line.split(" ")
            crystal['atomic_labels'].append(line_arr[0])
            
            crystal['atomic_positions'][k, 0] = float(line_arr[1])
            crystal['atomic_positions'][k, 1] = float(line_arr[2])
            crystal['atomic_positions'][k, 2] = float(line_arr[3]) 
            
# Increment
            k = k + 1
            
# Add/Save
        self.data['crystals'].append(crystal)
    
# END
    n = 0
    crystal = self.scf_crystal()
    d = 0
    while(n < len(self.d)):
      n, line, line_uc = self.next_line(n, self.d)   
      if(line[0:10] == "celldm(1)="):
        d = d + 1
        if(d == 2):
          crystal['alat'] = float(line[10:21].strip())
      elif(d == 2 and pwscf_output.compare(line.strip(), "crystal axes:")):
        for j in range(3):              
          n, line, line_uc = self.next_line(n, self.d)
          fields = pwscf_output.extract(line, "= (", ")", "s", " ")
          for i in range(len(fields)):
            crystal['cell_parameters'][j, i] = float(fields[i])
      elif(d == 2 and pwscf_output.compare(line.strip(), "Cartesian axes")):      
        
# Unit
        crystal['position_units'] = "alat"
        
# Read coords
        n, line, line_uc = self.next_line(n, self.d)
        n, line, line_uc = self.next_line(n, self.d)
        
        loop = True 
        k = 0
        while(loop):
          n, line, line_uc = self.next_line(n, self.d)   
          if(line.strip() == ""):
            loop = False
          else:
            line_arr = line.split("tau(")
            label = line_arr[0][-15:].strip()
            crystal['atomic_labels'].append(label)
            
            coords = line_arr[1]
            x = float(coords[9:21])
            y = float(coords[22:33])
            z = float(coords[34:44])
            crystal['atomic_positions'][k, 0] = x
            crystal['atomic_positions'][k, 1] = y
            crystal['atomic_positions'][k, 2] = z 
            
# Increment
            k = k + 1
            
# Add/Save
        self.data['crystals'].append(crystal)
        n = len(self.d)
    
# Loop through crystals
    for i in range(len(self.data['crystals'])):
# Adjust alat and cell_parameters so celldm(1)=1.0
      factor = 1.0 / self.data['crystals'][i]['cell_parameters'][0, 0]
      
      self.data['crystals'][i]['alat_adj'] = self.data['crystals'][i]['alat'] * self.data['crystals'][i]['cell_parameters'][0, 0]
      self.data['crystals'][i]['cell_parameters_adj'][:, :] = factor * self.data['crystals'][i]['cell_parameters'][:, :]
    
# Make crystal_positions
      if(self.data['crystals'][i]['position_units'] == 'crystal'):
        self.data['crystals'][i]['crystal_positions'][:,:] = self.data['crystals'][i]['atomic_positions'][:,:] 
      elif(self.data['crystals'][i]['position_units'] == 'alat'):  
        minv = numpy.linalg.inv(self.data['crystals'][i]['cell_parameters'][:, :])
        for j in range(len(self.data['crystals'][i]['atomic_positions'])):
          self.data['crystals'][i]['crystal_positions'][j, :] = numpy.matmul(minv[:,:], self.data['crystals'][i]['atomic_positions'][j, :])

  def load_results(self):
  
# Make new list for results
    self.data['results'] = []
    
    n = 0
    while(n < len(self.d)):
      n, line, line_uc = self.next_line(n, self.d)
      
# READ ENERGY
      if(pwscf_output.compare(line, "!    total energy")):
# Create dictionary
        results = self.scf_results()  
        results['energy'] = pwscf_output.extract(line, "=", "Ry", "f") 
        
# READ FORCES
      elif(pwscf_output.compare(line, "Forces acting on atoms")):
        n, line, line_uc = self.next_line(n, self.d)  
        loop = True
        f = 0
        while(loop):
          n, line, line_uc = self.next_line(n, self.d)  
          if(line.strip() == ""):
            loop = False
          else:
            line_arr = line.split("force =")
            fields = pwscf_output.single_spaces(line_arr[1].strip()).split(" ")
            results['forces'][f,0] = float(fields[0])
            results['forces'][f,1] = float(fields[1])
            results['forces'][f,2] = float(fields[2])
            f = f + 1
        if(f>0):
          results['f_on'] = True
        
# READ TOTAL FORCE
      elif(pwscf_output.compare(line, "Total force =")):
        results['total_force'] = pwscf_output.extract(line, "=", "T", "f")
        
# READ STRESS
      elif(pwscf_output.compare(line, "total   stress  (Ry/bohr**3)")):  
        results['s_on'] = True      
        for j in range(3):              
          n, line, line_uc = self.next_line(n, self.d)  
          fields = pwscf_output.extract(line, "", "", "f", " ", True)  
          results['stress'][j,0] = fields[3] 
          results['stress'][j,1] = fields[4] 
          results['stress'][j,2] = fields[5]

#SAVE
        self.data['results'].append(results)

  def aaa():
    
# Load
###################################
    n = 0
    counter = 0
    while(n < len(data)):
      n, line, line_uc = self.next_line(n, data)
      if(line != ""):
        counter += 1
        if(counter == 1):
          self.data['summary'] = line
        else:
          if(pwscf_output.compare(line, "Number of MPI processes:")):
            self.data['mpi_processes'] = pwscf_output.extract(line, ":", "", "i") 
        
          if(pwscf_output.compare(line, "bravais-lattice index     =")):
            self.data['bravais_lattice_index'] = pwscf_output.extract(line, "=", "", "i") 
            
          if(pwscf_output.compare(line, "lattice parameter (alat)  =")):
            self.data['alat'] = pwscf_output.extract(line, "=", "a.u.", "f")  
            
          if(pwscf_output.compare(line, "unit-cell volume          =")):
            self.data['volume'] = pwscf_output.extract(line, "=", "(a.u.)^3", "f")     
            
          if(pwscf_output.compare(line, "number of atoms/cell      =")):
            self.data['nat'] = pwscf_output.extract(line, "=", "", "i")  
            
          if(pwscf_output.compare(line, "number of atomic types    =")):
            self.data['types'] = pwscf_output.extract(line, "=", "", "i")  
            
          if(pwscf_output.compare(line, "number of electrons       =")):
            str_e = pwscf_output.extract(line, "=", "", "s")
            e, eu, ed = pwscf_output.electron_string(str_e)
            self.data['electrons'] = e
            self.data['electrons_up'] = eu
            self.data['electrons_down'] = ed
          
          if(pwscf_output.compare(line, "number of Kohn-Sham states=")):
            self.data['ks_states'] = pwscf_output.extract(line, "=", "", "i")   
            
          if(pwscf_output.compare(line, "kinetic-energy cutoff     =")):
            self.data['ecutwfc'] = pwscf_output.extract(line, "=", "Ry", "f")  
            
          if(pwscf_output.compare(line, "charge density cutoff     =")):
            self.data['ecutrho'] = pwscf_output.extract(line, "=", "Ry", "f")   
        
          if(pwscf_output.compare(line.strip(), "crystal axes:") and pwscf_output.is_zero(self.data['crystal_in'])):            
            for j in range(3):              
              n, line, line_uc = self.next_line(n, data)
              fields = pwscf_output.extract(line, "= (", ")", "s", " ")
              self.data['crystal_in'][j,:] = fields  
              self.data['crystal_calc'][j,:] = fields  
          
          if(pwscf_output.compare(line.strip(), "crystal axes:")):            
            for j in range(3):              
              n, line, line_uc = self.next_line(n, data)
              fields = pwscf_output.extract(line, "= (", ")", "s", " ")
              self.data['crystal_calc'][j,:] = fields            
        
          if(pwscf_output.compare(line, "!    total energy")):
            self.data['total_energy'] = pwscf_output.extract(line, "=", "Ry", "f")
            
          if(pwscf_output.compare(line, "Total force =")):
            self.data['total_force'] = pwscf_output.extract(line, "=", "T", "f")
            
          if(pwscf_output.compare(line, "total   stress  (Ry/bohr**3)")):        
            self.data['stress_sum'] = 0.0
            for j in range(3):              
              n, line, line_uc = self.next_line(n, data)   
              fields = pwscf_output.extract(line, "", "", "f", " ", True)  
              self.data['stress'][j,0] = fields[3] 
              self.data['stress'][j,1] = fields[4] 
              self.data['stress'][j,2] = fields[5]
              self.data['stress_sum'] = self.data['stress_sum'] + abs(fields[0]) + abs(fields[1]) + abs(fields[2])
            
#                  "stress": numpy.zeros((3,3)),
#      "stress_sum": None,
            
          if(pwscf_output.compare(line, "density = ")):
            self.data['density_full'] = pwscf_output.extract(line, "=", "", "s")
            self.data['density'] = pwscf_output.extract(line, "=", "g/cm^3", "f")
          
          if(pwscf_output.compare(line, "PWSCF        :")):
            self.data['cpu_time'] = pwscf_output.extract(line, ":", "CPU", "s")
            
          if(pwscf_output.compare(line, "PWSCF        :")):
            self.data['wall_time'] = pwscf_output.extract(line, "CPU", "WALL", "s")
          
          if(pwscf_output.compare(line, "JOB DONE.")):
            self.data['job_done'] = True
            
          if(pwscf_output.compare(line, "Exit code:")):
            self.data['error'] = True  
             
  def next_line(self, n, data):
    if(n < len(data)):
      line = data[n].strip()
      line_uc = line.upper()
      n = n + 1
      return n, line, line_uc
    else:
      n = n + 1
      return n, None, None
    
  def store(self, store, line, field, n=0):
    l, f = pwscf_output.read_line(line, field)  
    if(l != False):
      self.data[store] = f[n]

#  Run as it's own program
  def run(self):
    self.reset()

    option = ""
    file_name = ""

    if(len(sys.argv) > 1 and sys.argv[1] is not None):
      option = sys.argv[1]

    if(len(sys.argv) > 2 and sys.argv[2] is not None):
      file_name = sys.argv[2]

    if(option.lower().strip() == "" or option.lower().strip() == "interactive"):
      self.menu()
      exit()
    elif(option.lower().strip() == "quiet"):
      print("Quiet")
    else:
      return 0

#################################
# READ/LOAD input file
#################################

  def load_from_file(self, file_name):
# Init variable
    file_data = ""

# Read it in line by line
    fh = open(file_name, "r")
    for file_row in fh:
      file_data = file_data + file_row.strip() + '\n'

    return file_data

#################################
# Get
#################################

  def get_alat(self):
    return self.data['alat']
    
  def get_volume(self):
    return self.data['volume']  
  
  def get_total_energy(self):
    return self.data['total_energy']  
    
  def get_energy_per_atom(self):
    return (float(self.data['total_energy']) / float(self.data['nat']))    
  
  def get_total_force(self):
    return self.data['total_force']  
    
  def get_force_per_atom(self):
    return (float(self.data['total_force']) / float(self.data['nat']))  
  
  def get_density(self):
    return self.data['density']  
    
  def get_cell_parameters(self):
    cp = ['alat', 
          [str(self.data['crystal_calc'][0,0]), str(self.data['crystal_calc'][0,1]), str(self.data['crystal_calc'][0,2])], 
          [str(self.data['crystal_calc'][1,0]), str(self.data['crystal_calc'][1,1]), str(self.data['crystal_calc'][1,2])], 
          [str(self.data['crystal_calc'][2,0]), str(self.data['crystal_calc'][2,1]), str(self.data['crystal_calc'][2,2])]]
    return cp

# Return relaxed unit vector
  def get_cell_array(self):
    return self.data['crystal_calc']

# return alat and normalised unit vector
  def get_norm_relaxed(self):
    alat = self.data['alat']    
    cp = numpy.copy(self.data['crystal_calc'])
    f = cp[0,0]
    alat = alat * f
    cp = cp / f
    return alat, cp

# Get stress
  def get_stress(self):
    return self.data['stress']
    
  def get_stress_sum(self):
    return self.data['stress_sum']
  
  def get_job_done(self):
    return self.data['job_done']

  def get_ok(self):
    return self.data['ok']
    
  def get_crystal_positions(self, i=0):
    return self.data['crystals'][i]['crystal_positions']

#################################
# Interactive
#################################

  def menu(self):
    while(True):
      choice = self.print_menu().upper()
      print(choice)
      if(choice == "X"):
        exit()
      elif(choice == "1"):
        self.i_load()
      elif(choice == "2"):
        self.i_display()

  def print_menu(self):
    pwscf_output.header("Menu")
    print("1. Load File")
    print("2. Display File")
    print("X. Exit")
    return input("Choice: ")

  def i_load(self):
    pwscf_output.header("Load Output File")
    file_name = input("Enter file name: ")
    self.load(file_name)
    print("File loaded.")
    input()

  def i_display(self):
    pwscf_output.header("Display File")
    self.output_details()
    input()

  def output_details(self):
    print("Output")
    print("=======================================================================")
    for key in sorted(self.data.keys()):
      value = self.data[key]
      print(key, ":  ", value)
    print("=======================================================================")
    print()
    
  def xyz_evang(self):
    self.xyz_units = 'ev/ang'
    self.stress_units = 'gpa'

  def xyz_stress_gpa(self):
    self.stress_units = 'gpa'

  def make_xyz(self, option=None):
    self.xyz = []
    if(option == None):
      for rn in range(len(self.data['results'])):
        option = rn + 1
    elif(option == -1):
      option = len(self.data['results'])
    else:
      option = (option - 1) % len(self.data['results']) + 1
    self.make_xyz_inner(option)
    return self.xyz
    
  def make_xyz_inner(self, option):
    if(len(self.data['results'])==0):
      return False
    if(len(self.data['crystals'])==0):
      return False  
   
    rn = (option - 1) % len(self.data['results'])
    cn = rn
    if(rn == len(self.data['results']) - 1):
      cn = len(self.data['crystals']) - 1
      
    crystal = self.data['crystals'][cn]
    result = self.data['results'][rn]
    settings = self.data['scf_settings']
    species = settings['atomic_species']
    
# Add new list and set counter n
    self.xyz.append([])
    n = len(self.xyz) - 1
    
# Add data
    self.xyz[n].append("#ALAT " + str(crystal['alat_adj']))
    self.xyz[n].append("#X " + str(crystal['cell_parameters_adj'][0][0]) + " " + str(crystal['cell_parameters_adj'][0][1]) + " " + str(crystal['cell_parameters_adj'][0][2]))
    self.xyz[n].append("#Y " + str(crystal['cell_parameters_adj'][1][0]) + " " + str(crystal['cell_parameters_adj'][1][1]) + " " + str(crystal['cell_parameters_adj'][1][2]))
    self.xyz[n].append("#Z " + str(crystal['cell_parameters_adj'][2][0]) + " " + str(crystal['cell_parameters_adj'][2][1]) + " " + str(crystal['cell_parameters_adj'][2][2]))
    
# Just use 1 1 1
    self.xyz[n].append("#C 2 2 2")
    self.xyz[n].append("#RCUT 6.5")
    self.xyz[n].append("#L_UNITS bohr")
    self.xyz[n].append("#E_UNITS ry")
    self.xyz[n].append("#F_UNITS ry/bohr")
    self.xyz[n].append("#S_UNITS kbar")
    
    self.xyz[n].append("#E " + str(result['energy']))
    
    if(result['s_on']):
      self.xyz[n].append("#SX " + str(result['stress'][0,0]) + " " +  str(result['stress'][0,1]) + " " + str(result['stress'][0,2]))
      self.xyz[n].append("#SY " + str(result['stress'][1,0]) + " " +  str(result['stress'][1,1]) + " " + str(result['stress'][1,2]))
      self.xyz[n].append("#SZ " + str(result['stress'][2,0]) + " " +  str(result['stress'][2,1]) + " " + str(result['stress'][2,2]))
      
    for label in species.keys():
      self.xyz[n].append("#M " + label + " " + str(species[label]['mass']))
    
    for i in range(self.atom_count):
      line = crystal['atomic_labels'][i]
      line = line + " " + str(crystal['crystal_positions'][i,0]) + " " + str(crystal['crystal_positions'][i,1]) + " " + str(crystal['crystal_positions'][i,2])      
      if(result['f_on']):   
        line = line + " " + str(result['forces'][i,0]) + " " + str(result['forces'][i,1]) + " " + str(result['forces'][i,2])
#"s_on": False,
      self.xyz[n].append(line)
      
# Return
    return self.xyz[n]
    
  def cell_angles(self):  
    self.data['angle'][0] = vec_angle(self.data['crystal_calc'][0,:], self.data['crystal_calc'][1,:])
    self.data['angle'][1] = vec_angle(self.data['crystal_calc'][0,:], self.data['crystal_calc'][2,:])
    self.data['angle'][2] = vec_angle(self.data['crystal_calc'][1,:], self.data['crystal_calc'][2,:])
  
#################################
# Static Methods
#################################

  @staticmethod
  def remove_spaces(input_string):
    return input_string.replace(" ", "")
    
  @staticmethod
  def extract(input_string, start=None, end=None, type=None, split=None, trim=False):
    if(start == ""):
      start = None
    if(end == ""):
      end = None
    if(trim):
      input_string = input_string.strip()
    
# Start/End
    start_n = None
    end_n = None
      
    if(start == None and end == None):   
      start_n = 0
      end_n = len(input_string)
    elif(start == None and end != None):  
      end_l = len(end)   
      start_n = 0
      for n in range(len(input_string)):
        if(input_string[n:n+end_l] == end[0:end_l]):
          end_n = n
          break
    elif(start != None and end == None):  
      start_l = len(start)
      end_n = len(input_string)
      for n in range(len(input_string)):
        if(input_string[n:n+start_l] == start[0:start_l]):
          start_n = n + start_l
    else:  
      start_l = len(start)
      end_l = len(end)  
    
      for n in range(len(input_string)):
        if(input_string[n:n+start_l] == start[0:start_l]):
          start_n = n + start_l
        if(start_n != None and input_string[n:n+end_l] == end[0:end_l]):
          end_n = n
          break
        
# Read
    result = input_string[start_n:end_n].strip()       

# Split
    if(split != None):
      if(split == " "):
#result = re.sub(r'\s\s+', ' ', result)
        result = pwscf_output.single_spaces(result)
      result = result.split(split)
      for i in range(len(result)):
        if(type.lower() == "f"):
          result[i] = float(result[i])
        elif(type.lower() == "i"):
          result[i] = int(result[i])
        
    else:  
      if(type.lower() == "f"):
        result = float(result)
      elif(type.lower() == "i"):
        result = int(result)
        
# Return
    return result
      
  @staticmethod
  def compare(line, field):
    line = line.strip()
    line = line.upper() 
    
    field = field.strip()
    field = field.upper()
    
    f_len = len(field)
    if(len(line) >= f_len and line[0:f_len] == field[0:f_len]):
      return True
    return False
    
  @staticmethod
  def read_line(line, field):
    line = line.strip()
#line = re.sub(r'\s\s+', ' ', line)
#line = re.sub(r'\s=\s', '=', line)
    line = pwscf_output.clean(line)
    line_uc = line.upper() 
    
    field = field.strip()
#field = re.sub(r'\s\s+', ' ', field)
#field = re.sub(r'\s=\s', '=', field)
    field = pwscf_output.clean(field)
    field = field.upper()
    
    f_len = len(field)
    if(len(line_uc) >= f_len and line_uc[0:f_len] == field[0:f_len]):
      output = line[f_len:].strip()
      fields = output.split(" ")
      return output, fields      
    return False, False
    
  @staticmethod
  def fields(input_string):
    input_string = input_string.strip()
    output_string = ""
    last = None
    for character in input_string:
      if(character != " " or (character == " " and last != " ")):
        output_string += character
    return output_string.split(" ")
    
  @staticmethod
  def check_keyword(line, keyword):
    if(line.upper()[0:len(keyword)] == keyword.upper()):
      return True
    return False

  @staticmethod
  def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

  @staticmethod
  def header(sub_title=""):
    pwscf_output.clear_screen()
    print("==========================================================")
    print("                    PWscf Input Editor                    ")
    print("==========================================================")
    print()
    print(sub_title)
    print()
    print()
    print()

  @staticmethod
  def process_keyword(str_in):
    str_in = str_in.lower().strip()
    str_in = pwscf_output.remove_spaces(str_in)
    id = None
    keyword = ""
    flag = 0
    for character in str_in:
      if(character == "("):
        id = ""
        flag = 1
      elif(character == ")"):
        flag = 2
      elif(flag == 0):
        keyword += character
      elif(flag == 1):
        id = id + character
    if(id != None):
      try:
        id = int(id)
      except:
        id = None
    return keyword, id  

  @staticmethod
  def add_keyword(keywords, keyword, id, value):
    if(id == None):
      added = False
      for i in range(len(keywords)):
        if(keywords[i][0] == keyword):
          added = True
          keywords[i][1] = keyword
      if(added == False):
        keywords.append([keyword, value])
    else:   
      n = None
      for i in range(len(keywords)):
        if(keywords[i][0] == keyword):
          n = i
          break
      if(n == None):    
        keywords.append([keyword,[None]])
        n = len(keywords) - 1
        
      while(len(keywords[n][1]) < id):
        keywords[n][1].append(None)

      keywords[n][1][id-1] = value  

  @staticmethod
  def make_line(key, value):
    output = ""
    if(value != None):
       if(isinstance(value, (list,))):
         for i in range(len(value)):
           if(value[i] != None):
             output += key + "(" + str(i+1) + ") = " + value[i] + ", \n"                
       else:
         output += key + " = " + value + ", \n"   
    return output    

  @staticmethod
  def coord_format(float_in):
    pad = "              "
    value = str(round(float_in, 6)).strip()
    return value
    
  @staticmethod
  def label_format(label):  
    pad = "              "
    label = label.strip()
    return label
    
  @staticmethod
  def is_zero(arr):
    for i in range(arr.shape[0]):
      for j in range(arr.shape[1]):
        if(arr[i, j] != 0.0):
          return False
    return True
    
  @staticmethod
  def clean(str_in):  
    str_out = ""
    l = len(str_in)
    for i in range(l):
# Last, Next, This
      if(i == 0):
        last = None
      else:
        last = str_in[i-1]
      if(i < (l-1)):
        next = str_in[i+1]
      else:  
        next = None
      char = str_in[i]
    
# Check
      ok = True
      if(last == " " and char == " "):
        ok = False
      elif(last == "\n" and char == "\n"):
        ok = False
      elif(last == "\n" and char == " "):
        ok = False
      elif(char == " " and next == "\n"):
        ok = False
      elif(last == "=" and char == " "):
        ok = False
      elif(char == " " and next == "="):
        ok = False
        
# Add to string
      if(ok):
        str_out += char
    return str_out    
    
  @staticmethod
  def electron_string(str_in):
    arr = str_in.split("(up:")
    e = arr[0]
    if(len(arr) == 1):
      return e.strip(), None, None
    if(len(arr)==2):
      arr_b = arr[1].split(", down:")
      eu = arr_b[0]
      arr_c = arr_b[1].split(")")
      ed = arr_c[0]
      return e.strip(), eu.strip(), ed.strip()
  
    print("TEST")
    return "","",""
    
  @staticmethod
  def single_spaces(str_in):
    str_out = ""
    last = None
    for char in str_in:
      if(char != " " or (char == " " and last != " ")):
        str_out = str_out + char
      last = char
    return str_out
    
####################################
  
# Angle between two vectors
  @staticmethod
  def vec_angle(a, b):
    return numpy.acos(numpy.dot(a,b)/numpy.cross(a,b))
  
###########################################
#  CLASS file_typ
###########################################
class file_type:

  @staticmethod
  def check(file_path):
    content = std.file_to_list(file_path)
    
# Check if standard file
    count = 0
    for line in content:
      fields = line.split(" ")
      if(fields[0].upper() == "#ALAT"):
        count = count + 1
      if(fields[0].upper() == "#X"):
        count = count + 1
      if(fields[0].upper() == "#Y"):
        count = count + 1
      if(fields[0].upper() == "#Z"):
        count = count + 1
    if(count >= 4):
      return 'std'
  
# Check if pwscf/qe file
    count = 0
    for line in content:
      if(line.strip()[0:13] == "Program PWSCF"):
        count = count + 1
      if(line.strip()[0:27] == "bravais-lattice index     ="):
        count = count + 1
      if(line.strip()[0:27] == "kinetic-energy cutoff     ="):
        count = count + 1
      if(line.strip()[0:27] == "mixing beta               ="):
        count = count + 1
      if(line.strip()[0:27] == "Exchange-correlation      ="):
        count = count + 1
      if(line.strip()[0:9] == "JOB DONE."):
        count = count + 1
    if(count >= 4):
      return 'qe'   
           
###########################################
#  CLASS st
###########################################
class std:

  @staticmethod
  def file_to_list(file_name, clean=False):
# Init variable
    file_data = []
# Read it in line by line
    fh = open(file_name, "r")
    for line in fh:
      if(clean):
        line = line.strip()
        if(line != ""):
          file_data.append(line)          
      else:
        file_data.append(line[0:-1])
# Return
    return file_data
    
  @staticmethod
  def split_fields(line, sep=" "):
    out = line.split(sep)
    key = out[0]
    value = out[1]
    value_out = ''    
    indata = False
    for char in value:
      if(indata and char != '"'):
        value_out = value_out + char
      elif(indata and char == '"'):
        indata = False
      elif(not indata and char == '"'):
        indata = True
    return key, value_out
    
  @staticmethod
  def one_space(line, sep=" "):
    out = ''   
    indata = 0
    last_char = None
    for char in line:
      if(indata == 1 and char != "'" and last_char != "\\"):
        out = out + char
      elif(indata == 1 and char == "'" and last_char != "\\"):
        out = out + char
        indata = 0
      elif(indata == 2 and char != '"' and last_char != "\\"):
        out = out + char
      elif(indata == 2 and char == '"' and last_char != "\\"):
        out = out + char
        indata = 0
      elif(indata == 0 and not (char == " " and last_char == " ")):
        out = out + char
    return out   
    
  @staticmethod
  def to_fields(line, sep=" "):
    out = []
    temp = ''
    indata = 0
    last_char = None
    for char in line:
      if(indata == 1 and char != "'" and last_char != "\\"):
        temp = temp + char
      elif(indata == 1 and char == "'" and last_char != "\\"):
        temp = temp + char
        indata = 0
      elif(indata == 2 and char != '"' and last_char != "\\"):
        temp = temp + char
      elif(indata == 2 and char == '"' and last_char != "\\"):
        temp = temp + char
        indata = 0
      elif(indata == 0 and not (char == sep and last_char == sep)):
        if(char == sep):
          temp = temp.strip()
          if(temp != ""):
            out.append(temp)
            temp = ''
        else:
          temp = temp + char
    
    temp = temp.strip()
    if(temp != ""):
      out.append(temp)      
    return out    
    
  @staticmethod
  def make_dir(dir):
    if(not os.path.exists(dir)):
      os.mkdir(dir) 
    
  @staticmethod
  def remove_comments(content):
    data = ''
    i = 0
    for line in content:
      if(i > 0):
        data += '\n'
      data += line
      i = i + 1
    out = ''
    indata = 0
    incomment = 0
    for i in range(len(data)):
# Get char and next char
      char = data[i]
      next = None
      prev = None
      if(i < len(data)-1):
        next = data[i + 1]
      if(i > 0):
        prev = data[i - 1]
# If in '  '
      if(indata == 1 and char != "'" and last_char != "\\"):
        out = out + char
      elif(indata == 1 and char == "'" and last_char != "\\"):
        out = out + char
        indata = 0
# If in "  "
      elif(indata == 2 and char != '"' and last_char != "\\"):
        out = out + char
      elif(indata == 2 and char == '"' and last_char != "\\"):
        out = out + char
        indata = 0
      elif(indata == 0):
        if(incomment == 0 and char == "/" and next == "/"):
          incomment = 1
        elif(incomment == 1 and char == "\n"):
          incomment = 0
        if(incomment == 0 and char == "!"):
          incomment = 2
        elif(incomment == 2 and char == "\n"):
          incomment = 0
        if(incomment == 0 and char == "/" and next == "*"):
          incomment = 3
        elif(incomment == 3 and prev == "*" and char == "/"):
          incomment = 0
        elif(incomment == 0):
          out = out + char  
    return out.split("\n")    
    
# Remove comments from a block of data/text
  @staticmethod
  def remove_comments_data(data):
    out = ""
    n = 0
    inquotes = 0
    incomment = 0
    while n < len(data):
# Get char and next char
      char = data[n]
      next = None
      prev = None
      if(n < len(data)-1):
        next = data[n + 1]
      if(n > 0):
        prev = data[n - 1]
        
# If in '  '
      if(inquotes == 1 and char != "'" and last_char != "\\"):
        out = out + char
      elif(inquotes == 1 and char == "'" and last_char != "\\"):
        out = out + char
        inquotes = 0
# If in "  "
      elif(inquotes == 2 and char != '"' and last_char != "\\"):
        out = out + char
      elif(inquotes == 2 and char == '"' and last_char != "\\"):
        out = out + char
        inquotes = 0
# If not inside quotes
      elif(inquotes == 0):
# Comment on a line
        if(incomment == 0 and char == "/" and next == "/"):
          incomment = 1
        elif(incomment == 0 and char == "!"):
          incomment = 1
        elif(incomment == 0 and char == "#"):
          incomment = 1    
# Comment on line close
        elif(incomment == 1 and char == "\n"):
          incomment = 0
# Comment block
        elif(incomment == 0 and char == "/" and next == "*"):
          incomment = 3
        elif(incomment == 3 and prev == "*" and char == "/"):
          incomment = 0
        elif(incomment == 0):
          out = out + char  
# Increment counter
      n = n + 1
    return out        

# Single spaces, tabs to spaces
  @staticmethod
  def prep_data(content):
    out = []
    for line in content:
      line_new = std.prep_data_line(line)
      if(line_new != ''):
        out.append(line_new)
    return out  
      
  @staticmethod
  def prep_data_line(line): 
    temp = ''
    indata = 0
    last_char = None
    for char in line:
      if(char == '\t'):
        char = ' '
      if(indata == 1 and char != "'" and last_char != "\\"):
        temp = temp + char
      elif(indata == 1 and char == "'" and last_char != "\\"):
        temp = temp + char
        indata = 0
      elif(indata == 2 and char != '"' and last_char != "\\"):
        temp = temp + char
      elif(indata == 2 and char == '"' and last_char != "\\"):
        temp = temp + char
        indata = 0
      elif(indata == 0 and not (char == ' ' and last_char == ' ')):
        temp = temp + char       
      last_char = char  
    return temp.strip()    
    
  @staticmethod
  def remove_quotes(inp): 
    if(isinstance(inp, list)):    
      for i in range(len(inp)):
        inp[i] = std.remove_quotes(inp[i])        
      return inp
    else:
      inp = inp.strip()
      if(inp[0] == '"' and inp[-1] == '"'):
        return inp[1:-1]
      if(inp[0] == "'" and inp[-1] == "'"):
        return inp[1:-1]
      return inp
      
  @staticmethod
  def config_file_to_list(file_name):
# Init variable
    file_data = []
# Read it in line by line
    fh = open(file_name, "r")
    for line in fh:
      if(line.strip() != ""):
        line = line.strip()
        line = std.remove_comments(line)
        line = std.prep_data_line(line)
        fields = std.to_fields(line)
        file_data.append(fields)         
# Return
    file_data = std.remove_quotes(file_data)
    return file_data
    
  @staticmethod
  def get_dir(file_path):
    directory = ''
    read = False
    for i in range(len(file_path)):
      if(read):
        directory = file_path[-1-i] + directory
      if(file_path[-1-i] == "/"):
        read = True
    return directory
  
  @staticmethod
  def read_csv(filename):
    data = []
    if(os.path.isfile(filename)):
# Read from file into memory
      fh = open(filename, 'r')
      file_data = ""
      for line in fh:
        file_data = file_data + line
      fh.close()
# Remove comments
      file_data = std.remove_comments_data(file_data)
# Read Data
      lines = file_data.split("\n")
      for line in lines:
        line = line.strip()
        if(line != ""):
          data.append(line.split(","))  
    return data
    
  def option(input):
    input = input.strip().upper()
    if(input[0:1] == "Y"):
      return True
    elif(input[0:2] == "ON"):
      return True
    elif(input[0:1] == "T"):
      return True
    else:
      return False

###########################################
#  CLASS lin
###########################################
class line:

  def read_details(details):
    ds = []
    for d in details:
      ds.append(d.strip().lower())
      
    line = {
            'on': False,
            'colour': '#FFFFFF',
            'weight': 'thin',
            'type': 'solid',
            'f': 0.5,
           }
      
    if(not ('none' in ds or 'false' in ds)):
      line['on'] = True
      line['colour'] = '#000000' 
      
# Look for weight
      if('thin' in ds):
        line['weight'] = 'thin'
      elif('very thin' in ds):
        line['weight'] = 'very thin'
      elif('thick' in ds):
        line['weight'] = 'thick'
      elif('very thick' in ds):
        line['weight'] = 'very thick'
      elif('ultra thick' in ds):
        line['weight'] = 'ultra thick'
        
# Look for type
      if('solid' in ds):
        line['type'] = 'solid'
      elif('dashed' in ds):
        line['type'] = 'dashed'
      elif('dotted' in ds):
        line['type'] = 'dotted' 
        
# Look for colour
      for d in ds:
        if(len(d) == 7 and d[0] == '#'):
          line['colour'] = d[0:7] 
          
# Any floats
      for d in ds:
        try:
          line['f'] = float(d)
          break
        except:
          pass
    return line

###########################################
#  CLASS gri
###########################################
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

###########################################
###########################################
#  MAIN
###########################################
###########################################

# Run
tc = tikzcrystal()

tc.main()

