# Maricraft: Clone Area
# Clones a 10x10x10 area 15 blocks away
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ clone ~-5 ~-1 ~-5 ~5 ~9 ~5 ~10 ~-1 ~-5

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]