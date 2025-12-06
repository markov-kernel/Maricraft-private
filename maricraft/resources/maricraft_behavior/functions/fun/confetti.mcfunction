# Maricraft: Confetti
# Celebrate with confetti particles!
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ particle minecraft:totem_particle ~ ~1 ~

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]