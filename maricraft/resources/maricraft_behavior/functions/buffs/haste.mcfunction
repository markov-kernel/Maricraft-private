# Maricraft: Haste
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

effect @s haste 300 2 true

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]