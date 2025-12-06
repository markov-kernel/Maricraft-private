# Maricraft: Super Bow (Bedrock Edition)
# Gives enchanted bow with arrows
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

replaceitem entity @s slot.weapon.mainhand 0 bow
enchant @s power 5
enchant @s flame 1
enchant @s infinity 1
enchant @s unbreaking 3
give @s arrow 64

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]