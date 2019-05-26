import os
import json
import subprocess

def noteParticle(x,y,z):
  return f'particle note {x} {y} {z} .1 0 .1 1 1 force @a'

class SetBlock:
  def __init__(self, x, y, z, block, data=0, replace=''):
    self.x, self.y, self.z, self.block, self.data, self.replace = x, y, z, block, data, replace
  def toCmd(self):
    if self.replace == '':
      return f'setblock {self.x} {self.y} {self.z} {self.block} {self.data} replace'
    else:
      return f'fill {self.x} {self.y} {self.z} {self.x} {self.y} {self.z} {self.block} {self.data} replace {self.replace}'

def setblock(x, y, z, block, data=0, replace=''):
  return SetBlock(x, y, z, block, data, replace).toCmd()

class Summon:
  def __init__(self, x, y, z, entity, tag=''):
    self.x, self.y, self.z, self.entity, self.tag = x, y, z, entity, tag
  def toCmd(self):
    _tag = ''
    if self.tag != None and self.tag != '':
      _tag = f' {{{self.tag}}}'
    return f'summon {self.entity} {self.x} {self.y} {self.z} {_tag}'

class TellRawNode:
  def __init__(self, text, color='white', bold=False, fixChar=True):
    self.data = {
      "text" : text.replace('"','\\"').replace('\\','\\\\') if fixChar else text,
      "color": color,
      "bold" : bold
    }
  def toJson(self):
    return json.dumps(self.data)

class TellRaw:
  def __init__(self, entity):
    self.entity = entity
    self.nodes  = []
  def addNode(self, trNode):
    self.nodes.append(trNode)
  def toCmd(self):
    if len(self.nodes) == 0:
      return ''
    else:
      nodeJson = '[' +  ','.join([node.toJson() for node in self.nodes]) + ']'
      return f'tellraw {self.entity} {nodeJson}'

class Parabola3:
  def __init__(self, x,y,z, X,Y,Z, tick, g=-9.8, tickrate=20):
    self.x,self.y,self.z, self.X,self.Y,self.Z, self.tick, self.g, self.tickrate = x,y,z, X,Y,Z, tick, g, tickrate
    dy      = Y-y
    t       = tick/tickrate
    self.v0 = ( dy - 0.5*g*(t**2) ) / t
  def getDy(self, tick):
    t = tick/self.tickrate
    return self.v0*t + 0.5*self.g*(t**2)
  def getDx(self, tick):
    return (self.X-self.x) * (tick/self.tick)
  def getDz(self, tick):
    return (self.Z-self.z) * (tick/self.tick)
  def toMotion(self):
    return ((self.X-self.x)/(self.tick/self.tickrate),self.v0,(self.Z-self.z)/(self.tick/self.tickrate))
  def toPosList(self):
    posList = []
    for tick in range(0, self.tick+1):
      posList.append((self.x+self.getDx(tick), self.y+self.getDy(tick), self.z+self.getDz(tick)))
    return posList

class TpFallingEntity:
  def __init__(self, entity, name, x,y,z, x2,y2,z2, tick, g=-9.8, tickrate=20):
    self.entity, self.name = entity, name
    self.x, self.y, self.z, self.x2,self.y2,self.z2, self.tick, self.tickrate, self.g = x,y,z, x2,y2,z2, tick, tickrate, g
  def toCmd(self, kill=False):
    motion = Parabola3(self.x,self.y,self.z, self.x2,self.y2,self.z2, tick=self.tick, tickrate=self.tickrate, g=self.g).toMotion()
    vx,vy,vz = motion
    print(motion)
    return f'summon {self.entity} {self.x} {self.y} {self.z} {{CustomName:"{self.name}",Motion:[{vx},{vy},{vz}],DropItem:0b}}'
  def toCmds(self, kill=False):
    cmds    = []
    posList = Parabola3(self.x,self.y,self.z, self.x2,self.y2,self.z2, tick=self.tick, tickrate=self.tickrate, g=self.g).toPosList()
    firstOne= True
    for pos in posList:
      x,y,z = pos
      _time = 600 - self.tick 
      if firstOne:
        firstOne = False
        cmd = f'summon {self.entity} {x} {y} {z} {{CustomName:"{self.name}",NoGravity:1b,DropItem:0b}}'
        cmds.append(cmd)
      else:
        cmd = f'tp @e[name={self.name}] {x} {y} {z}'
        cmds.append(cmd)

    if kill:
      cmds.append(f'kill @e[name={self.name}]')
    return cmds


class Log:
  def __init__(self, msg):
    self.tellRaw = TellRaw('@a')
    self.tellRaw.addNode(TellRawNode(msg))
  def toCmd(self):
    return self.tellRaw.toCmd()

def log(msg):
  return Log(msg).toCmd()

def pngTellRaw(CompleteFilePath):
  # print(CompleteFilePath)
  # rc,out = subprocess.getstatusoutput(f'pngTellRaw.exe "{CompleteFilePath}"')
  # return out
  os.system(f'pngTellRaw.exe "{CompleteFilePath}"')
  with open('command.mcfunction', encoding='utf-8') as f:
    return f.read()

def writeMcFunction(name, cmd):
  namespace, _name = name.split(':')
  file = f'./{namespace}/{_name}.mcfunction'
  doc = open(file, 'w')
  doc.write(cmd)
  doc.close()


class FallingEntity:
  def __init__(self, x,y,z, x2,y2,z2, tick, noGravity=False, entity='armor_stand', data=''):
    self.x, self.y, self.z, self.x2,self.y2,self.z2, self.tick, self.noGravity = x,y,z, x2,y2,z2, tick, noGravity 
    self.entity, self.data = entity, data
  def toCmd(self, noGravity=None):
    _noGravity = self.noGravity if noGravity == None else noGravity
    dx, dy, dz = self.x2-self.x, self.y2-self.y, self.z2-self.z
    vx         = 0.02*dx / (1-0.98**self.tick)
    vz         = 0.02*dz / (1-0.98**self.tick)
    if _noGravity:
      vy = 0.02*dy / (1-0.98**self.tick)
    else:
      vy = ((0.02*dy + 0.04*(self.tick-1)) / (1-0.98**(self.tick-1))) - 1.96

    if abs(vx) > 10 or abs(vy) > 10 or abs(vz) > 10:
      print(f'Error: In FallingEntity motion is too large !!!')

    NoGravity = 1 if _noGravity else 0
    nbt = f'NoGravity:{NoGravity},Motion:[{vx}d,{vy}d,{vz}d]'
    if self.data != '':
      nbt = self.data + ',' + nbt
    return f'summon {self.entity} {self.x} {self.y} {self.z} {{{nbt}}}'

def fallingEntity(x,y,z, x2,y2,z2, tick, noGravity=False, entity='armor_stand', data=''):
  return FallingEntity(x,y,z, x2,y2,z2, tick, noGravity, entity, data).toCmd()


class FallingBlock: 
  def __init__(self, x,y,z, x2,y2,z2, tick, noGravity=False, block='sand', data=0, toSet=False, force=False):
    self.x, self.y, self.z, self.x2,self.y2,self.z2, self.tick, self.noGravity = x,y,z, x2,y2,z2, tick, noGravity 
    self.block, self.data, self.toSet = block, data, toSet
    self.force = force
  def toCmd(self, noGravity=None):
    _noGravity = self.noGravity if noGravity == None else noGravity
    dx, dy, dz = self.x2-self.x, self.y2-self.y, self.z2-self.z
    vx         = 0.02*dx / (1-0.98**self.tick)
    vz         = 0.02*dz / (1-0.98**self.tick)
    if _noGravity:
      vy = 0.02*dy / (1-0.98**self.tick)
      time = 600 - (self.tick) if self.toSet else 600 - (self.tick - 2) 
    else:
      vy = ((0.02*dy + 0.04*(self.tick)) / (1-0.98**(self.tick))) - 1.96
      time = 600 - (self.tick) if self.toSet else 600 - (self.tick - 1) 
    if (not self.force) and (abs(vx) > 10 or abs(vy) > 10 or abs(vz) > 10):
      print(f'Error: In FallingBlock motion is too large !!! [{vx}, {vy}, {vz}] t:{self.tick}')
    else:
      vx = vx if abs(vx) <= 10 else (10.0 if vx > 0 else -10.0)
      vy = vy if abs(vy) <= 10 else (10.0 if vy > 0 else -10.0)
      vz = vz if abs(vz) <= 10 else (10.0 if vz > 0 else -10.0)

    
    NoGravity = 1 if _noGravity else 0
    return f'summon falling_block {self.x} {self.y} {self.z} {{Block:"{self.block}",Data:{self.data},Time:{time},NoGravity:{NoGravity},Motion:[{vx}d,{vy}d,{vz}d],DropItem:0b}}'

def fallingBlock(x,y,z, x2,y2,z2, tick, noGravity=False, block='sand', data=0, toSet=False, force=False):
  return FallingBlock(x,y,z, x2,y2,z2, tick, noGravity, block, data, toSet, force).toCmd()


# class FallingBlockFack: 
#   def __init__(self, x,y,z, x2,y2,z2, tick, noGravity=False, block='sand', data=0, toSet=True):
#     self.x, self.y, self.z, self.x2,self.y2,self.z2, self.tick, self.noGravity = x,y,z, x2,y2,z2, tick, noGravity 
#     self.block, self.data, self.toSet = block, data, toSet
#   def toCmd(self, noGravity=None):
#     _noGravity = self.noGravity if noGravity == None else noGravity
#     dx, dy, dz = self.x2-self.x, self.y2-self.y, self.z2-self.z
#     vx         = 0.02*dx / (1-0.98**self.tick)
#     vz         = 0.02*dz / (1-0.98**self.tick)
#     if _noGravity:
#       vy = 0.02*dy / (1-0.98**(self.tick))
#     else:
#       vy = ((0.02*dy + 0.04*(self.tick-1)) / (1-0.98**(self.tick-1))) - 1.96 # HERE t-1
#       #                            HERE                      HERE

#     if abs(vx) > 10 or abs(vy) > 10 or abs(vz) > 10:
#       print(f'Error: In FallingBlock motion is too large !!!')

#     time = 600 - (self.tick)
#     time = time if self.toSet else time + 1
#     NoGravity = 1 if _noGravity else 0
#     return f'summon falling_block {self.x} {self.y} {self.z} {{Block:"{self.block}",Data:{self.data},Time:{time},NoGravity:{NoGravity},Motion:[{vx}d,{vy}d,{vz}d],DropItem:0b}}'

# def fallingBlockFack(x,y,z, x2,y2,z2, tick, noGravity=False, block='sand', data=0, toSet=True):
#   return FallingBlockFack(x,y,z, x2,y2,z2, tick, noGravity, block, data, toSet).toCmd()