# Maricraft: Disco Lights
# Spawns colorful particle effects
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ particle minecraft:balloon_gas_particle ~ ~2 ~
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ particle minecraft:falling_dust ~ ~2 ~

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]