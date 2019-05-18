import os
import shutil
import time

outputFolder = '_seq'

class SeqItem:
  def __init__(self, tick):
    self.tick=tick
    self.cmds=[]

  def addCmd(self, cmd):
    self.cmds.append(cmd)

class Seq:
  def __init__(self):
    self.seq = []

  def findByTick(self, tick):
    for item in self.seq:
      if item.tick == tick:
        return item
    # 查无此项
    newSeqItem = SeqItem(tick)
    self.seq.append(newSeqItem)
    return newSeqItem

  def insert(self, tick, cmd):
    self.findByTick(tick).addCmd(cmd)

  def fixSeq(self):
    self.seq.sort(key=lambda item: item.tick)
    fix = -self.seq[0].tick
    for item in self.seq:
      item.tick += fix

  def clearCmd(self):
    try:
      shutil.rmtree(f'./{outputFolder}')
    except:
      pass
    time.sleep(1)
    os.mkdir(f'./{outputFolder}')

  def buildCmd(self, index, cmd):
    doc = open(f'./{outputFolder}/{index}.mcfunction', 'w', encoding='utf-8')
    doc.write(cmd)
    doc.close()

  def makeCmd(self, log=False, loopCmd=''):
    self.fixSeq()
    self.clearCmd()

    # 测试
    if log:
      doc = open(f'log.txt', 'w', encoding='utf-8')
      for item in self.seq:
        doc.write(f'tick: {item.tick}' + '\n')
        doc.write('\n'.join(['  ' + s for s in item.cmds]) + '\n')

    lastTick = 0
    for item in self.seq:
      currentTick = item.tick

      # 填充空帧
      if currentTick - lastTick > 1:
        for i in range(lastTick+1, currentTick):
          self.buildCmd(i, f'gamerule gameLoopFunction {outputFolder}:{i+1}' + '\n' + loopCmd)

      # 写当前帧
      cmdStr = '\n'.join(item.cmds) + f'\ngamerule gameLoopFunction {outputFolder}:{currentTick+1}' + '\n' + loopCmd
      self.buildCmd(currentTick, cmdStr)
      lastTick = currentTick
    self.buildCmd(lastTick+1, f'\ngamerule gameLoopFunction {outputFolder}:999999')

if __name__ == '__main__':
  seq = Seq()
  for i in range(4, 12):
    cmd = f'setblock 14 65 {i} dirt'
    seq.findByTick(i).addCmd(cmd)
  for i in range(20, 24):
    cmd = f'setblock 14 65 {i} dirt'
    seq.findByTick(i).addCmd(cmd)    
  seq.makeCmd()
