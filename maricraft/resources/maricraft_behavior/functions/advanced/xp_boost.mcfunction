# Maricraft: XP Boost 1000
# Adds 1000 experience points
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

xp 1000 @s

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]