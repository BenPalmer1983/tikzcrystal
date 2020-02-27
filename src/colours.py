import numpy

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
  