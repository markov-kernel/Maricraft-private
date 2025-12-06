# Maricraft: Water Pool
# Creates a small water pool
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-3 ~-2 ~-3 ~3 ~-2 ~3 stone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 water

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]