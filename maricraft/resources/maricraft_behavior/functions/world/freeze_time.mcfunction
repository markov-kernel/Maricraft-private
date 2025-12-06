# Maricraft: Freeze Time
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

gamerule doDaylightCycle false

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]