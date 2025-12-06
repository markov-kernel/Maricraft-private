# Maricraft: Super Axe (Bedrock Edition)
# Gives enchanted netherite axe
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

replaceitem entity @s slot.weapon.mainhand 0 netherite_axe
enchant @s sharpness 5
enchant @s efficiency 5
enchant @s unbreaking 3
enchant @s mending 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]