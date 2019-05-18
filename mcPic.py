# -*- coding: utf-8 -*-  

import matplotlib.image as mpimg
import os

root = (0, 4, 0)

# BlockDB = [
# # wool
# # ('wool 0',221,222,221),
# ('wool 0',208,206,204),
# ('wool 1',219,124,60),
# ('wool 2',181,81,190),
# ('wool 3',109,139,201),
# ('wool 4',180,163,38),
# ('wool 5',67,176,57),
# # ('wool 6',213,161,157),
# ('wool 6',166,129,127),
# ('wool 7',69,69,69),
# ('wool 8',156,163,163),
# ('wool 9',48,113,140),
# ('wool 10',120,56,173),
# ('wool 11',47,59,146),
# ('wool 12',76,48,29),
# ('wool 13',53,71,28),
# ('wool 14',156,54,50),
# ('wool 15',27,23,23),
# # stone
# ('stone 0',130,130,130),
# ('stone 1',164,107,86),
# ('stone 2',168,120,102),
# # ('stone 4',178,178,181),
# ('stone 5',125,125,121),
# ('stone 6',129,129,132),
# # dirt
# ('grass 0',83,127,72),
# ('dirt 0',134,97,67),
# ('dirt 1',92,64,44),
# ('dirt 2',127,79,35),
# ('cobblestone 0',105,105,105),
# # planks
# ('planks 2',194,194,194),
# ('planks 4',183,100,55),
# ('planks 5',60,39,18),
# # log !!!!!!!!!!!! 有方向限制 !!!!!!!!!!!!!!!!!
# ('log 0',183,148,94),
# ('log 1',117,90,53),
# ('log 2',179,154,98),
# ('log 3',167,134,82),
# ('log 4',84,66,40),
# ('log 5',38,24,11),
# # ('log 6',144,149,144),
# ('log 7',71,54,21),
# ('log2 4',77,73,66),
# ('log2 5',35,26,15),

# # ('sponge 0',205,208,67),
# ('sponge 0',172,170,55),
# ('sponge 1',254,213,31),
# ('lapis_block 0',17,38,140),
# # ('sandstone 0',222,213,161),
# ('sandstone 0',169,170,142),
# ('gold_block 0',254,250,75),
# # ('iron_block 0',238,236,230),
# ('iron_block 0',198,195,184),
# ('obsidian 0',34,28,47),
# ('diamond_block 0',111,224,219),
# ('clay 0',153,159,171),
# ('netherrack 0',108,50,50),
# ('soul_sand 0',79,59,46),
# ('mycelium 0',115,100,105),
# ('end_stone 0',255,249,175),
# ('emerald_block 0',71,211,106),
# # ('quartz_block 1',236,234,228),
# ('quartz_block 1',206,217,204),
# # stained_hardened_clay
# # ('stained_hardened_clay 0',255,255,255),
# ('stained_hardened_clay 0',240,240,240),
# ('stained_hardened_clay 1',163,85,38),
# ('stained_hardened_clay 2',149,88,110),
# ('stained_hardened_clay 3',113,110,140),
# ('stained_hardened_clay 4',187,134,38),
# ('stained_hardened_clay 5',104,119,54),
# ('stained_hardened_clay 6',162,80,81),
# ('stained_hardened_clay 7',58,42,36),
# ('stained_hardened_clay 8',135,107,99),
# ('stained_hardened_clay 9',87,90,91),
# ('stained_hardened_clay 10',118,69,86),
# ('stained_hardened_clay 11',74,59,91),
# ('stained_hardened_clay 12',77,52,36),
# ('stained_hardened_clay 13',76,84,43),
# ('stained_hardened_clay 14',144,63,48),
# ('stained_hardened_clay 15',37,23,17),

# ('prismarine 0',95,151,154),
# ('prismarine 1',108,168,153),
# ('prismarine 2',58,91,80),
# ('hay_block 0',163,135,17),
# ('hardened_clay 0',148,90,65),
# ('coal_block 0',19,19,19),
# ('red_sandstone 0',164,83,28),
# ('purpur_block 0',163,117,163),
# ('nether_wart_block 0',138,14,15),
# ('red_nether_brick 0',61,4,6),
# # concrete
# ('concrete 0',208,214,215),
# # ('concrete 0',187,179,170),
# ('concrete 1',225,97,1),
# ('concrete 2',169,48,159),
# ('concrete 3',35,137,198),
# ('concrete 4',241,176,22),
# ('concrete 5',93,168,24),
# ('concrete 6',213,100,142),
# ('concrete 7',55,58,62),
# ('concrete 8',124,124,114),
# ('concrete 9',22,119,136),
# ('concrete 10',101,31,157),
# ('concrete 11',44,46,143),
# ('concrete 12',97,60,32),
# ('concrete 13',74,92,37),
# ('concrete 14',143,34,34),
# ('concrete 15',8,10,15),
# ]

BlockDB = [
('coal_ore 0', 0, 0, 0),
('diamond_ore 0', 15, 15, 15),
('emerald_ore 0', 31, 31, 31),
('gold_ore 0', 47, 47, 47),
('iron_ore 0', 255, 255, 255),
('lapis_ore 0', 239, 239, 239),
('quartz_ore 0', 223, 223, 223),
('redstone_ore 0', 207, 207, 207),
('wool 0', 63, 63, 63),
('stained_hardened_clay 0', 63, 63, 106),
('concrete 0', 63, 106, 63),
('white_glazed_terracotta 0', 63, 106, 106),
('wool 1', 106, 63, 63),
('stained_hardened_clay 1', 106, 63, 106),
('concrete 1', 106, 106, 63),
('orange_glazed_terracotta 0', 106, 106, 106),
('wool 2', 63, 63, 148),
('stained_hardened_clay 2', 63, 106, 148),
('concrete 2', 63, 148, 63),
('magenta_glazed_terracotta 0', 63, 148, 106),
('wool 3', 63, 148, 148),
('stained_hardened_clay 3', 106, 63, 148),
('concrete 3', 106, 106, 148),
('light_blue_glazed_terracotta 0', 106, 148, 63),
('wool 4', 106, 148, 106),
('stained_hardened_clay 4', 106, 148, 148),
('concrete 4', 148, 63, 63),
('yellow_glazed_terracotta 0', 148, 63, 106),
('wool 5', 148, 63, 148),
('stained_hardened_clay 5', 148, 106, 63),
('concrete 5', 148, 106, 106),
('lime_glazed_terracotta 0', 148, 106, 148),
('wool 6', 148, 148, 63),
('stained_hardened_clay 6', 148, 148, 106),
('concrete 6', 148, 148, 148),
('pink_glazed_terracotta 0', 63, 63, 191),
('wool 7', 63, 106, 191),
('stained_hardened_clay 7', 63, 148, 191),
('concrete 7', 63, 191, 63),
('gray_glazed_terracotta 0', 63, 191, 106),
('wool 8', 63, 191, 148),
('stained_hardened_clay 8', 63, 191, 191),
('concrete 8', 106, 63, 191),
('silver_glazed_terracotta 0', 106, 106, 191),
('wool 9', 106, 148, 191),
('stained_hardened_clay 9', 106, 191, 63),
('concrete 9', 106, 191, 106),
('cyan_glazed_terracotta 0', 106, 191, 148),
('wool 10', 106, 191, 191),
('stained_hardened_clay 10', 148, 63, 191),
('concrete 10', 148, 106, 191),
('purple_glazed_terracotta 0', 148, 148, 191),
('wool 11', 148, 191, 63),
('stained_hardened_clay 11', 148, 191, 106),
('concrete 11', 148, 191, 148),
('blue_glazed_terracotta 0', 148, 191, 191),
('wool 12', 191, 63, 63),
('stained_hardened_clay 12', 191, 63, 106),
('concrete 12', 191, 63, 148),
('brown_glazed_terracotta 0', 191, 63, 191),
('wool 13', 191, 106, 63),
('stained_hardened_clay 13', 191, 106, 106),
('concrete 13', 191, 106, 148),
('green_glazed_terracotta 0', 191, 106, 191),
('wool 14', 191, 148, 63),
('stained_hardened_clay 14', 191, 148, 106),
('concrete 14', 191, 148, 148),
('red_glazed_terracotta 0', 191, 148, 191),
('wool 15', 191, 191, 63),
('stained_hardened_clay 15', 191, 191, 106),
('concrete 15', 191, 191, 148),
('black_glazed_terracotta 0', 191, 191, 191),
]

class SetBlock:
  def __init__(self, x, y, z, b):
    self.x, self.y, self.z, self.b = x, y, z, b
  def toCmd(self):
    return f'setblock {self.x} {self.y} {self.z} {self.b} replace'
  def toAir(self):
    return f'setblock {self.x} {self.y} {self.z} air 0 replace'

# R=190, G=190, B=190 
# return 'black_glazed_terracotta 0'
def findBlock(R,G,B):
  def distance(item, R, G, B):
    return (item[1]-R)**2 + (item[2]-G)**2 + (item[3]-B)**2
  res = min(BlockDB, key=lambda item:distance(item, R, G, B))
  return res[0]

def buildPB(picBlocks, fileName, tag=''):
  doc = open(f'./draw/{fileName}{tag}.mcfunction', 'w')
  doc.write('\n'.join([pB.toCmd() for pB in picBlocks]))
  doc.close()  

  doc = open(f'./draw/{fileName}_air{tag}.mcfunction', 'w')
  doc.write('\n'.join([pB.toAir() for pB in picBlocks]))
  doc.close()

def make(file, split=False, hack=True, testing=False):
  pic = mpimg.imread(f'{file}.png')

  picBlocks = []
  x,y,z = root
  reverse = 1
  for line in pic[::-1]:
    z = root[2] if reverse == 1 else root[2] + len(line) - 1
    for pixel in line[::reverse]:
      if len(pixel) < 4 or pixel[3] > 0:
        RGB = [c*255 for c in pixel[0:3]]
        b  = findBlock(*RGB)
        picBlocks.append(SetBlock(x,y,z,b))
      z += reverse
    x += 1
    reverse *= -1

  for i in range(0, 100):
    size  = 2**16
    picBs = picBlocks[i*size:(i+1)*size]
    if len(picBs) == 0:
      break
    buildPB(picBs,fileName=f'all{i}')

if __name__ == '__main__':
  make('23')