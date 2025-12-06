# Maricraft: Kill Hostiles
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

kill @e[type=zombie,r=100]
kill @e[type=skeleton,r=100]
kill @e[type=creeper,r=100]
kill @e[type=spider,r=100]
kill @e[type=enderman,r=100]
kill @e[type=witch,r=100]

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]