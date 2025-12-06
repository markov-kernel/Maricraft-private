# Maricraft: Super Sword (Bedrock Edition)
# Gives enchanted netherite sword
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

replaceitem entity @s slot.weapon.mainhand 0 netherite_sword
enchant @s sharpness 5
enchant @s fire_aspect 2
enchant @s looting 3
enchant @s unbreaking 3
enchant @s mending 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]