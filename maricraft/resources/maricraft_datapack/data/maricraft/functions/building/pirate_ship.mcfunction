# Maricraft: Pirate Ship (Bedrock Edition)
# Builds a full pirate ship with sails and treasure

# Hull bottom (dark oak, boat shape)
fill ~5 ~ ~2 ~15 ~ ~18 dark_oak_planks
fill ~6 ~-1 ~4 ~14 ~-1 ~16 dark_oak_planks
fill ~7 ~-2 ~6 ~13 ~-2 ~14 dark_oak_planks

# Hull sides (curved bow and stern)
fill ~5 ~1 ~2 ~5 ~3 ~18 dark_oak_planks
fill ~15 ~1 ~2 ~15 ~3 ~18 dark_oak_planks

# Bow (front, pointed)
fill ~6 ~1 ~1 ~14 ~3 ~1 dark_oak_planks
fill ~7 ~1 ~0 ~13 ~2 ~0 dark_oak_planks
fill ~9 ~1 ~-1 ~11 ~1 ~-1 dark_oak_planks

# Stern (back, raised)
fill ~6 ~1 ~19 ~14 ~5 ~19 dark_oak_planks
fill ~6 ~1 ~20 ~14 ~5 ~20 dark_oak_planks

# Main deck
fill ~6 ~3 ~3 ~14 ~3 ~18 oak_planks

# Captain's cabin (stern)
fill ~7 ~4 ~15 ~13 ~7 ~19 oak_planks hollow
fill ~9 ~4 ~15 ~11 ~6 ~15 air
setblock ~10 ~4 ~15 oak_door
fill ~8 ~5 ~19 ~12 ~6 ~19 glass

# Cabin roof
fill ~7 ~7 ~15 ~13 ~7 ~19 spruce_planks

# Main mast (center)
fill ~10 ~4 ~10 ~10 ~18 ~10 oak_log

# Crow's nest
fill ~8 ~16 ~8 ~12 ~16 ~12 oak_planks hollow
fill ~9 ~16 ~9 ~11 ~16 ~11 air
fill ~8 ~17 ~8 ~8 ~17 ~12 oak_fence
fill ~12 ~17 ~8 ~12 ~17 ~12 oak_fence
fill ~9 ~17 ~8 ~11 ~17 ~8 oak_fence
fill ~9 ~17 ~12 ~11 ~17 ~12 oak_fence

# Main sail (white wool)
fill ~6 ~8 ~10 ~9 ~15 ~10 white_wool
fill ~11 ~8 ~10 ~14 ~15 ~10 white_wool

# Secondary mast (front)
fill ~10 ~4 ~5 ~10 ~12 ~5 oak_log

# Front sail
fill ~7 ~6 ~5 ~13 ~11 ~5 white_wool

# Plank (walking the plank!)
fill ~16 ~3 ~10 ~20 ~3 ~10 oak_planks

# Treasure chests
setblock ~8 ~4 ~17 chest
setblock ~12 ~4 ~17 chest

# Lanterns
setblock ~7 ~5 ~5 lantern
setblock ~13 ~5 ~5 lantern
setblock ~7 ~5 ~15 lantern
setblock ~13 ~5 ~15 lantern

# Ship wheel (at stern)
setblock ~10 ~5 ~18 oak_fence

# Cannons (fence + black wool)
setblock ~5 ~2 ~8 black_wool
setblock ~5 ~2 ~12 black_wool
setblock ~15 ~2 ~8 black_wool
setblock ~15 ~2 ~12 black_wool

# Anchor chain
setblock ~5 ~1 ~3 chain
setblock ~5 ~0 ~3 chain
setblock ~5 ~-1 ~3 chain

# Pirate flag on main mast
setblock ~10 ~19 ~10 black_banner

# Railing
fill ~6 ~4 ~3 ~14 ~4 ~3 oak_fence
fill ~6 ~4 ~14 ~14 ~4 ~14 oak_fence

say Pirate Ship complete! Arrr, set sail for adventure!
