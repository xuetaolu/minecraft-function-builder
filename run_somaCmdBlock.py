import midiout
import sequence
import noteMsg
import util
import random

# 在这里设置传入的mid路径
# midifile = r'C:\Users\dell\Desktop\膝盖\金蛇狂舞（双钢琴版）.mid'
midifile = r'./mid/鸟之诗A.mid'
tickRate = 40.0
loopCmd  = ''
lineWidth= 2
lineLen  = 48
buildSpeed = 16
onlyProgram= 1
# loopCmd  = 'tp @a ~0.25 ~ ~'


# 常用指令暴露出来
from util import setblock
from util import fallingBlock
from util import noteParticle
from util import log
from fallingEntity import FallingBlock
from midiout import Soma as SOMA

FB = FallingBlock() # 伪单例模式使用 FallingBlock
Soma = SOMA()
seq = sequence.Seq()

BuildList = {}

DataTableProgram = [1 for c in range(16)]

def setCmdBlocksByPos(x,y,z,cmds):
  res = []
  # print(len(cmds))
  for i,cmd in enumerate( cmds ):
    if i == 0:
      res.append( f'setblock {x} {y+i} {z} command_block 1 replace {{Command:"{cmd}",TrackOutput:0,auto:0}}' )
    else:
      res.append( f'setblock {x} {y+i} {z} chain_command_block 1 replace {{Command:"{cmd}",TrackOutput:0,auto:1}}' )
  return '\n'.join( res )

def setCmdBlocksByTick(tick, cmds):
  _x,_y,_z = 0,32,0

  _length = lineLen
  _width  = lineWidth

  _div = tick // _length
  _mod = tick % (_length*2)

  _z += _div*_width

  _x += (_mod if _mod < _length else 2*_length - _mod -1)*2

  seqCmds = []

  if len(cmds) > 0:
    seqCmds.append(setCmdBlocksByPos(_x, _y, _z, cmds + [noteParticle(_x, _y+len(cmds)+1, _z)]))
  else:
    seqCmds.append(setblock(_x,_y,_z,'wool', random.randint(1,14)))
  
  if _mod < _length:
    seqCmds.append(setblock(_x-1,_y-1,_z,'grass'))
    seqCmds.append(setblock(_x-1,_y,_z,'unpowered_repeater', 1))
    if _mod == 0 and _z > 0:
      seqCmds.append(setblock(_x-1,_y-1,_z-_width,'grass'))
      seqCmds.append(setblock(_x-1,_y,_z-_width,'redstone_wire', 3))
      for Z in range(_z-_width, _z+1):
        seqCmds.append(setblock(_x-2,_y-1,Z,'grass'))
        seqCmds.append(setblock(_x-2,_y,Z,'redstone_wire'))
  else:
    seqCmds.append(setblock(_x+1,_y-1,_z,'grass'))
    seqCmds.append(setblock(_x+1,_y,_z,'unpowered_repeater', 3))
    if _mod == _length:
      seqCmds.append(setblock(_x+1,_y-1,_z-_width,'grass'))
      seqCmds.append(setblock(_x+1,_y,_z-_width,'redstone_wire', 1))
      for Z in range(_z-_width, _z+1):
        seqCmds.append(setblock(_x+2,_y-1,Z,'grass'))
        seqCmds.append(setblock(_x+2,_y,Z,'redstone_wire', 0))
  return '\n'.join(seqCmds)

if __name__ == '__main__':
  msgList = noteMsg.MsgList()
  msgList.load(midifile, tickRate)
  for item in msgList:
    tick = item.tick
    rsTick = tick
    for msg in item.msgs.msgs:
      # 设置乐器
      if msg.velocity == -2:
        DataTableProgram[msg.channel] = msg.program
        print(f'setprogram c:{msg.channel} po:{msg.program}')
        # seq.findByTick(tick).addCmd(midiout.setprogram(msg.channel, msg.program))
        pass

      # 设置控制
      elif msg.velocity == -3:
        print(f'controlchange c:{msg.channel} ct:{msg.control}, v:{msg.value}')
        # seq.findByTick(tick).addCmd(midiout.controlchange(msg.channel, msg.control, msg.value))
        pass

      # 弯轮音
      elif msg.velocity == -1:
        print(f'pitchwheel c:{msg.channel} pi:{msg.pitch}')
        # seq.findByTick(tick).addCmd(midiout.pitchwheel(msg.channel, msg.pitch))
        pass

      # 音符 具备长度、若是弯轮音在 msg.move 中会提供移动值 
      elif msg.velocity > 0:
        sTick = tick
        eTick = tick+msg.length
        channel = msg.channel
        note    = msg.note
        velocity= msg.velocity
        program = onlyProgram if onlyProgram != None else DataTableProgram[msg.channel]

        # 按下
        if not BuildList.__contains__(rsTick):
          BuildList[rsTick] = []
          BuildList[rsTick].append(Soma.toPlaySoundCmd(note, program, velocity))
        else:
          BuildList[rsTick].append(Soma.toPlaySoundCmd(note, program, velocity))


        lastRsTick = rsTick

  # print(BuildList)
  print(f'lastRsTick: {lastRsTick}')

  for i in range(0, lastRsTick+1):
    if BuildList.__contains__(i):
      cmd = setCmdBlocksByTick(i, BuildList[i])
      seq.findByTick(i//buildSpeed).addCmd(cmd)
    else:
      cmd = setCmdBlocksByTick(i, [])
      seq.findByTick(i//buildSpeed).addCmd(cmd)

  seq.makeCmd(log=True, loopCmd=loopCmd)