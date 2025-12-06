# Maricraft: Glass Platform
# Creates a glass floor beneath the player
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 glass

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]