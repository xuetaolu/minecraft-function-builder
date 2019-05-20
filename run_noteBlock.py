import midiout
import sequence
import noteMsg
import util
import random

# 在这里设置传入的mid路径
# midifile = r'E:\Minecraft1.11\.minecraft\saves\DEMO 4-4 Hack - old\data\functions\Toilet Story 4(black remix 262278 notes) .mid'
midifile = r'./mid/彩虹猫-Part.mid'
tickRate = 28.0
noteRoot = 66
lineWidth= 8


# 常用指令暴露出来
from util import setblock
from util import fallingBlock
from util import noteParticle
from fallingEntity import FallingBlock

FB = FallingBlock() # 伪单例模式使用 FallingBlock
NB = midiout.NoteBlock()
seq = sequence.Seq()

# def getPos(tick, note, velocity, channel, xfix=0.25, zfix=1.0, x=0.0, y=0.0, z=0.0):
#   _x,_y,_z = 0.5,16.05,13.5+88
#   _x      += tick*xfix + x
#   _z      += -note*zfix + z
#   _y      += y + (channel)*2.0
#   return _x,_y,_z
#   
def getNoteBlocksCmd(tick, noteList):
  _x,_y,_z = 0,4,0

  _length = 16
  _width  = lineWidth

  _div = tick // _length
  _mod = tick % (_length*2)

  _z += _div*_width

  _x += (_mod if _mod < _length else 2*_length - _mod -1)*2


  dLen = (_width//2) * 2
  dx = [0 for i in range(dLen)]
  dy = [0 for i in range(dLen)]
  dz = [0] + [-i for i in range(1,_width//2+1)] + [i for i in range(1,_width//2+1)]
  dz.sort(key=lambda a: abs(a))
  print(dz, _width//2)

  cmds = []
  if len(noteList) > 0:
    for i,note in enumerate(noteList):
      if i >= dLen:
        print(f'in getNoteBlocksCmd i > {dLen}')
        break
      else:
        x,y,z = _x+dx[i], _y+dy[i], _z+dz[i]
        cmds.append(NB.toNoteBlockCmd(note, x,y,z, root=noteRoot))
        # x,y,z = x,y+1,z
        # cmds.append(setblock(x,y,z, 'redstone_wire', 0))
  else:
    cmds.append(setblock(_x,_y,_z,'grass', 1))
  
  if _mod < _length:
    cmds.append(setblock(_x-1,_y,_z,'unpowered_repeater', 1))
    if _mod == 0 and _z > 0:
      cmds.append(setblock(_x-1,_y,_z-_width,'redstone_wire', 3))
      for Z in range(_z-_width, _z+1):
        cmds.append(setblock(_x-2,_y,Z,'redstone_wire', 0))
  else:
    cmds.append(setblock(_x+1,_y,_z,'unpowered_repeater', 3))
    if _mod == _length:
      # print(f'{_x}')
      cmds.append(setblock(_x+1,_y,_z-_width,'redstone_wire', 1))
      for Z in range(_z-_width, _z+1):
        cmds.append(setblock(_x+2,_y,Z,'redstone_wire', 0))
  return '\n'.join(cmds)

BuildList = {}

if __name__ == '__main__':
  msgList = noteMsg.MsgList()
  msgList.load(midifile, tickRate)
  for item in msgList.msgList:
    tick = item.tick
    rsTick = int(tick/2)
    for msg in item.msgs.msgs:
      # 设置乐器
      if msg.velocity == -2:
        # seq.findByTick(tick).addCmd(midiout.setprogram(msg.channel, msg.program))
        pass

      # 设置控制
      elif msg.velocity == -3:
        # seq.findByTick(tick).addCmd(midiout.controlchange(msg.channel, msg.control, msg.value))
        pass

      # 弯轮音
      elif msg.velocity == -1:
        # seq.findByTick(tick).addCmd(midiout.pitchwheel(msg.channel, msg.pitch))
        pass

      # 音符 具备长度、若是弯轮音在 msg.move 中会提供移动值 
      elif msg.velocity > 0:
        sTick = tick
        eTick = tick+msg.length
        channel = msg.channel
        note    = msg.note
        velocity= msg.velocity

        # 按下
        if not BuildList.__contains__(rsTick):
          BuildList[rsTick] = []
          BuildList[rsTick].append(msg.note)
        else:
          BuildList[rsTick].append(msg.note)

        lastRsTick = rsTick
        # 
        # print(f'c:{msg.channel}, n:{msg.note}, v:{msg.velocity}')
        # seq.findByTick(tick).addCmd(util.log(f't:{tick}, c:{msg.channel}, n:{msg.note}, v:{msg.velocity}'))
        # seq.findByTick(sTick).addCmd(NB.toPlaySoundCmd(msg.note, msg.velocity))



        # # 弹起
        # seq.findByTick(eTick).addCmd(midiout.toCmd(msg.channel, msg.note, 0))

  print(BuildList)
  print(lastRsTick)

  for i in range(0, lastRsTick+1):
    if BuildList.__contains__(i):
      cmd = getNoteBlocksCmd(i, BuildList[i])
      seq.findByTick(i).addCmd(cmd)
    else:
      cmd = getNoteBlocksCmd(i, [])
      seq.findByTick(i).addCmd(cmd)

  seq.makeCmd(log=True)