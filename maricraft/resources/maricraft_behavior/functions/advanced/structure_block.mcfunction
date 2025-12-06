# Maricraft: Structure Block
# Gives structure blocks for saving/loading builds
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s structure_block 4

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]