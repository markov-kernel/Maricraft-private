# Maricraft: Find Mineshaft
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

locate structure mineshaft

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]