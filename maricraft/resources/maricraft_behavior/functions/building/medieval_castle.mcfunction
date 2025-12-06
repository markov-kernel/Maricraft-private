# Maricraft: Medieval Castle (Bedrock Edition)
# Builds an elaborate castle with walls, towers, and courtyard

# Clear the area first
fill ~2 ~ ~2 ~22 ~15 ~22 air

# Main outer walls (stone brick, 20x20 base, 8 blocks high)
fill ~2 ~ ~2 ~22 ~8 ~2 stone_bricks hollow
fill ~2 ~ ~22 ~22 ~8 ~22 stone_bricks hollow
fill ~2 ~ ~2 ~2 ~8 ~22 stone_bricks hollow
fill ~22 ~ ~2 ~22 ~8 ~22 stone_bricks hollow

# Corner tower 1 (front-left) - taller
fill ~2 ~ ~2 ~5 ~12 ~5 stone_bricks hollow
fill ~2 ~12 ~2 ~5 ~12 ~5 deepslate_bricks
fill ~3 ~13 ~3 ~4 ~13 ~4 stone_brick_stairs

# Corner tower 2 (front-right)
fill ~19 ~ ~2 ~22 ~12 ~5 stone_bricks hollow
fill ~19 ~12 ~2 ~22 ~12 ~5 deepslate_bricks
fill ~20 ~13 ~3 ~21 ~13 ~4 stone_brick_stairs

# Corner tower 3 (back-left)
fill ~2 ~ ~19 ~5 ~12 ~22 stone_bricks hollow
fill ~2 ~12 ~19 ~5 ~12 ~22 deepslate_bricks
fill ~3 ~13 ~20 ~4 ~13 ~21 stone_brick_stairs

# Corner tower 4 (back-right)
fill ~19 ~ ~19 ~22 ~12 ~22 stone_bricks hollow
fill ~19 ~12 ~19 ~22 ~12 ~22 deepslate_bricks
fill ~20 ~13 ~20 ~21 ~13 ~21 stone_brick_stairs

# Crenellations on walls (battlements)
fill ~6 ~8 ~2 ~7 ~9 ~2 stone_bricks
fill ~9 ~8 ~2 ~10 ~9 ~2 stone_bricks
fill ~12 ~8 ~2 ~13 ~9 ~2 stone_bricks
fill ~15 ~8 ~2 ~16 ~9 ~2 stone_bricks

# Main gate entrance (front wall)
fill ~11 ~ ~2 ~13 ~5 ~2 air
setblock ~11 ~ ~2 iron_door
setblock ~13 ~ ~2 iron_door

# Gate arch decoration
fill ~10 ~5 ~2 ~14 ~6 ~2 chiseled_stone_bricks

# Courtyard floor (cobblestone)
fill ~6 ~-1 ~6 ~18 ~-1 ~18 cobblestone

# Central keep (smaller building inside)
fill ~9 ~ ~9 ~15 ~6 ~15 stone_bricks hollow
fill ~9 ~6 ~9 ~15 ~7 ~15 oak_planks

# Keep entrance
fill ~12 ~ ~9 ~12 ~3 ~9 air
setblock ~12 ~ ~9 oak_door

# Keep windows
fill ~9 ~2 ~11 ~9 ~3 ~13 glass
fill ~15 ~2 ~11 ~15 ~3 ~13 glass

# Torches for lighting
setblock ~4 ~4 ~4 torch
setblock ~20 ~4 ~4 torch
setblock ~4 ~4 ~20 torch
setblock ~20 ~4 ~20 torch
setblock ~12 ~4 ~12 lantern

# Banner flags on towers
setblock ~3 ~14 ~3 white_banner
setblock ~20 ~14 ~3 white_banner
setblock ~3 ~14 ~20 white_banner
setblock ~20 ~14 ~20 white_banner

# Moat around castle (water)
fill ~0 ~-2 ~0 ~24 ~-1 ~1 water
fill ~0 ~-2 ~23 ~24 ~-1 ~24 water
fill ~0 ~-2 ~2 ~1 ~-1 ~22 water
fill ~23 ~-2 ~2 ~24 ~-1 ~22 water

say Medieval Castle complete! Your fortress awaits!
