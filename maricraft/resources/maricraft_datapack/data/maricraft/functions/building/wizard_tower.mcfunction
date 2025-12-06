# Maricraft: Wizard Tower (Bedrock Edition)
# Builds a mystical wizard tower with enchanting room

# Base foundation (deepslate)
fill ~5 ~-1 ~5 ~15 ~-1 ~15 deepslate_bricks

# Tower base - Level 1-5 (stone bricks, roughly circular)
fill ~7 ~ ~6 ~13 ~5 ~14 stone_bricks hollow
fill ~6 ~ ~7 ~14 ~5 ~13 stone_bricks hollow

# Tower middle - Level 6-15 (deepslate bricks)
fill ~7 ~6 ~6 ~13 ~15 ~14 deepslate_bricks hollow
fill ~6 ~6 ~7 ~14 ~15 ~13 deepslate_bricks hollow

# Tower top - Level 16-20 (polished deepslate)
fill ~7 ~16 ~6 ~13 ~20 ~14 polished_deepslate hollow
fill ~6 ~16 ~7 ~14 ~20 ~13 polished_deepslate hollow

# Entrance doorway
fill ~10 ~ ~6 ~10 ~3 ~6 air
setblock ~10 ~ ~6 oak_door

# Spiral staircase (inside tower)
setblock ~8 ~1 ~8 oak_stairs
setblock ~9 ~2 ~8 oak_stairs
setblock ~10 ~3 ~9 oak_stairs
setblock ~11 ~4 ~10 oak_stairs
setblock ~11 ~5 ~11 oak_stairs
setblock ~10 ~6 ~12 oak_stairs
setblock ~9 ~7 ~12 oak_stairs
setblock ~8 ~8 ~11 oak_stairs
setblock ~8 ~9 ~10 oak_stairs
setblock ~9 ~10 ~9 oak_stairs
setblock ~10 ~11 ~9 oak_stairs
setblock ~11 ~12 ~10 oak_stairs
setblock ~11 ~13 ~11 oak_stairs
setblock ~10 ~14 ~12 oak_stairs
setblock ~9 ~15 ~11 oak_stairs

# Purple stained glass windows (spiral pattern)
setblock ~7 ~3 ~10 purple_stained_glass
setblock ~13 ~5 ~10 purple_stained_glass
setblock ~10 ~7 ~6 purple_stained_glass
setblock ~10 ~9 ~14 purple_stained_glass
setblock ~7 ~11 ~10 purple_stained_glass
setblock ~13 ~13 ~10 purple_stained_glass
setblock ~10 ~15 ~6 purple_stained_glass
setblock ~10 ~17 ~14 purple_stained_glass

# Enchanting room floor (Level 16)
fill ~8 ~16 ~8 ~12 ~16 ~12 oak_planks

# Enchanting table in center
setblock ~10 ~17 ~10 enchant_table

# Bookshelves around enchanting table
fill ~8 ~17 ~8 ~8 ~19 ~12 bookshelf
fill ~12 ~17 ~8 ~12 ~19 ~12 bookshelf
fill ~9 ~17 ~8 ~11 ~19 ~8 bookshelf
fill ~9 ~17 ~12 ~11 ~19 ~12 bookshelf

# Glowstone lighting
setblock ~9 ~19 ~9 glowstone
setblock ~11 ~19 ~9 glowstone
setblock ~9 ~19 ~11 glowstone
setblock ~11 ~19 ~11 glowstone

# Pointed roof (purple terracotta)
fill ~6 ~21 ~6 ~14 ~21 ~14 purple_terracotta
fill ~7 ~22 ~7 ~13 ~22 ~13 purple_terracotta
fill ~8 ~23 ~8 ~12 ~23 ~12 purple_terracotta
fill ~9 ~24 ~9 ~11 ~24 ~11 purple_terracotta
setblock ~10 ~25 ~10 purple_terracotta

# Lightning rod on top
setblock ~10 ~26 ~10 lightning_rod

# Brewing stands and cauldrons
setblock ~8 ~17 ~10 brewing_stand
setblock ~12 ~17 ~10 cauldron

# Carpet decoration
setblock ~9 ~17 ~10 purple_carpet
setblock ~11 ~17 ~10 purple_carpet

# Lanterns
setblock ~10 ~4 ~7 lantern
setblock ~10 ~10 ~7 lantern

say Wizard Tower complete! Magic awaits within!
