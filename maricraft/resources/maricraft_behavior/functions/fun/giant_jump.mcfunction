# Maricraft: Giant Jump
# Launches you super high into the air with safe landing
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

effect @s levitation 2 50 true
effect @s slow_falling 30 0 true

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]