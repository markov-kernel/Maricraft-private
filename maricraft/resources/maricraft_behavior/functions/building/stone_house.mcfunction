# Maricraft: Stone House (Bedrock Edition)
# Builds a small stone house instantly
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~2 ~ ~2 ~8 ~4 ~8 stone hollow
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~2 ~5 ~2 ~8 ~5 ~8 stone_bricks
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~5 ~ ~2 wooden_door ["minecraft:cardinal_direction"="north","upper_block_bit"=false,"open_bit"=false,"door_hinge_bit"=false]
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~5 ~1 ~2 wooden_door ["minecraft:cardinal_direction"="north","upper_block_bit"=true,"open_bit"=false,"door_hinge_bit"=false]
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~3 ~1 ~8 ~4 ~2 ~8 glass
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~6 ~1 ~8 ~7 ~2 ~8 glass

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]