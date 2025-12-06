# Maricraft: Golden Apples
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s golden_apple 64

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]