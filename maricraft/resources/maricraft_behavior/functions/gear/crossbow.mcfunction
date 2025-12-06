# Maricraft: Crossbow (Bedrock Edition)
# Gives enchanted crossbow
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

replaceitem entity @s slot.weapon.mainhand 0 crossbow
enchant @s quick_charge 3
enchant @s multishot 1
enchant @s unbreaking 3

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]