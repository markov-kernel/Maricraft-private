# Maricraft: Safe Fire
# Set yourself on fire (with fire resistance!)
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

effect @s fire_resistance 60 0 true
effect @s regeneration 60 1 true

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]