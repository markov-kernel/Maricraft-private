# Maricraft: Lava Moat
# Digs a moat around the player and fills with lava
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-6 ~-2 ~-6 ~6 ~-1 ~-5 lava
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-6 ~-2 ~5 ~6 ~-1 ~6 lava
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-6 ~-2 ~-4 ~-5 ~-1 ~4 lava
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~5 ~-2 ~-4 ~6 ~-1 ~4 lava

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]