# Maricraft: Clear Area 10x10
# Removes all blocks in a 10x10x10 cube around the player
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-5 ~ ~-5 ~5 ~10 ~5 air

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]