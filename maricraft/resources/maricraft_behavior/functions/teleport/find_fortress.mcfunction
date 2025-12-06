# Maricraft: Find Fortress
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

locate structure fortress

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]