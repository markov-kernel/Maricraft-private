# Maricraft: Bee Hive
# Spawns bees with a bee nest
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~ ~2 ~ bee_nest
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon bee ~ ~3 ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon bee ~1 ~3 ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon bee ~-1 ~3 ~

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]