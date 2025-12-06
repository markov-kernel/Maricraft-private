# Maricraft: Dolphin
# Spawns a friendly dolphin (needs water!)
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ summon dolphin ~ ~ ~

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]