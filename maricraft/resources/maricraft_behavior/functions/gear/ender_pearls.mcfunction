# Maricraft: Ender Pearls
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s ender_pearl 16

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]