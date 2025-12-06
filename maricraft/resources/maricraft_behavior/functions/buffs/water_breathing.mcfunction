# Maricraft: Water Breathing
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

effect @s water_breathing 600 0 true

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]