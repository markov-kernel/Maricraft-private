# Maricraft: Wolf Pack
# Spawns 5 wolves (Bedrock: bring bones to tame them!)
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon wolf ~ ~ ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon wolf ~1 ~ ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon wolf ~-1 ~ ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon wolf ~ ~ ~1
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon wolf ~ ~ ~-1
give @s bone 10

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]