# Maricraft: Lightning Strike
# Strikes lightning where you stand
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon lightning_bolt ~ ~ ~

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]