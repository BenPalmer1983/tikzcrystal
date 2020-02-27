################################################################
#    Processing PWscf input file
#
#
#
#
################################################################


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
    self.latex = ''
    self.latex_colour = ''
    self.latex_background = ''
    self.latex_content = ''
    self.data = []
    self.colours_set = []
    self.space = {'a':5, 'b':5, 'c':5, 'alpha':90, 'beta':90, 'gamma':90, 'gx': 4, 'gy': 4, 'gz': 4, 'zdepth': 1.0, 'zscale': 0.8,}
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
  
    alpha = self.space['alpha']
    beta = self.space['beta']
    gamma = self.space['gamma']
  
    return self.transform(x, y, z, a, b, c, alpha, beta, gamma, round_p)

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
        if(len(fb) == 1):
          dict[f[0].lower()] = [f[1]]
        elif(len(fb) > 1):
          dict[f[0].lower()] = fb
    
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
    
###########################################
###########################################
#  MAIN
###########################################
###########################################

# Run
tc = tikzcrystal()

tc.main()

