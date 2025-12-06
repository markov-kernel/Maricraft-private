# Maricraft: TP to Surface
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ tp @s ~ 320 ~
effect @s slow_falling 10 0 true

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]