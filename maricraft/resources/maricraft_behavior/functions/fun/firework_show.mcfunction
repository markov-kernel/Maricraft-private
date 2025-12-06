# Maricraft: Firework Show
# Launches fireworks all around
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon fireworks_rocket ~ ~1 ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon fireworks_rocket ~3 ~1 ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon fireworks_rocket ~-3 ~1 ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon fireworks_rocket ~ ~1 ~3

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]