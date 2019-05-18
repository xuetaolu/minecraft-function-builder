import mido

class Msg:
  def __init__(self, t=0, T=0, c=0, n=0, v=0, l=1, p=0, program=0, control=0, value=0):
    self.tick     = t
    self.track    = T
    self.channel  = c
    self.note     = n
    self.velocity = v
    self.length   = l
    self.pitch    = p
    self.program  = program
    self.control  = control
    self.value    = value
    self.move     = []

class Msgs:
  def __init__(self):
    self.msgs = []

  def append(self, newMsg):
    self.msgs.append(newMsg)

  def hasMsgDown(self, channel, note, beside=None):
    for msg in self.msgs:
      if msg.channel == channel and msg.note == note and msg.velocity > 0 and msg != beside:
        return True
    return False

class MsgListItem:
  def __init__(self):
    self.tick = 0
    self.msgs = Msgs()

class MsgList:
  def __init__(self):
    # 最终要保存的信息表 msgList
    self.msgList = []

  def findByTick(self, tick):
    for item in self.msgList:
      if item.tick == tick:
        return item
    # 查无此项
    newItem = MsgListItem()
    newItem.tick = tick
    self.msgList.append(newItem)
    return newItem

  def fixForShortNote(self, item):
    for msg in item.msgs.msgs:
      if msg.velocity == 0 and item.msgs.hasMsgDown(channel=msg.channel, note=msg.note):
        tick = item.tick + 1
        self.findByTick(tick).msgs.append(msg)
        item.msgs.msgs.remove(msg)

  def fixForOverLapNote(self, item):
    for msg in item.msgs.msgs:
      if msg.velocity == 0 and item.msgs.hasMsgDown(channel=msg.channel, note=msg.note):
        tick = item.tick - 1
        self.findByTick(tick).msgs.append(msg)
        item.msgs.msgs.remove(msg)

  def fixForRepeatNote(self, item):
    for msg in item.msgs.msgs:
      if msg.velocity > 0 and item.msgs.hasMsgDown(channel=msg.channel, note=msg.note, beside=msg):
        item.msgs.msgs.remove(msg)

  def fixForOverLapPitch(self, item, newMsg):
    for msg in item.msgs.msgs:
      if msg != newMsg and msg.velocity == -1 and msg.channel == newMsg.channel:
        item.msgs.msgs.remove(msg)

  def sortByTick(self):
    self.msgList.sort(key=lambda item: item.tick)

  def makeLength(self):
    noteMsgMarker = [[None for note in range(0,128+1)] for channel in range(0,15+1)]
    for item in self.msgList:
      for msg in item.msgs.msgs:
        n = msg.note
        c = msg.channel
        # 这个信息是按下的，标记一下
        if msg.velocity > 0:
          noteMsgMarker[c][n] = msg
        # 当前信息是抬起的，从已标记的notemsg查找，根据它的tick补回它的length
        elif noteMsgMarker[c][n] != None:
          noteMsgMarker[c][n].length = msg.tick - noteMsgMarker[c][n].tick
          noteMsgMarker[c][n] = None

  def makePitch(self):
    noteMsgMarker = [[None for note in range(0,128+1)] for channel in range(0,15+1)]
    for item in self.msgList:
      for msg in item.msgs.msgs:
        n = msg.note
        c = msg.channel
        # 这个信息是按下的，标记一下
        if msg.velocity > 0:
          noteMsgMarker[c][n] = msg
        # 当前信息是抬起的，从已标记的notemsg查找，根据它的tick补回它的length
        elif msg.velocity == 0:
          noteMsgMarker[c][n] = None
        elif msg.velocity == -1:
          for markMsg in noteMsgMarker[c]:
            if markMsg != None:
              dt = msg.tick - markMsg.tick
              move = (msg.pitch-128*64) / 64 / 4 / 2
              markMsg.move.append((dt, move))


  def load(self, file, tickrate=20.0, makeLength=True, makePitch=True):
    mid = mido.MidiFile(file)
    currentTime = 0.0
    currentTick = 0

    lastChannel, lastNote = -1, -1
    for msg in mid:
      if msg.is_meta:
        if msg.time > 0:
          currentTime += msg.time

      elif msg.type == 'program_change':
        if msg.time > 0:
          currentTime += msg.time
        m = {
          'track'   : 0, #msg.track,
          'channel' : msg.channel,
          'note'    : -2,
          'velocity': -2,
          'program' : msg.program,
          # 'time'    : msg.time,
          # 'tick'    : int(round(time / tickDelta)),
        }
        toTick = int(round(currentTime / (1/tickrate)))
        newMsg = Msg(toTick,m['track'],m['channel'],m['note'],m['velocity'],program=m['program'])
        item = self.findByTick(toTick)
        item.msgs.append(newMsg)  

      elif msg.type == 'control_change':
        if msg.time > 0:
          currentTime += msg.time

        m = {
          'track'   : 0, #msg.track,
          'channel' : msg.channel,
          'note'    : -3,
          'velocity': -3,
          'control' : msg.control,
          'value'   : msg.value,
          # 'time'    : msg.time,
          # 'tick'    : int(round(time / tickDelta)),
        }
        toTick = int(round(currentTime / (1/tickrate)))
        newMsg = Msg(toTick,m['track'],m['channel'],m['note'],m['velocity'],control=m['control'],value=m['value'])
        item = self.findByTick(toTick)
        item.msgs.append(newMsg)  

      elif msg.type == 'pitchwheel':
        if msg.time == 0: # to be test
          continue
        currentTime += msg.time
        m = {
          'track'   : 0, #msg.track,
          'channel' : msg.channel,
          'note'    : -1,
          'velocity': -1,
          'pitch'   : msg.pitch + 128*64,
          # 'time'    : msg.time,
          # 'tick'    : int(round(time / tickDelta)),
        }

        toTick = int(round(currentTime / (1/tickrate)))

        newMsg = Msg(toTick,m['track'],m['channel'],m['note'],m['velocity'],p=m['pitch'])
        
        # print(f'newItem: t:{newMsg.tick} c:{newMsg.channel} v:{newMsg.velocity} p:{newMsg.pitch}')

        item = self.findByTick(toTick)
        item.msgs.append(newMsg)  
        
        self.fixForOverLapPitch(item, newMsg)



      elif msg.type == 'note_on' or msg.type == 'note_off':
        if msg.time == 0 and lastChannel == msg.channel and lastNote == msg.note and msg.velocity == 0:
          continue

        lastChannel, lastNote = msg.channel, msg.note

        currentTime += msg.time
        m = {
          'track'   : 0, #msg.track,
          'channel' : msg.channel,
          'note'    : msg.bytes()[1],
          'velocity': 0 if msg.type == 'note_off' else msg.bytes()[2],
          # 'time'    : msg.time,
          # 'tick'    : int(round(time / tickDelta)),
        }

        toTick = int(round(currentTime / (1/tickrate)))

        newMsg = Msg(toTick,m['track'],m['channel'],m['note'],m['velocity'])
        
        item = self.findByTick(toTick)
        item.msgs.append(newMsg)

        if newMsg.velocity > 0:
          self.fixForOverLapNote(item)
          self.fixForRepeatNote(item)
        else:
          self.fixForShortNote(item)

      else:
        # print(f'In else: {msg.time}')
        if msg.time > 0:
          currentTime += msg.time

    self.sortByTick()

    if makeLength:
      self.makeLength()

    if makePitch:
      self.makePitch()


if __name__ == '__main__':
  msgList = MsgList()
  msgList.load(f'./mid/test.mid', 100.0 / 5, makeLength=True)
  for item in msgList.msgList:
    print(f'tick: {item.tick}')
    for msg in item.msgs.msgs:
      if msg.velocity > 0:
        print(f'  msg: c:{msg.channel} n:{msg.note} v:{msg.velocity} l:{msg.length}')
        pass


          




