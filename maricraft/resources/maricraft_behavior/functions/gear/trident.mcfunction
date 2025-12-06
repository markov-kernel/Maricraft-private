# Maricraft: Trident (Bedrock Edition)
# Gives enchanted trident
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

replaceitem entity @s slot.weapon.mainhand 0 trident
enchant @s loyalty 3
enchant @s channeling 1
enchant @s impaling 5
enchant @s unbreaking 3

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]