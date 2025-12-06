# Maricraft: Dragon Nest (Bedrock Edition)
# Builds an epic dragon nest with treasure and dragon egg

# Create crater shape (dig down)
fill ~-10 ~-1 ~-10 ~10 ~4 ~10 air

# Outer rim (blackstone)
fill ~-10 ~ ~-10 ~10 ~2 ~-10 polished_blackstone
fill ~-10 ~ ~10 ~10 ~2 ~10 polished_blackstone
fill ~-10 ~ ~-9 ~-10 ~2 ~9 polished_blackstone
fill ~10 ~ ~-9 ~10 ~2 ~9 polished_blackstone

# Second rim layer (gilded blackstone)
fill ~-9 ~-1 ~-9 ~9 ~1 ~-9 gilded_blackstone
fill ~-9 ~-1 ~9 ~9 ~1 ~9 gilded_blackstone
fill ~-9 ~-1 ~-8 ~-9 ~1 ~8 gilded_blackstone
fill ~9 ~-1 ~-8 ~9 ~1 ~8 gilded_blackstone

# Crater floor (obsidian)
fill ~-8 ~-2 ~-8 ~8 ~-2 ~8 obsidian
fill ~-6 ~-3 ~-6 ~6 ~-3 ~6 obsidian
fill ~-4 ~-4 ~-4 ~4 ~-4 ~4 crying_obsidian

# End stone accents
fill ~-8 ~-2 ~-8 ~-6 ~-2 ~-6 end_stone
fill ~6 ~-2 ~-8 ~8 ~-2 ~-6 end_stone
fill ~-8 ~-2 ~6 ~-6 ~-2 ~8 end_stone
fill ~6 ~-2 ~6 ~8 ~-2 ~8 end_stone

# Center pedestal for dragon egg
fill ~-1 ~-3 ~-1 ~1 ~-1 ~1 obsidian
setblock ~0 ~-2 ~0 crying_obsidian
setblock ~0 ~-1 ~0 obsidian
setblock ~0 ~ ~0 dragon_egg

# Gold treasure scattered around
setblock ~-3 ~-3 ~-2 gold_block
setblock ~3 ~-3 ~-2 gold_block
setblock ~-2 ~-3 ~3 gold_block
setblock ~2 ~-3 ~3 gold_block
setblock ~-4 ~-3 ~0 gold_block
setblock ~4 ~-3 ~0 gold_block

# Treasure chests
setblock ~-5 ~-2 ~-5 chest
setblock ~5 ~-2 ~-5 chest
setblock ~-5 ~-2 ~5 chest
setblock ~5 ~-2 ~5 chest

# Diamond blocks (rare treasure)
setblock ~0 ~-3 ~-3 diamond_block
setblock ~0 ~-3 ~3 diamond_block

# Soul fire torches (purple glow effect)
setblock ~-3 ~-1 ~-3 soul_lantern
setblock ~3 ~-1 ~-3 soul_lantern
setblock ~-3 ~-1 ~3 soul_lantern
setblock ~3 ~-1 ~3 soul_lantern

# End rods (crystal effect)
setblock ~-2 ~-1 ~0 end_rod
setblock ~2 ~-1 ~0 end_rod
setblock ~0 ~-1 ~-2 end_rod
setblock ~0 ~-1 ~2 end_rod

# Purple glass decorations (mystical)
setblock ~-6 ~ ~0 purple_stained_glass
setblock ~6 ~ ~0 purple_stained_glass
setblock ~0 ~ ~-6 purple_stained_glass
setblock ~0 ~ ~6 purple_stained_glass

# Dramatic spikes around rim
setblock ~-10 ~3 ~0 pointed_dripstone
setblock ~10 ~3 ~0 pointed_dripstone
setblock ~0 ~3 ~-10 pointed_dripstone
setblock ~0 ~3 ~10 pointed_dripstone

# Corner pillars (obsidian towers)
fill ~-10 ~ ~-10 ~-10 ~6 ~-10 obsidian
fill ~10 ~ ~-10 ~10 ~6 ~-10 obsidian
fill ~-10 ~ ~10 ~-10 ~6 ~10 obsidian
fill ~10 ~ ~10 ~10 ~6 ~10 obsidian

# Fire on pillars
setblock ~-10 ~7 ~-10 soul_fire
setblock ~10 ~7 ~-10 soul_fire
setblock ~-10 ~7 ~10 soul_fire
setblock ~10 ~7 ~10 soul_fire

# Chains hanging
setblock ~-5 ~1 ~-5 chain
setblock ~-5 ~ ~-5 chain
setblock ~5 ~1 ~-5 chain
setblock ~5 ~ ~-5 chain

# Magma blocks for danger
setblock ~-7 ~-2 ~0 magma_block
setblock ~7 ~-2 ~0 magma_block
setblock ~0 ~-2 ~-7 magma_block
setblock ~0 ~-2 ~7 magma_block

say Dragon Nest complete! The dragon's treasure is yours... if you dare!
