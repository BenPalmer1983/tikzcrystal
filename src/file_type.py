import sys
import os
import numpy
sys.path.append("py")
from std import std

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
           
    
    
    
    
    
