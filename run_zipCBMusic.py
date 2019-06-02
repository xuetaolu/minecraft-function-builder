import midiout
import sequence
import noteMsg
import util
import random
from Sequence2CmdBlock import Sequence2CmdBlock
from collections import defaultdict

# 在这里设置传入的mid路径
# midifile = r'E:\Minecraft1.11\.minecraft\saves\DEMO 4-4 Hack - old\data\functions\Toilet Story 4(black remix 262278 notes) .mid'
midifile = r'C:\Users\dell\Desktop\膝盖\Be the one.mid'
midifile = r"./mid/S1.mid"
tickRate = 60.0
buildSpeed = 16
buildSpaceCfg = {
  'x' : 1,     
  'y' : 4,
  'z' : 1+32,
  'dx': 30,
  'dy': 128,
  'dz': 30,
}

# loopCmd  = ''

# 常用指令暴露出来
from util import setblock
from util import fallingBlock
from util import noteParticle
from fallingEntity import FallingBlock

FB = FallingBlock() # 伪单例模式使用 FallingBlock

def getPos(tick, note, velocity, channel, xfix=0.25, zfix=1.0, x=0.0, y=0.0, z=0.0):
  _x,_y,_z = 0.5,16.05,13.5+88
  _x      += tick*xfix + x
  _z      += -note*zfix + z
  _y      += y + (channel)*2.0
  return _x,_y,_z

seq = sequence.Seq()

seq2cb = Sequence2CmdBlock()
seq2cb.setCubePosFunction(**buildSpaceCfg)

cmdSeq = defaultdict(list)
def cmdSeqAddCmd( i, cmd ):
  for c in cmd.split('\n'):
    if len(c) == 1:
      continue
    cmdSeq[i].append( c )

def redstoneMusic():
  msgList = noteMsg.MsgList()
  msgList.load(midifile, tickRate)
  for item in msgList:
    tick = item.tick
    for msg in item.msgs.msgs:
      # 设置乐器
      if msg.velocity == -2:
        # seq.findByTick(tick).addCmd(midiout.setprogram(msg.channel, msg.program))
        cmdSeqAddCmd( tick, midiout.setprogram(msg.channel, msg.program) )

      # 设置控制
      elif msg.velocity == -3:
        # seq.findByTick(tick).addCmd(midiout.controlchange(msg.channel, msg.control, msg.value))
        cmdSeqAddCmd( tick, midiout.controlchange(msg.channel, msg.control, msg.value) )

      # 弯轮音
      elif msg.velocity == -1:
        # seq.findByTick(tick).addCmd(midiout.pitchwheel(msg.channel, msg.pitch))
        cmdSeqAddCmd( tick, midiout.pitchwheel(msg.channel, msg.pitch) )

      # 音符 具备长度、若是弯轮音在 msg.move 中会提供移动值 
      elif msg.velocity > 0:
        sTick = tick
        eTick = tick+msg.length
        channel = msg.channel
        note    = msg.note
        velocity= msg.velocity

        # 按下
        # seq.findByTick(sTick).addCmd(midiout.toCmd(msg.channel, msg.note, msg.velocity))
        cmdSeqAddCmd( sTick, midiout.toCmd(msg.channel, msg.note, msg.velocity) )

        # 弹起
        # seq.findByTick(eTick).addCmd(midiout.toCmd(msg.channel, msg.note, 0))
        cmdSeqAddCmd( eTick, midiout.toCmd(msg.channel, msg.note, 0) )

        # p0 = getPos(sTick, note, velocity, channel, y=16, x=-16)
        # p1 = getPos(sTick, note, velocity, channel)
        # fT = int((1.0-msg.velocity/128.0)*36.0 + 8.0)
        # seq.findByTick(sTick-fT).addCmd(FB.getCmdBy2PWithT(*p0, *p1, fT, False, 'wool', channel%14 + 1))##

        # # 非弯轮音
        # if len(msg.move) == 0:
        #   p0 = getPos(sTick, note, velocity, channel)
        #   p1 = getPos(eTick, note, velocity, channel)
        #   pn = getPos(sTick, note, velocity, channel, y=1)
        #   fT = msg.length if msg.length > 0 else 1
        #   maxHeight = 8.0
        #   for reTick, cmd in FB.getHushCmdsBy2PWithT(*p0, *p1, fT, maxHeight+p0[1], 'wool', channel%14 + 1):
        #     seq.findByTick(sTick+reTick).addCmd(cmd)##
        #     pass
        #   seq.findByTick(sTick).addCmd(noteParticle(*pn))##


        #   p0 = getPos(sTick, note, velocity, channel, y=-0.1)
        #   p1 = getPos(sTick, note, velocity, channel, y=-1.0)
        #   fT = int((1.0-msg.velocity/128.0)*36.0 + 8.0)
        #   seq.findByTick(sTick).addCmd(FB.getCmdBy2PWithT(*p0, *p1, fT, False, 'chain_command_block', channel))##

        # # 弯轮音
        # else:
        #   pn = getPos(tick, note, velocity, channel, y=1)
        #   seq.findByTick(tick).addCmd(noteParticle(*pn))##

        #   lastNote = note
        #   tmpMove = msg.move[:]
        #   tmpMove.sort(key = lambda m:m[0])
        #   if tmpMove[0][0] != 0:
        #     tmpMove.append((0, 0.0))
        #     tmpMove.sort(key = lambda m:m[0])

        #   for i,m in enumerate(tmpMove):
  

        #     # 这是最后一项
        #     if i == len(tmpMove)-1:
        #       if msg.length > m[0]:
        #         m0 = m
        #         m1 = m
        #         sTick = tick + m0[0]
        #         eTick = tick + msg.length
        #         sNote = note + m0[1]
        #         eNote = note + m1[1]
        #         fT    = eTick - sTick
        #         lastNote = eNote
        #       else:
        #         break

        #     # 这不是最后一项
        #     else:
        #       m0 = m
        #       m1 = tmpMove[i+1]
        #       sTick = tick + m0[0]
        #       eTick = tick + m1[0]
        #       sNote = note + m0[1]
        #       eNote = note + m1[1]
        #       fT    = eTick - sTick
        #       lastNote = eNote

        #     p0 = getPos(sTick, sNote, velocity, channel)
        #     p1 = getPos(eTick, eNote, velocity, channel)
              
        #     if fT > 0:
        #       maxHeight = 8.0
        #       for reTick, cmd in FB.getHushCmdsBy2PWithT(*p0, *p1, fT, maxHeight+p0[1], 'wool', channel%14 + 1):
        #         seq.findByTick(sTick+reTick).addCmd(cmd)##
        #       pass

        #   p0 = getPos(tick, note, velocity, channel, y=-0.1)
        #   p1 = getPos(tick, note, velocity, channel, y=-1.0)
        #   fT = int((1.0-msg.velocity/128.0)*36.0 + 8.0)
        #   seq.findByTick(tick).addCmd(FB.getCmdBy2PWithT(*p0, *p1, fT, False, 'chain_command_block', channel))##



if __name__ == '__main__':

  redstoneMusic()

  # for i in range(0,100):
  #   cmdSeqAddCmd(i, f'say {i/60.0}')

  minI = min([ k for k,v in cmdSeq.items() ])
  maxI = max([ k for k,v in cmdSeq.items() ])
  for i, cmds in seq2cb.getCmdBlockBySequence( ( cmdSeq[i] for i in range( minI, maxI + 1) ), maxI-minI + 1 ):
    seq.findByTick(i//buildSpeed).addCmd(cmds)

  seq.makeCmd(log=True)