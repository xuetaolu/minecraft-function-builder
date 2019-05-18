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