import numpy as np

direction_dic = {
  'down':    { 'rpos':( 0, -1, 0), 'data':0 },
  'up':      { 'rpos':( 0,  1, 0), 'data':1 },
  'left':    { 'rpos':( 0, 0, -1), 'data':2 },
  'right':   { 'rpos':( 0, 0,  1), 'data':3 },
  'back':    { 'rpos':(-1, 0,  0), 'data':4 },
  'forward': { 'rpos':( 1, 0,  0), 'data':5 },
}
dir_rpos_dic = {}
for k,v in direction_dic.items():
  dir_rpos_dic[v['rpos']] = v['data']

def getCubePosFunction(x=0,y=4,z=0, dx=32,dy=128,dz=32):
  S = dx * dz
  V = dx*dy*dz
  def posFunction( index ):
    if 0 <= index < V:
      h = index // S
      if h % 2 == 0:
        w = index % S // dx
        if w % 2 == 0 :
          l = index % S % dx
        else:
          l = (dx-1) - index % S % dx
      else:
        w = (dz-1) - index % S // dx
        if w % 2 != 0 :
          l = index % S % dx
        else:
          l = (dx-1) - index % S % dx

      pos = ( x+l, y+h, z+w )
      return pos
    else:
      print( f'[Error]: index:{index} large than V:{V}' )
      exit(-1)
  
  return posFunction

class PosParam:
  def __init__(self, pos, data):
    self.pos = pos
    self.data= data

class Sequence2CmdBlock:
  def __init__(self, func=None):
    self.curPosIndex = 0
    self.posFunction = func
    self.appendCmdNum= 2
  def setCubePosFunction(self, x=0,y=4,z=0, dx=32,dy=128,dz=32):
    self.setPosFunction( getCubePosFunction(x,y,z, dx,dy,dz) )
  def setPosFunction(self, func):
    self.posFunction = func
  def calDirection(self, pos1, pos2):
    p1, p2 = np.array(pos1), np.array(pos2)
    direct = p2-p1
    length = np.linalg.norm( direct )
    if length != 1.0:
      return None, None
    else:
      rpos = tuple( direct.tolist() )
      return rpos, dir_rpos_dic[rpos]

  def getNPos(self, N, maxTryTime=16):
    index      = self.curPosIndex
    posList    = []
    tryTime    = 0
    while len(posList) < N:
      pos = self.posFunction( index )
      if len(posList) == 0:
        posList.append( PosParam( pos, None ) )
      else:
        rpos, data = self.calDirection( posList[-1].pos, pos )
        if data != None:
          posList[-1].data = data
          posList.append( PosParam( pos, None ) )
        else:
          tryTime += 1
          if tryTime >= maxTryTime:
            print(f'[Error]: Try Time is large than {maxTryTime} in getNPos')
            return 
          else:
            posList = []
            index -= 1

      index += 1

    # 最后一个计算方向
    if N > 0:
      rpos, data = self.calDirection( posList[-1].pos, self.posFunction( index ) )
      if data:
        posList[-1].data = data
      else:
        if len(posList) > 1:
          posList[-1].data = posList[-2].data
        else:
          posList[-1].data = 0

    self.curPosIndex = index

    return posList

  def testCmdBlockCmds( self, cmds, appendCmdNum ):
    N = len( cmds ) + appendCmdNum
    posList = self.getNPos( N )
    return posList, cmds

  def getCmdBlockBySequence( self, sequence, sequenceLen=None ):
    positionsAndCmdsList = []
    res = []
    if sequenceLen == None:
      sequenceLen = len(sequence)

    for i, cmds in enumerate(sequence):
      if i != sequenceLen-1:
        appendCmdNum = self.appendCmdNum  
      else: 
        appendCmdNum = 0
      posList, cmds = self.testCmdBlockCmds( cmds, appendCmdNum )
      positionsAndCmdsList.append( ( posList, cmds ) )

    for i, positionsAndCmds in enumerate(positionsAndCmdsList):
      posList,cmds = positionsAndCmds
      if i != sequenceLen-1:
        nextPos = positionsAndCmdsList[i+1][0][0].pos
        x,y,z   = nextPos
        appendCmds = []
        appendCmds.append(f'blockdata {x} {y} {z} {{auto:1}}')
        appendCmds.append(f'blockdata {x} {y} {z} {{auto:0}}')
        cmds = appendCmds + cmds

      curRes = []
      for j in range(len(cmds)):
        cmd,pos,data = cmds[j], posList[j].pos, posList[j].data
        x, y, z      = pos
        block        = 'command_block' if j == 0 else 'chain_command_block'
        auto         =              0  if j == 0 else  1      
        curRes.append( f'setblock {x} {y} {z} {block} {data} destroy {{Command:"{cmd}",auto:{auto},TrackOutput:0}}' )

      res.append( ( i, '\n'.join( curRes ) ) )

    return res