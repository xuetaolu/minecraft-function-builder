fill ~ ~ ~ ~-9 ~ ~ stone_slab 4 replace brick_block 0
fill ~ ~ ~-1 ~-9 ~ ~-1 quartz_stairs 3 replace quartz_block 0
fill ~ ~ ~-1 ~-9 ~ ~-1 stone_slab 7 replace quartz_stairs 2
fill ~ ~ ~1 ~-9 ~ ~1 quartz_stairs 2 replace quartz_block 0
fill ~ ~ ~1 ~-9 ~ ~1 stone_slab 7 replace quartz_stairs 3
particle note ~-8.2 ~.3 ~0.5 .2 0 .2 1 1 force @a
#summon falling_block ~1.4 ~3.1 ~0.5 {Block:"redstone_block",Data:0,DropItem:0b,NoGravity:1b}
#summon falling_block ~-6.3 ~1.7 ~0.5 {Block:"redstone_block",Data:0,DropItem:0b,NoGravity:1b}