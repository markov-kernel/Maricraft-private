# Maricraft: Rainbow Sheep
# Spawns a magical color-changing sheep!
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon sheep ~ ~ ~ minecraft:entity_born "jeb_"

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]