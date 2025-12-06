# Maricraft: Full Tool Set (Bedrock Edition)
# Gives all netherite tools
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s netherite_pickaxe 1
give @s netherite_shovel 1
give @s netherite_axe 1
give @s netherite_hoe 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]