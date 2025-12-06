# Maricraft: TP to Spawn
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

tp @s 0 100 0

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]