# Maricraft: Horse + Saddle
# Spawns a horse and gives you a saddle
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon horse ~ ~ ~ minecraft:ageable_grow_up
give @s saddle 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]