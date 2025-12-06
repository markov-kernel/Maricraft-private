# Maricraft: Light Blocks
# Gives invisible light sources
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s light_block 16

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]