# Maricraft: Wizard Tower (Bedrock Edition)
# Builds an elaborate mystical wizard tower with enchanting room, observatory, and secret chambers

# ============================================
# ITERATION 1: EXPANDED BASE & EXTERIOR
# ============================================

# Clear area for construction
fill ~3 ~-2 ~3 ~17 ~30 ~17 air

# Extended foundation platform (larger base)
fill ~3 ~-2 ~3 ~17 ~-2 ~17 cobblestone
fill ~4 ~-1 ~4 ~16 ~-1 ~16 deepslate_bricks

# Decorative border around foundation
fill ~3 ~-1 ~3 ~17 ~-1 ~3 polished_blackstone
fill ~3 ~-1 ~17 ~17 ~-1 ~17 polished_blackstone
fill ~3 ~-1 ~4 ~3 ~-1 ~16 polished_blackstone
fill ~17 ~-1 ~4 ~17 ~-1 ~16 polished_blackstone

# Corner pillars at base
fill ~3 ~ ~3 ~3 ~2 ~3 polished_blackstone
fill ~17 ~ ~3 ~17 ~2 ~3 polished_blackstone
fill ~3 ~ ~17 ~3 ~2 ~17 polished_blackstone
fill ~17 ~ ~17 ~17 ~2 ~17 polished_blackstone

# Exterior buttresses (support columns)
fill ~5 ~ ~5 ~5 ~4 ~5 stone_bricks
fill ~15 ~ ~5 ~15 ~4 ~5 stone_bricks
fill ~5 ~ ~15 ~5 ~4 ~15 stone_bricks
fill ~15 ~ ~15 ~15 ~4 ~15 stone_bricks

# Stone path leading to entrance
fill ~10 ~-1 ~0 ~10 ~-1 ~5 cobblestone
fill ~9 ~-1 ~1 ~11 ~-1 ~4 stone_bricks

# Garden plots on corners
fill ~3 ~-1 ~4 ~4 ~-1 ~5 grass_block
fill ~16 ~-1 ~4 ~17 ~-1 ~5 grass_block
fill ~3 ~-1 ~15 ~4 ~-1 ~16 grass_block
fill ~16 ~-1 ~15 ~17 ~-1 ~16 grass_block

# Flowers in garden
setblock ~3 ~ ~4 red_flower
setblock ~4 ~ ~5 yellow_flower
setblock ~16 ~ ~4 red_flower
setblock ~17 ~ ~5 yellow_flower
setblock ~3 ~ ~15 red_flower
setblock ~4 ~ ~16 yellow_flower
setblock ~16 ~ ~15 red_flower
setblock ~17 ~ ~16 yellow_flower

# Fence posts around perimeter
setblock ~3 ~3 ~3 oak_fence
setblock ~17 ~3 ~3 oak_fence
setblock ~3 ~3 ~17 oak_fence
setblock ~17 ~3 ~17 oak_fence

# Exterior torches
setblock ~5 ~5 ~5 torch
setblock ~15 ~5 ~5 torch
setblock ~5 ~5 ~15 torch
setblock ~15 ~5 ~15 torch
setblock ~10 ~ ~1 torch
setblock ~9 ~ ~3 torch
setblock ~11 ~ ~3 torch

# Original base foundation (deepslate)
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

# ============================================
# ITERATION 2: ENHANCED GROUND FLOOR INTERIOR
# ============================================

# Ground floor flooring (different material sections)
fill ~7 ~ ~7 ~13 ~ ~13 oak_planks
fill ~8 ~ ~8 ~12 ~ ~12 spruce_planks

# Potion storage area (left side)
setblock ~7 ~1 ~8 brewing_stand
setblock ~7 ~1 ~9 brewing_stand
setblock ~7 ~1 ~10 cauldron
setblock ~7 ~1 ~11 cauldron
setblock ~7 ~1 ~12 chest

# Ingredient shelf (bookshelves as storage)
fill ~7 ~2 ~8 ~7 ~3 ~12 bookshelf

# Carpet runner down the middle
fill ~9 ~ ~7 ~11 ~ ~7 purple_carpet
fill ~10 ~ ~8 ~10 ~ ~13 purple_carpet

# Work desk area (right side)
setblock ~13 ~1 ~8 crafting_table
setblock ~13 ~1 ~9 chest
setblock ~13 ~1 ~10 lectern
setblock ~13 ~1 ~11 chest

# Wall banners
setblock ~7 ~3 ~7 purple_banner
setblock ~13 ~3 ~7 purple_banner
setblock ~7 ~3 ~13 purple_banner
setblock ~13 ~3 ~13 purple_banner

# Ceiling lanterns on ground floor
setblock ~9 ~5 ~9 lantern
setblock ~11 ~5 ~9 lantern
setblock ~9 ~5 ~11 lantern
setblock ~11 ~5 ~11 lantern

# Decorative armor stand area
setblock ~8 ~ ~13 cobblestone
setblock ~12 ~ ~13 cobblestone

# Small rug by entrance
setblock ~10 ~ ~7 red_carpet
setblock ~9 ~ ~7 purple_carpet
setblock ~11 ~ ~7 purple_carpet

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

# ============================================
# ITERATION 7: LIBRARY & STUDY ROOM (Level 6-10)
# ============================================

# Library floor (level 6)
fill ~7 ~6 ~7 ~13 ~6 ~13 dark_oak_planks

# Central reading area floor
fill ~9 ~6 ~9 ~11 ~6 ~11 red_carpet

# Floor-to-ceiling bookshelves (walls)
fill ~7 ~7 ~7 ~7 ~10 ~13 bookshelf
fill ~13 ~7 ~7 ~13 ~10 ~13 bookshelf
fill ~8 ~7 ~7 ~12 ~10 ~7 bookshelf
fill ~8 ~7 ~13 ~12 ~10 ~13 bookshelf

# Reading nook with lecterns
setblock ~8 ~7 ~9 lectern
setblock ~8 ~7 ~11 lectern
setblock ~12 ~7 ~9 lectern
setblock ~12 ~7 ~11 lectern

# Cozy carpet seating area
setblock ~9 ~6 ~8 orange_carpet
setblock ~10 ~6 ~8 red_carpet
setblock ~11 ~6 ~8 orange_carpet
setblock ~9 ~6 ~12 orange_carpet
setblock ~10 ~6 ~12 red_carpet
setblock ~11 ~6 ~12 orange_carpet

# Spiral of floating candles
setblock ~8 ~8 ~8 candle
setblock ~9 ~9 ~9 candle
setblock ~10 ~10 ~10 candle
setblock ~11 ~9 ~11 candle
setblock ~12 ~8 ~12 candle

# Writing desk area
setblock ~10 ~7 ~7 dark_oak_planks
setblock ~10 ~7 ~8 crafting_table
setblock ~9 ~7 ~7 chest
setblock ~11 ~7 ~7 chest

# Decorative globe (carved pumpkin on fence)
setblock ~8 ~7 ~8 oak_fence
setblock ~8 ~8 ~8 carved_pumpkin

# Library chandelier
setblock ~10 ~10 ~10 chain
setblock ~10 ~9 ~10 lantern

# Reading lights
setblock ~8 ~10 ~10 soul_lantern
setblock ~12 ~10 ~10 soul_lantern

# Purple stained glass windows (spiral pattern)
setblock ~7 ~3 ~10 purple_stained_glass
setblock ~13 ~5 ~10 purple_stained_glass
setblock ~10 ~7 ~6 purple_stained_glass
setblock ~10 ~9 ~14 purple_stained_glass
setblock ~7 ~11 ~10 purple_stained_glass
setblock ~13 ~13 ~10 purple_stained_glass
setblock ~10 ~15 ~6 purple_stained_glass
setblock ~10 ~17 ~14 purple_stained_glass

# ============================================
# ITERATION 8: ALCHEMY LABORATORY (Level 11-15)
# ============================================

# Alchemy lab floor
fill ~7 ~11 ~7 ~13 ~11 ~13 polished_blackstone

# Bubbling cauldrons with magma underneath
setblock ~8 ~10 ~8 magma_block
setblock ~8 ~11 ~8 cauldron
setblock ~12 ~10 ~8 magma_block
setblock ~12 ~11 ~8 cauldron
setblock ~8 ~10 ~12 magma_block
setblock ~8 ~11 ~12 cauldron
setblock ~12 ~10 ~12 magma_block
setblock ~12 ~11 ~12 cauldron

# Central brewing station
setblock ~10 ~12 ~10 brewing_stand
setblock ~9 ~12 ~10 brewing_stand
setblock ~11 ~12 ~10 brewing_stand

# Ingredient storage barrels
setblock ~7 ~12 ~9 barrel
setblock ~7 ~12 ~10 barrel
setblock ~7 ~12 ~11 barrel
setblock ~13 ~12 ~9 barrel
setblock ~13 ~12 ~10 barrel
setblock ~13 ~12 ~11 barrel

# Glowing potion display (colored glass with light)
setblock ~9 ~13 ~7 lime_stained_glass
setblock ~10 ~13 ~7 red_stained_glass
setblock ~11 ~13 ~7 blue_stained_glass
setblock ~10 ~14 ~7 glowstone

# Alchemist's workbench
setblock ~10 ~12 ~13 crafting_table
setblock ~9 ~12 ~13 chest
setblock ~11 ~12 ~13 chest

# Smoke effect (cobwebs at ceiling)
setblock ~8 ~15 ~8 cobweb
setblock ~12 ~15 ~8 cobweb
setblock ~8 ~15 ~12 cobweb
setblock ~12 ~15 ~12 cobweb

# Lab lighting (soul lanterns for blue glow)
setblock ~9 ~14 ~9 soul_lantern
setblock ~11 ~14 ~9 soul_lantern
setblock ~9 ~14 ~11 soul_lantern
setblock ~11 ~14 ~11 soul_lantern

# Ingredient shelf
fill ~7 ~13 ~7 ~7 ~14 ~7 bookshelf
fill ~13 ~13 ~7 ~13 ~14 ~7 bookshelf

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

# ============================================
# ITERATION 3: OBSERVATORY LEVEL & WINDOWS
# ============================================

# Observatory level structure (Level 21-25)
fill ~7 ~21 ~6 ~13 ~25 ~14 polished_deepslate hollow
fill ~6 ~21 ~7 ~14 ~25 ~13 polished_deepslate hollow

# Observatory floor
fill ~8 ~21 ~8 ~12 ~21 ~12 spruce_planks

# Large observation windows (all sides)
fill ~7 ~22 ~9 ~7 ~24 ~11 glass
fill ~13 ~22 ~9 ~13 ~24 ~11 glass
fill ~9 ~22 ~6 ~11 ~24 ~6 glass
fill ~9 ~22 ~14 ~11 ~24 ~14 glass

# Telescope platform (center)
setblock ~10 ~22 ~10 polished_blackstone
setblock ~10 ~23 ~10 end_rod
setblock ~10 ~24 ~10 end_rod

# Star chart floor pattern (blue glass inlay)
setblock ~9 ~21 ~9 blue_stained_glass
setblock ~11 ~21 ~9 blue_stained_glass
setblock ~9 ~21 ~11 blue_stained_glass
setblock ~11 ~21 ~11 blue_stained_glass
setblock ~10 ~21 ~10 light_blue_stained_glass

# Balcony (front side)
fill ~8 ~21 ~5 ~12 ~21 ~5 spruce_planks
fill ~8 ~22 ~5 ~8 ~22 ~5 iron_bars
fill ~9 ~22 ~5 ~11 ~22 ~5 iron_bars
fill ~12 ~22 ~5 ~12 ~22 ~5 iron_bars

# Balcony corners
setblock ~8 ~22 ~6 iron_bars
setblock ~12 ~22 ~6 iron_bars

# More elaborate windows on tower body (spiral pattern enhanced)
setblock ~6 ~2 ~10 purple_stained_glass
setblock ~14 ~2 ~10 purple_stained_glass
setblock ~6 ~4 ~10 blue_stained_glass
setblock ~14 ~4 ~10 blue_stained_glass
setblock ~10 ~6 ~6 purple_stained_glass
setblock ~10 ~8 ~14 blue_stained_glass
setblock ~6 ~10 ~10 purple_stained_glass
setblock ~14 ~12 ~10 blue_stained_glass
setblock ~10 ~14 ~6 purple_stained_glass
setblock ~10 ~16 ~14 blue_stained_glass
setblock ~6 ~18 ~10 purple_stained_glass
setblock ~14 ~19 ~10 blue_stained_glass

# Window frames (stone brick accents)
setblock ~6 ~3 ~10 stone_bricks
setblock ~14 ~3 ~10 stone_bricks
setblock ~6 ~5 ~10 stone_bricks
setblock ~14 ~5 ~10 stone_bricks

# Observatory lighting
setblock ~8 ~24 ~8 glowstone
setblock ~12 ~24 ~8 glowstone
setblock ~8 ~24 ~12 glowstone
setblock ~12 ~24 ~12 glowstone

# ============================================
# ITERATION 4: MAGICAL EFFECTS & DECORATIONS
# ============================================

# Floating crystal display in enchanting room
setblock ~10 ~19 ~10 chain
setblock ~10 ~20 ~10 amethyst_block

# Crystal pillars in corners of enchanting room
setblock ~8 ~17 ~8 amethyst_block
setblock ~12 ~17 ~8 amethyst_block
setblock ~8 ~17 ~12 amethyst_block
setblock ~12 ~17 ~12 amethyst_block

# Soul lanterns for mystical blue lighting
setblock ~7 ~8 ~10 soul_lantern
setblock ~13 ~8 ~10 soul_lantern
setblock ~10 ~8 ~7 soul_lantern
setblock ~10 ~8 ~13 soul_lantern

# More soul lanterns on middle section
setblock ~7 ~13 ~10 soul_lantern
setblock ~13 ~13 ~10 soul_lantern

# Ender chest (magical storage) in enchanting room
setblock ~9 ~17 ~8 ender_chest

# Candles scattered throughout
setblock ~8 ~1 ~7 candle
setblock ~12 ~1 ~7 candle
setblock ~8 ~1 ~13 candle
setblock ~12 ~1 ~13 candle
setblock ~10 ~17 ~8 candle
setblock ~10 ~17 ~12 candle

# Cobwebs in upper corners (aged look)
setblock ~7 ~5 ~7 cobweb
setblock ~13 ~5 ~7 cobweb
setblock ~7 ~5 ~13 cobweb
setblock ~13 ~5 ~13 cobweb

# End rods as magical light pillars
setblock ~8 ~6 ~10 end_rod
setblock ~12 ~6 ~10 end_rod
setblock ~10 ~11 ~8 end_rod
setblock ~10 ~11 ~12 end_rod

# Skulls for mystical decoration
setblock ~7 ~2 ~10 skeleton_skull
setblock ~13 ~2 ~10 skeleton_skull

# Redstone lamps (can be powered)
setblock ~8 ~10 ~8 redstone_lamp
setblock ~12 ~10 ~8 redstone_lamp
setblock ~8 ~10 ~12 redstone_lamp
setblock ~12 ~10 ~12 redstone_lamp

# Chain decorations hanging from ceiling
setblock ~9 ~15 ~9 chain
setblock ~11 ~15 ~9 chain
setblock ~9 ~15 ~11 chain
setblock ~11 ~15 ~11 chain

# ============================================
# ITERATION 5: ELABORATE ROOF & CORNER SPIRES
# ============================================

# Main roof base layer (wider overhang)
fill ~5 ~26 ~5 ~15 ~26 ~15 purple_terracotta
fill ~6 ~26 ~6 ~14 ~26 ~14 magenta_terracotta

# Roof tier 2
fill ~6 ~27 ~6 ~14 ~27 ~14 purple_terracotta
fill ~7 ~27 ~7 ~13 ~27 ~13 magenta_terracotta

# Roof tier 3
fill ~7 ~28 ~7 ~13 ~28 ~13 purple_terracotta
fill ~8 ~28 ~8 ~12 ~28 ~12 magenta_terracotta

# Roof tier 4
fill ~8 ~29 ~8 ~12 ~29 ~12 purple_terracotta
fill ~9 ~29 ~9 ~11 ~29 ~11 magenta_terracotta

# Roof tier 5 (peak)
fill ~9 ~30 ~9 ~11 ~30 ~11 purple_terracotta
setblock ~10 ~31 ~10 purple_terracotta

# Corner spire 1 (front-left)
fill ~5 ~26 ~5 ~5 ~32 ~5 deepslate_bricks
setblock ~5 ~33 ~5 purple_terracotta
setblock ~5 ~34 ~5 lightning_rod

# Corner spire 2 (front-right)
fill ~15 ~26 ~5 ~15 ~32 ~5 deepslate_bricks
setblock ~15 ~33 ~5 purple_terracotta
setblock ~15 ~34 ~5 lightning_rod

# Corner spire 3 (back-left)
fill ~5 ~26 ~15 ~5 ~32 ~15 deepslate_bricks
setblock ~5 ~33 ~15 purple_terracotta
setblock ~5 ~34 ~15 lightning_rod

# Corner spire 4 (back-right)
fill ~15 ~26 ~15 ~15 ~32 ~15 deepslate_bricks
setblock ~15 ~33 ~15 purple_terracotta
setblock ~15 ~34 ~15 lightning_rod

# Main spire/weather vane
setblock ~10 ~32 ~10 chain
setblock ~10 ~33 ~10 chain
setblock ~10 ~34 ~10 lightning_rod

# Beacon at very top (inside main spire)
setblock ~10 ~30 ~10 beacon

# Hanging lanterns from eaves
setblock ~5 ~25 ~10 chain
setblock ~5 ~24 ~10 lantern
setblock ~15 ~25 ~10 chain
setblock ~15 ~24 ~10 lantern
setblock ~10 ~25 ~5 chain
setblock ~10 ~24 ~5 lantern
setblock ~10 ~25 ~15 chain
setblock ~10 ~24 ~15 lantern

# Copper accents on roof edges
setblock ~6 ~26 ~5 copper_block
setblock ~14 ~26 ~5 copper_block
setblock ~6 ~26 ~15 copper_block
setblock ~14 ~26 ~15 copper_block
setblock ~5 ~26 ~6 copper_block
setblock ~5 ~26 ~14 copper_block
setblock ~15 ~26 ~6 copper_block
setblock ~15 ~26 ~14 copper_block

# Gold trim on spire bases
setblock ~5 ~26 ~5 gold_block
setblock ~15 ~26 ~5 gold_block
setblock ~5 ~26 ~15 gold_block
setblock ~15 ~26 ~15 gold_block

# ============================================
# ITERATION 6: SECRET BASEMENT & FINAL POLISH
# ============================================

# Secret basement chamber (below foundation)
fill ~7 ~-6 ~7 ~13 ~-3 ~13 stone_bricks hollow
fill ~8 ~-5 ~8 ~12 ~-5 ~12 cobblestone

# Hidden trapdoor entrance (inside tower)
setblock ~10 ~ ~12 oak_trapdoor
fill ~10 ~-1 ~12 ~10 ~-2 ~12 ladder

# Secret treasure room floor
fill ~8 ~-5 ~8 ~12 ~-5 ~12 obsidian

# Treasure!
setblock ~10 ~-4 ~10 chest
setblock ~9 ~-4 ~9 gold_block
setblock ~11 ~-4 ~9 gold_block
setblock ~9 ~-4 ~11 diamond_block
setblock ~11 ~-4 ~11 emerald_block

# Glowing loot
setblock ~10 ~-4 ~8 glowstone
setblock ~10 ~-4 ~12 glowstone

# Mystical barrier wall at back
fill ~8 ~-4 ~13 ~12 ~-3 ~13 crying_obsidian

# Redstone lamp lighting in basement
setblock ~8 ~-3 ~8 redstone_lamp
setblock ~12 ~-3 ~8 redstone_lamp
setblock ~8 ~-3 ~12 redstone_lamp
setblock ~12 ~-3 ~12 redstone_lamp

# Spider webs in basement corners
setblock ~8 ~-4 ~8 cobweb
setblock ~12 ~-4 ~8 cobweb

# ============================================
# ITERATION 9: ARCANE PORTAL CHAMBER (Deep Basement)
# ============================================

# Expand basement deeper for portal chamber
fill ~6 ~-10 ~6 ~14 ~-7 ~14 stone_bricks hollow
fill ~7 ~-9 ~7 ~13 ~-9 ~13 obsidian

# Portal frame structure (nether portal style)
fill ~9 ~-8 ~10 ~11 ~-8 ~10 obsidian
fill ~9 ~-7 ~10 ~9 ~-5 ~10 obsidian
fill ~11 ~-7 ~10 ~11 ~-5 ~10 obsidian
fill ~9 ~-4 ~10 ~11 ~-4 ~10 obsidian

# Crying obsidian accents on portal
setblock ~9 ~-6 ~10 crying_obsidian
setblock ~11 ~-6 ~10 crying_obsidian

# Mystical symbols on floor (wool pattern)
setblock ~8 ~-9 ~8 purple_wool
setblock ~12 ~-9 ~8 purple_wool
setblock ~8 ~-9 ~12 purple_wool
setblock ~12 ~-9 ~12 purple_wool
setblock ~10 ~-9 ~8 blue_wool
setblock ~10 ~-9 ~12 blue_wool
setblock ~8 ~-9 ~10 blue_wool
setblock ~12 ~-9 ~10 blue_wool

# Floating rune stones (end rods + purple glass)
setblock ~7 ~-7 ~7 end_rod
setblock ~7 ~-6 ~7 purple_stained_glass
setblock ~13 ~-7 ~7 end_rod
setblock ~13 ~-6 ~7 purple_stained_glass
setblock ~7 ~-7 ~13 end_rod
setblock ~7 ~-6 ~13 purple_stained_glass
setblock ~13 ~-7 ~13 end_rod
setblock ~13 ~-6 ~13 purple_stained_glass

# Energy conduits (chains to ceiling)
setblock ~8 ~-7 ~10 chain
setblock ~8 ~-6 ~10 chain
setblock ~12 ~-7 ~10 chain
setblock ~12 ~-6 ~10 chain

# Soul fire ring around portal
setblock ~8 ~-8 ~9 soul_fire
setblock ~8 ~-8 ~11 soul_fire
setblock ~12 ~-8 ~9 soul_fire
setblock ~12 ~-8 ~11 soul_fire

# Nether-themed accent blocks
setblock ~7 ~-8 ~10 netherrack
setblock ~13 ~-8 ~10 netherrack
setblock ~10 ~-8 ~7 netherrack
setblock ~10 ~-8 ~13 netherrack

# Portal chamber lighting
setblock ~7 ~-7 ~10 soul_lantern
setblock ~13 ~-7 ~10 soul_lantern

# Ladder access from upper basement
fill ~10 ~-6 ~7 ~10 ~-3 ~7 ladder

# ============================================
# ITERATION 10: GREENHOUSE & GARDEN (East Side)
# ============================================

# Greenhouse foundation
fill ~18 ~-1 ~7 ~24 ~-1 ~13 stone_bricks
fill ~19 ~ ~8 ~23 ~ ~12 grass_block

# Glass walls and roof
fill ~18 ~ ~7 ~24 ~4 ~7 glass
fill ~18 ~ ~13 ~24 ~4 ~13 glass
fill ~24 ~ ~8 ~24 ~4 ~12 glass
fill ~18 ~5 ~7 ~24 ~5 ~13 glass

# Glass ceiling frame (wood)
fill ~18 ~4 ~7 ~24 ~4 ~7 oak_planks
fill ~18 ~4 ~13 ~24 ~4 ~13 oak_planks
fill ~24 ~4 ~8 ~24 ~4 ~12 oak_planks

# Entrance from tower
fill ~15 ~ ~10 ~17 ~2 ~10 air
setblock ~17 ~ ~10 oak_door

# Variety of plants
setblock ~19 ~1 ~8 red_flower
setblock ~20 ~1 ~8 yellow_flower
setblock ~21 ~1 ~8 red_flower
setblock ~22 ~1 ~8 yellow_flower
setblock ~23 ~1 ~8 red_flower

setblock ~19 ~1 ~12 red_flower
setblock ~20 ~1 ~12 yellow_flower
setblock ~21 ~1 ~12 red_flower
setblock ~22 ~1 ~12 yellow_flower
setblock ~23 ~1 ~12 red_flower

# Central water feature (fountain)
setblock ~21 ~ ~10 cobblestone
setblock ~21 ~1 ~10 water

# Bee hives
setblock ~19 ~2 ~9 bee_nest
setblock ~23 ~2 ~11 bee_nest

# Composters
setblock ~19 ~1 ~10 composter
setblock ~23 ~1 ~10 composter

# Potted plants on shelves
setblock ~20 ~1 ~9 oak_planks
setblock ~22 ~1 ~9 oak_planks
setblock ~20 ~1 ~11 oak_planks
setblock ~22 ~1 ~11 oak_planks

# Hanging vines from ceiling
setblock ~19 ~4 ~9 vine
setblock ~23 ~4 ~11 vine
setblock ~21 ~4 ~8 vine
setblock ~21 ~4 ~12 vine

# Lantern lighting
setblock ~20 ~3 ~10 lantern
setblock ~22 ~3 ~10 lantern

# Connecting path
fill ~16 ~-1 ~9 ~17 ~-1 ~11 cobblestone

# ============================================
# ITERATION 11: DEFENSIVE FEATURES
# ============================================

# Arrow slits in tower walls (narrow windows)
setblock ~6 ~7 ~10 air
setblock ~14 ~7 ~10 air
setblock ~10 ~7 ~6 air
setblock ~10 ~7 ~14 air

setblock ~6 ~12 ~10 air
setblock ~14 ~12 ~10 air
setblock ~10 ~12 ~6 air
setblock ~10 ~12 ~14 air

# Moat around the base
fill ~0 ~-2 ~0 ~20 ~-1 ~2 water
fill ~0 ~-2 ~18 ~20 ~-1 ~20 water
fill ~0 ~-2 ~3 ~2 ~-1 ~17 water
fill ~18 ~-2 ~3 ~20 ~-1 ~17 water

# Moat walls (stone)
fill ~0 ~-2 ~0 ~20 ~-2 ~0 stone_bricks
fill ~0 ~-2 ~20 ~20 ~-2 ~20 stone_bricks
fill ~0 ~-2 ~1 ~0 ~-2 ~19 stone_bricks
fill ~20 ~-2 ~1 ~20 ~-2 ~19 stone_bricks

# Bridge over moat (to entrance)
fill ~9 ~-1 ~0 ~11 ~-1 ~2 oak_planks
fill ~9 ~ ~0 ~9 ~ ~2 oak_fence
fill ~11 ~ ~0 ~11 ~ ~2 oak_fence

# Watchtower platform above observatory
fill ~8 ~35 ~8 ~12 ~35 ~12 oak_planks
fill ~8 ~36 ~8 ~8 ~36 ~12 oak_fence
fill ~12 ~36 ~8 ~12 ~36 ~12 oak_fence
fill ~9 ~36 ~8 ~11 ~36 ~8 oak_fence
fill ~9 ~36 ~12 ~11 ~36 ~12 oak_fence

# Signal fire pit on watchtower
setblock ~10 ~36 ~10 netherrack
setblock ~10 ~37 ~10 fire

# Iron golem summoning circle
setblock ~2 ~-1 ~10 iron_block
setblock ~2 ~ ~10 iron_block
setblock ~2 ~1 ~10 iron_block
setblock ~1 ~1 ~10 iron_block
setblock ~3 ~1 ~10 iron_block
setblock ~2 ~2 ~10 carved_pumpkin

# Defensive dispenser (hidden)
setblock ~6 ~1 ~6 dispenser
setblock ~14 ~1 ~6 dispenser

# Warning bells at entrance
setblock ~8 ~3 ~5 bell
setblock ~12 ~3 ~5 bell

# Guard torches along moat
setblock ~5 ~ ~1 torch
setblock ~15 ~ ~1 torch
setblock ~5 ~ ~19 torch
setblock ~15 ~ ~19 torch

# ============================================
# ITERATION 12: GRAND ENTRANCE & FINAL FLOURISHES
# ============================================

# Expanded entrance hall columns
fill ~8 ~ ~4 ~8 ~4 ~4 stone_bricks
fill ~12 ~ ~4 ~12 ~4 ~4 stone_bricks
setblock ~8 ~5 ~4 chiseled_stone_bricks
setblock ~12 ~5 ~4 chiseled_stone_bricks

# Magical doorway arch
fill ~9 ~4 ~5 ~11 ~4 ~5 purple_terracotta
setblock ~10 ~5 ~5 end_rod

# Runes on arch (purple glass)
setblock ~9 ~3 ~5 purple_stained_glass
setblock ~11 ~3 ~5 purple_stained_glass

# Welcome mat pattern
setblock ~10 ~ ~5 purple_carpet
setblock ~9 ~ ~5 black_carpet
setblock ~11 ~ ~5 black_carpet

# Trophy displays outside entrance
setblock ~7 ~1 ~4 oak_planks
setblock ~7 ~2 ~4 dragon_egg
setblock ~13 ~1 ~4 oak_planks
setblock ~13 ~2 ~4 beacon

# Floating orbs of light throughout tower
setblock ~7 ~4 ~10 end_rod
setblock ~13 ~4 ~10 end_rod
setblock ~10 ~4 ~7 end_rod
setblock ~10 ~4 ~13 end_rod

# More floating orbs on higher levels
setblock ~7 ~9 ~10 end_rod
setblock ~13 ~9 ~10 end_rod
setblock ~7 ~14 ~10 end_rod
setblock ~13 ~14 ~10 end_rod
setblock ~7 ~19 ~10 end_rod
setblock ~13 ~19 ~10 end_rod

# Crystal chandelier in observatory
setblock ~10 ~24 ~10 chain
setblock ~10 ~23 ~10 amethyst_block
setblock ~9 ~23 ~10 chain
setblock ~11 ~23 ~10 chain
setblock ~10 ~23 ~9 chain
setblock ~10 ~23 ~11 chain

# Final roof decorations
setblock ~7 ~26 ~7 soul_lantern
setblock ~13 ~26 ~7 soul_lantern
setblock ~7 ~26 ~13 soul_lantern
setblock ~13 ~26 ~13 soul_lantern

# Banner flags on spires
setblock ~5 ~35 ~5 purple_banner
setblock ~15 ~35 ~5 purple_banner
setblock ~5 ~35 ~15 purple_banner
setblock ~15 ~35 ~15 purple_banner

# Enchanted glow around beacon top
setblock ~9 ~31 ~10 glowstone
setblock ~11 ~31 ~10 glowstone
setblock ~10 ~31 ~9 glowstone
setblock ~10 ~31 ~11 glowstone

# Gold accents on entrance
setblock ~8 ~ ~4 gold_block
setblock ~12 ~ ~4 gold_block

# Final polish - fence details on corners
setblock ~6 ~6 ~6 oak_fence
setblock ~14 ~6 ~6 oak_fence
setblock ~6 ~6 ~14 oak_fence
setblock ~14 ~6 ~14 oak_fence

# Final architectural polish - exterior wall details
fill ~6 ~3 ~6 ~6 ~3 ~6 chiseled_stone_bricks
fill ~14 ~3 ~6 ~14 ~3 ~6 chiseled_stone_bricks
fill ~6 ~3 ~14 ~6 ~3 ~14 chiseled_stone_bricks
fill ~14 ~3 ~14 ~14 ~3 ~14 chiseled_stone_bricks

# Tower rings (decorative bands)
fill ~6 ~10 ~6 ~14 ~10 ~6 deepslate_tiles
fill ~6 ~10 ~14 ~14 ~10 ~14 deepslate_tiles
fill ~6 ~10 ~7 ~6 ~10 ~13 deepslate_tiles
fill ~14 ~10 ~7 ~14 ~10 ~13 deepslate_tiles

# Second decorative ring
fill ~6 ~15 ~6 ~14 ~15 ~6 deepslate_tiles
fill ~6 ~15 ~14 ~14 ~15 ~14 deepslate_tiles
fill ~6 ~15 ~7 ~6 ~15 ~13 deepslate_tiles
fill ~14 ~15 ~7 ~14 ~15 ~13 deepslate_tiles

# Flying buttress arches
setblock ~4 ~8 ~10 stone_brick_stairs
setblock ~16 ~8 ~10 stone_brick_stairs
setblock ~10 ~8 ~4 stone_brick_stairs
setblock ~10 ~8 ~16 stone_brick_stairs

# Final torch placement for ambiance
setblock ~4 ~9 ~10 torch
setblock ~16 ~9 ~10 torch
setblock ~10 ~9 ~4 torch
setblock ~10 ~9 ~16 torch

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
