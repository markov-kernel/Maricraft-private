# Maricraft: TP Back 75
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ execute @s ~~~ tp @s ^0 ^0 ^-75

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]