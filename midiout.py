def toCmd(channel, note, velocity):
  if velocity == 0:
    return f'midiout noteclose {channel} {note}'
  else:
    return f'midiout noteopen {channel} {note} {velocity}'

def pitchwheel(channel, pitch):
  # pitch 0-16383
  msb = pitch // 128
  lsb = pitch % 128
  # print(f'pitch:{pitch} lsb:{lsb} msb:{msb}')
  return f'midiout pitchwheelrange {channel} {lsb} {msb}'

def setprogram(channel, program):
  return f'midiout setprogram {channel} {program}'

def controlchange(channel, control, value):
  return f'midiout setcontrol {channel} {control} {value}'

class NoteBlock:
  def __init__(self):
    pass
  def toPlaySoundCmd(self, note, velocity, root=66):
    _note = note - root
    if 0 <= _note <= 24:
      pitch = 2**((_note-12)/12)
      return f'execute xue ~ ~ ~ playsound minecraft:block.note.harp voice @a ~ ~ ~ {velocity/128} {pitch}'
    else:
      print(f'Out of range in NB toPlaySoundCmd: {note}')
      return ''
  def toNoteBlockCmd(self, note, x,y,z, root=66):
    _note = note - root
    if 0 <= _note <= 24:
      return f'setblock {x} {y} {z} noteblock 0 destroy {{note:{_note}}}'
    else:
      print(f'Out of range in NB toNoteBlockCmd: {note}')
      return ''


if __name__ == '__main__':
  NB = NoteBlock()
  print(NB.toPlaySoundCmd(56))