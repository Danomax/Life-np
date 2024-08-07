import re

def life_iterate(Z):
  '''
  Conway's Game of Life Iteration (Z=0s,1s matrix)
  '''
  # Count neighbours
  N = (Z[0:-2,0:-2] + Z[0:-2,1:-1] + Z[0:-2,2: ] +
       Z[1:-1,0:-2]                + Z[1:-1,2: ] +
       Z[2:  ,0:-2] + Z[2:  ,1:-1] + Z[2:  ,2: ])
  # Apply rules
  birth = (N==3) & (Z[1:-1,1:-1]==0)
  survive = ((N==2) | (N==3)) & (Z[1:-1,1:-1]==1)
  Z[...] = 0
  Z[1:-1,1:-1][birth | survive] = 1
  return Z

def rule_iterate(Z, rule, neighborhood = 'Moore'):
  '''
  Cellular Automata Iteration (Z=0s,1s matrix)
  rule = b[number of births]/s[number of survives]
  neighborhood = Moore for now
  '''
  # Count neighbours
  if neighborhood == 'Moore':
      N = (Z[0:-2,0:-2] + Z[0:-2,1:-1] + Z[0:-2,2: ] +
           Z[1:-1,0:-2]                + Z[1:-1,2: ] +
           Z[2:  ,0:-2] + Z[2:  ,1:-1] + Z[2:  ,2: ])
  b_match = re.search('[bB][0-9]+',rule)
  s_match = re.search('[sS][0-9]+',rule)
  r_split = rule.split('/')
  b_list = re.findall('[0-9]',r_split[0])
  s_list = re.findall('[0-9]',r_split[1])
  # Apply rules
  birth = (N==int(b_list[0])) & (Z[1:-1,1:-1]==0)
  survive = ((N==int(s_list[0])) | (N==int(s_list[1])) ) & (Z[1:-1,1:-1]==1)
  Z[...] = 0
  Z[1:-1,1:-1][birth | survive] = 1
  return Z