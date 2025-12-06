# Maricraft: Steak x64
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s cooked_beef 64

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]