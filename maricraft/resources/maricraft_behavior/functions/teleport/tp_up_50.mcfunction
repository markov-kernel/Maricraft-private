# Maricraft: TP Up 50
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ tp @s ~ ~50 ~

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]