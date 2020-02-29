######################################################
#  Ben Palmer University of Birmingham 2020
#  Free to use
######################################################

import numpy
from pwscf_output import pwscf_output
from file_type import file_type

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