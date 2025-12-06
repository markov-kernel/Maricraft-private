# Maricraft: Mob Spawner
# Gives a monster spawner block
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s mob_spawner 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]