# Maricraft: Light Up Area
# Places sea lanterns in a grid pattern
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-4 ~-1 ~-4 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~4 ~-1 ~-4 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-4 ~-1 ~4 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~4 ~-1 ~4 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~ ~-1 ~ sea_lantern

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]