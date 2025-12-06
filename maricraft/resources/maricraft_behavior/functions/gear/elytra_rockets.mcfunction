# Maricraft: Elytra + Rockets (Bedrock Edition)
# Gives enchanted elytra and firework rockets
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

replaceitem entity @s slot.armor.chest 0 elytra
enchant @s unbreaking 3
enchant @s mending 1
give @s firework_rocket 64

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]