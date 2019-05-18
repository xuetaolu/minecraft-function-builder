setblock ~1 ~1 ~ stone_slab 6 replace
fill ~ ~1 ~ ~-5 ~1 ~ air 0 replace nether_brick 0
setblock ~-6 ~1 ~ air 0 replace
setblock ~-6 ~ ~ nether_brick_stairs 0
particle note ~-6.8 ~1.5 ~0.5 .1 0 .1 1 1 force @a
#summon falling_block ~1.4 ~3.1 ~0.5 {Block:"redstone_block",Data:0,DropItem:0b,NoGravity:1b}
#summon falling_block ~-4.7 ~2.2 ~0.5 {Block:"redstone_block",Data:0,DropItem:0b,NoGravity:1b}