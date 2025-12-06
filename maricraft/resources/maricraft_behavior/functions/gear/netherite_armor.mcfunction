# Maricraft: Netherite Armor
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s netherite_helmet 1
give @s netherite_chestplate 1
give @s netherite_leggings 1
give @s netherite_boots 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]