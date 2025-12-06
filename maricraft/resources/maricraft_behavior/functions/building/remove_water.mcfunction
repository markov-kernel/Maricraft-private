# Maricraft: Remove Water
# Drains all water in a 20-block radius
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-10 ~-5 ~-10 ~10 ~5 ~10 air replace water

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]