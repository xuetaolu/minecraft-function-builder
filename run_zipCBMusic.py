import midiout
import sequence
import noteMsg
import util
import random
from Sequence2CmdBlock import Sequence2CmdBlock
from collections import defaultdict
import numpy as np

# 在这里设置传入的mid路径
# midifile = r'E:\Minecraft1.11\.minecraft\saves\DEMO 4-4 Hack - old\data\functions\Toilet Story 4(black remix 262278 notes) .mid'
midifile = r'C:\Users\Administrator\Desktop\msDownload\2018-12-14\东方系列神组曲.mid'
# midifile = r'C:\Users\dell\Desktop\膝盖\Be the one.mid'
# midifile = r"./mid/S1.mid"
tickRate = 60.0

buildToCB  = True
buildSpeed = 16
buildSpaceCfg = {
  'x' : 1,     
  'y' : 1,
  'z' : 1,
  'dx': 14,
  'dy': 14,
  'dz': 14,
  'chunkList' : [ (x,y,z) for y in range(1,3+1) for x in range(8) for z in range(8) ], 
}

class PosFunctionOutPutParam:
  def __init__(self):
    self.lastUseChunkIndex = None
    self.loopUseChunkFlag  = False
    self.lenGiveChunk      = None

pfopParam = PosFunctionOutPutParam()

def getChunkPosFunction(x=0,y=0,z=0, dx=16,dy=16,dz=16,chunkList=None, outParam=None):
  chunkList = [(0,0,0)] if chunkList == None or len(chunkList) < 1 else chunkList
  S = dx * dz
  V = dx*dy*dz - 1
  def posFunction( lIndex ):
    chunkListLen = len(chunkList)

    chunkIndex = lIndex // V
    index      = lIndex  % V

    if chunkIndex >= chunkListLen and outParam != None:
      outParam.loopUseChunkFlag  = True
      outParam.lastUseChunkIndex = chunkIndex
      outParam.lenGiveChunk      = chunkListLen
      # print(f'outParam, loopUseChunkFlag:{outParam.loopUseChunkFlag}, lastUseChunkIndex:{outParam.lastUseChunkIndex}, lenGiveChunk:{outParam.lenGiveChunk}')

    chunkPos   = chunkList[chunkIndex%chunkListLen]

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

    pos = tuple( (np.array(pos) + np.array(chunkPos) * 16).tolist() )

    # print(index)
    return pos

  return posFunction

# loopCmd  = ''

# 常用指令暴露出来
from util import setblock
from util import fallingBlock
from util import noteParticle
from fallingEntity import FallingBlock

FB = FallingBlock() # 伪单例模式使用 FallingBlock

def getPos(tick, note, velocity, channel, xfix=0.25, zfix=1.0, x=0.0, y=0.0, z=0.0):
  _x,_y,_z = 64.5,50.05,0
  _x      += tick*xfix + x
  _z      += note*zfix + z
  _y      += y + (channel)*2.0
  return _x,_y,_z

seq = sequence.Seq()

seq2cb = Sequence2CmdBlock()
seq2cb.setPosFunction( getChunkPosFunction(**buildSpaceCfg, outParam=pfopParam) )

def redstoneMusic():
  msgList = noteMsg.MsgList()
  msgList.load(midifile, tickRate)
  for item in msgList:
    tick = item.tick
    for msg in item.msgs.msgs:
      # 设置乐器
      if msg.velocity == -2:
        seq.findByTick(tick).addCmd(midiout.setprogram(msg.channel, msg.program))

      # 设置控制
      elif msg.velocity == -3:
        seq.findByTick(tick).addCmd(midiout.controlchange(msg.channel, msg.control, msg.value))
        pass
      # 弯轮音
      elif msg.velocity == -1:
        seq.findByTick(tick).addCmd(midiout.pitchwheel(msg.channel, msg.pitch))
        pass
      # 音符 具备长度、若是弯轮音在 msg.move 中会提供移动值 
      elif msg.velocity > 0:
        sTick = tick
        eTick = tick+msg.length
        channel = msg.channel
        note    = msg.note
        velocity= msg.velocity

        # 按下
        seq.findByTick(sTick).addCmd(midiout.toCmd(msg.channel, msg.note, msg.velocity))
        # seq.findByTick(sTick).addCmd(setblock(msg.channel, msg.velocity//8, msg.note, 'wool', msg.channel%14+1))

        # 弹起
        seq.findByTick(eTick).addCmd(midiout.toCmd(msg.channel, msg.note, 0))
        # seq.findByTick(sTick).addCmd(setblock(msg.channel, msg.velocity//8, msg.note, 'wool', msg.channel%14+1))

        p0 = getPos(0, note, velocity, channel, y=16, x=-16)
        p1 = getPos(0, note, velocity, channel)
        fT = int((1.0-msg.velocity/128.0)*36.0 + 8.0)+40
        seq.findByTick(sTick-fT).addCmd(FB.getCmdBy2PWithT(*p0, *p1, fT, False, 'wool', channel%14 + 1))##

        # 非弯轮音
        if len(msg.move) == 0:
          p0 = getPos(0, note, velocity, channel)
          p1 = getPos(eTick-sTick, note, velocity, channel)
          pn = getPos(0, note, velocity, channel, y=1)
          fT = msg.length if msg.length > 0 else 1
          maxHeight = 8.0
          for reTick, cmd in FB.getHushCmdsBy2PWithT(*p0, *p1, fT, maxHeight+p0[1], 'wool', channel%14 + 1):
            seq.findByTick(sTick+reTick).addCmd(cmd)##
            pass
          seq.findByTick(sTick).addCmd(noteParticle(*pn))##


          p0 = getPos(0, note, velocity, channel, y=-0.1)
          p1 = getPos(0, note, velocity, channel, y=-1.0)
          fT = int((1.0-msg.velocity/128.0)*36.0 + 8.0)
          seq.findByTick(sTick).addCmd(FB.getCmdBy2PWithT(*p0, *p1, fT, False, 'chain_command_block', channel))##

        # 弯轮音
        else:
          pn = getPos(0, note, velocity, channel, y=1)
          seq.findByTick(tick).addCmd(noteParticle(*pn))##

          lastNote = note
          tmpMove = msg.move[:]
          tmpMove.sort(key = lambda m:m[0])
          if tmpMove[0][0] != 0:
            tmpMove.append((0, 0.0))
            tmpMove.sort(key = lambda m:m[0])

          for i,m in enumerate(tmpMove):
  

            # 这是最后一项
            if i == len(tmpMove)-1:
              if msg.length > m[0]:
                m0 = m
                m1 = m
                sTick = tick + m0[0]
                eTick = tick + msg.length
                sNote = note + m0[1]
                eNote = note + m1[1]
                fT    = eTick - sTick
                lastNote = eNote
              else:
                break

            # 这不是最后一项
            else:
              m0 = m
              m1 = tmpMove[i+1]
              sTick = tick + m0[0]
              eTick = tick + m1[0]
              sNote = note + m0[1]
              eNote = note + m1[1]
              fT    = eTick - sTick
              lastNote = eNote

            p0 = getPos(sTick-tick, sNote, velocity, channel)
            p1 = getPos(eTick-tick, eNote, velocity, channel)
              
            if fT > 0:
              maxHeight = 8.0
              for reTick, cmd in FB.getHushCmdsBy2PWithT(*p0, *p1, fT, maxHeight+p0[1], 'wool', channel%14 + 1):
                seq.findByTick(sTick+reTick).addCmd(cmd)##
              pass

          p0 = getPos(0, note, velocity, channel, y=-0.1)
          p1 = getPos(0, note, velocity, channel, y=-1.0)
          fT = int((1.0-msg.velocity/128.0)*36.0 + 8.0)
          seq.findByTick(tick).addCmd(FB.getCmdBy2PWithT(*p0, *p1, fT, False, 'chain_command_block', channel))##



if __name__ == '__main__':

  redstoneMusic()
  # 
  # for tick in range(0, 100):
  #   seq.findByTick(tick).addCmd(f'say {tick}')
  # if buildToCB:
  # print( f'loopUseChunkFlag: {pfopParam.loopUseChunkFlag}' )

  newSeq = seq.makeCmdToCB(seq2cb, buildSpeed=buildSpeed, autoMake=False)
  if not pfopParam.loopUseChunkFlag:
    newSeq.makeCmd(log=True)
  else:
    print(f'[Error]:You need to give {pfopParam.lastUseChunkIndex+1} chunk(s),')
    print(f'        But you just give {pfopParam.lenGiveChunk} chunk(s).')

  # else:
    # seq.makeCmd(log=True)