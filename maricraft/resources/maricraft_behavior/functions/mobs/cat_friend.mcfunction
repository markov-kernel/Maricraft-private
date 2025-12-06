# Maricraft: Cat Friend
# Spawns a cat (Bedrock: bring fish to tame it!)
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon cat ~ ~ ~
give @s fish 5

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]