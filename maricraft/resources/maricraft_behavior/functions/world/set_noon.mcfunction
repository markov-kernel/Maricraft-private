# Maricraft: Set Noon
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

time set noon

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]