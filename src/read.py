######################################################
#  Ben Palmer University of Birmingham 2020
#  Free to use
######################################################

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