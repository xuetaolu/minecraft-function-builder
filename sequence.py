import os
import shutil
import time

outputFolder = '_seq'

class SeqItem:
  def __init__(self, tick):
    self.tick=tick
    self.cmds=[]

  def addCmd(self, cmd, filter=None):
    for c in cmd.split('\n'):
      if len(c) > 0:
        if filter != None:
          self.cmds.append( filter(c) )
        else:
          self.cmds.append(c)

class Seq:
  def __init__(self):
    self._seqDict = {}

  def __iter__(self):
    tmpList = [item for k,item in self._seqDict.items()]
    tmpList.sort(key=lambda item: item.tick)
    fix     = -tmpList[0].tick
    for item in tmpList:
      item.tick += fix
      yield item

  def yieldAllTick(self, minI, maxI, loopCmd=''):
  # minI = min([ k for k in self._seqDict ])
  # maxI = max([ k for k in self._seqDict ])
    for tick in range(minI, maxI):
      res = None
      if tick in self._seqDict:
        res = self._seqDict[tick].cmds + [loopCmd]
      else:
        res = []
      if len(loopCmd) > 0:
        yield res + [loopCmd]
      else:
        yield res

  def findByTick(self, tick):
    if tick in self._seqDict:
      return self._seqDict[tick]
    # 查无此项
    newSeqItem = SeqItem(tick)
    self._seqDict[tick] = newSeqItem
    return newSeqItem

  def insert(self, tick, cmd):
    self.findByTick(tick).addCmd(cmd)

  # def fixSeq(self):
  #   self._seqDict.sort(key=lambda item: item.tick)
  #   fix = -self._seqDict[0].tick
  #   for item in self._seqDict:
  #     item.tick += fix

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
    # self.fixSeq()
    self.clearCmd()

    # 测试
    if log:
      doc = open(f'log.txt', 'w', encoding='utf-8')
      for item in self:
        doc.write(f'tick: {item.tick}' + '\n')
        doc.write('\n'.join(['  ' + s for s in item.cmds]) + '\n')

    lastTick = 0
    for item in self:
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

  def makeCmdToCB(self, seq2cbObj, log=False, buildSpeed=16, loopCmd='', autoMake=True):
    minI = min([ k for k in self._seqDict ])
    maxI = max([ k for k in self._seqDict ])
    newSeq = Seq()
    for i, cmds in seq2cbObj.getCmdBlockBySequence( self.yieldAllTick(minI, maxI+1, loopCmd), maxI-minI + 1 ):
      newSeq.findByTick(i//buildSpeed).addCmd(cmds)
    if autoMake:
      newSeq.makeCmd(log=log)
    return newSeq

if __name__ == '__main__':
  seq = Seq()
  for i in range(4, 12):
    cmd = f'setblock 14 65 {i} dirt'
    seq.findByTick(i).addCmd(cmd)
  for i in range(20, 24):
    cmd = f'setblock 14 65 {i} dirt'
    seq.findByTick(i).addCmd(cmd)    
  seq.makeCmd()
