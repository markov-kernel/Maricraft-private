# Maricraft: Diamond Armor
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s diamond_helmet 1
give @s diamond_chestplate 1
give @s diamond_leggings 1
give @s diamond_boots 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]