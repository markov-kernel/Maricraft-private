# Maricraft: Parrot Party
# Spawns 3 colorful parrots
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon parrot ~ ~ ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon parrot ~1 ~ ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon parrot ~-1 ~ ~

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]