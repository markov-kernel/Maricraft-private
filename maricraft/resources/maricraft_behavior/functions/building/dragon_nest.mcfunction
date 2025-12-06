# Maricraft: Dragon Nest (Bedrock Edition)
# Builds an epic dragon nest with treasure and dragon egg

# Create crater shape (dig down)
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-10 ~-1 ~-10 ~10 ~4 ~10 air

# Outer rim (blackstone)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-10 ~ ~-10 ~10 ~2 ~-10 polished_blackstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-10 ~ ~10 ~10 ~2 ~10 polished_blackstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-10 ~ ~-9 ~-10 ~2 ~9 polished_blackstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~10 ~ ~-9 ~10 ~2 ~9 polished_blackstone

# Second rim layer (gilded blackstone)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-9 ~-1 ~-9 ~9 ~1 ~-9 gilded_blackstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-9 ~-1 ~9 ~9 ~1 ~9 gilded_blackstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-9 ~-1 ~-8 ~-9 ~1 ~8 gilded_blackstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~9 ~-1 ~-8 ~9 ~1 ~8 gilded_blackstone

# Crater floor (obsidian)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-8 ~-2 ~-8 ~8 ~-2 ~8 obsidian
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-6 ~-3 ~-6 ~6 ~-3 ~6 obsidian
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-4 ~-4 ~-4 ~4 ~-4 ~4 crying_obsidian

# End stone accents
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-8 ~-2 ~-8 ~-6 ~-2 ~-6 end_stone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~6 ~-2 ~-8 ~8 ~-2 ~-6 end_stone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-8 ~-2 ~6 ~-6 ~-2 ~8 end_stone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~6 ~-2 ~6 ~8 ~-2 ~8 end_stone

# Center pedestal for dragon egg
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-1 ~-3 ~-1 ~1 ~-1 ~1 obsidian
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-2 ~0 crying_obsidian
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-1 ~0 obsidian
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~ ~0 dragon_egg

# Gold treasure scattered around
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-3 ~-3 ~-2 gold_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~3 ~-3 ~-2 gold_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-2 ~-3 ~3 gold_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~2 ~-3 ~3 gold_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-4 ~-3 ~0 gold_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~4 ~-3 ~0 gold_block

# Treasure chests
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-5 ~-2 ~-5 chest
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~5 ~-2 ~-5 chest
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-5 ~-2 ~5 chest
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~5 ~-2 ~5 chest

# Diamond blocks (rare treasure)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-3 ~-3 diamond_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-3 ~3 diamond_block

# Soul fire torches (purple glow effect)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-3 ~-1 ~-3 soul_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~3 ~-1 ~-3 soul_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-3 ~-1 ~3 soul_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~3 ~-1 ~3 soul_lantern

# End rods (crystal effect)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-2 ~-1 ~0 end_rod
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~2 ~-1 ~0 end_rod
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-1 ~-2 end_rod
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-1 ~2 end_rod

# Purple glass decorations (mystical)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-6 ~ ~0 purple_stained_glass
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~6 ~ ~0 purple_stained_glass
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~ ~-6 purple_stained_glass
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~ ~6 purple_stained_glass

# Dramatic spikes around rim
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-10 ~3 ~0 pointed_dripstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~10 ~3 ~0 pointed_dripstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~3 ~-10 pointed_dripstone
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~3 ~10 pointed_dripstone

# Corner pillars (obsidian towers)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-10 ~ ~-10 ~-10 ~6 ~-10 obsidian
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~10 ~ ~-10 ~10 ~6 ~-10 obsidian
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-10 ~ ~10 ~-10 ~6 ~10 obsidian
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~10 ~ ~10 ~10 ~6 ~10 obsidian

# Fire on pillars
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-10 ~7 ~-10 soul_fire
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~10 ~7 ~-10 soul_fire
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-10 ~7 ~10 soul_fire
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~10 ~7 ~10 soul_fire

# Chains hanging
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-5 ~1 ~-5 chain
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-5 ~ ~-5 chain
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~5 ~1 ~-5 chain
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~5 ~ ~-5 chain

# Magma blocks for danger
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-7 ~-2 ~0 magma
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~7 ~-2 ~0 magma
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-2 ~-7 magma
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-2 ~7 magma

say Dragon Nest complete! The dragon's treasure is yours... if you dare!

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]