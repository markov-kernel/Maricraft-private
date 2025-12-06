# Maricraft: Totem of Undying
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s totem_of_undying 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]