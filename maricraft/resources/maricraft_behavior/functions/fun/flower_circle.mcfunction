# Maricraft: Flower Circle
# Creates a circle of flowers around you
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~3 ~ ~ poppy
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-3 ~ ~ dandelion
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~ ~ ~3 blue_orchid
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~ ~ ~-3 allium
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~2 ~ ~2 azure_bluet
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-2 ~ ~2 red_tulip
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~2 ~ ~-2 orange_tulip
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-2 ~ ~-2 pink_tulip

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]