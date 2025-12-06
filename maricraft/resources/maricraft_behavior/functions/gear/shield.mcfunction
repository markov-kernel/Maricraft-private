# Maricraft: Shield (Bedrock Edition)
# Gives enchanted shield to offhand
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

replaceitem entity @s slot.weapon.offhand 0 shield
enchant @s unbreaking 3
enchant @s mending 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]