# Maricraft: Underwater Dome (Bedrock Edition)
# Builds a glass dome base - perfect for underwater!

# Clear area for dome
fill ~-8 ~-1 ~-8 ~8 ~10 ~8 air

# Floor (prismarine)
fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 prismarine
fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 prismarine_bricks
fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 dark_prismarine

# Dome layer 1 (base, r=7)
fill ~-7 ~ ~-7 ~7 ~ ~7 glass hollow
fill ~-7 ~1 ~-7 ~7 ~1 ~7 glass hollow

# Dome layer 2 (r=6)
fill ~-6 ~2 ~-6 ~6 ~2 ~6 glass hollow
fill ~-6 ~3 ~-6 ~6 ~3 ~6 glass hollow

# Dome layer 3 (r=5)
fill ~-5 ~4 ~-5 ~5 ~4 ~5 glass hollow
fill ~-5 ~5 ~-5 ~5 ~5 ~5 glass hollow

# Dome layer 4 (r=4)
fill ~-4 ~6 ~-4 ~4 ~6 ~4 glass hollow

# Dome layer 5 (r=3)
fill ~-3 ~7 ~-3 ~3 ~7 ~3 glass hollow

# Dome top (r=2)
fill ~-2 ~8 ~-2 ~2 ~8 ~2 glass hollow

# Dome cap
fill ~-1 ~9 ~-1 ~1 ~9 ~1 glass

# Clear interior (air pocket)
fill ~-6 ~ ~-6 ~6 ~1 ~6 air
fill ~-5 ~2 ~-5 ~5 ~3 ~5 air
fill ~-4 ~4 ~-4 ~4 ~5 ~4 air
fill ~-3 ~6 ~-3 ~3 ~6 ~3 air
fill ~-2 ~7 ~-2 ~2 ~7 ~2 air

# Sea lantern lighting
setblock ~0 ~ ~0 sea_lantern
setblock ~-4 ~ ~-4 sea_lantern
setblock ~4 ~ ~-4 sea_lantern
setblock ~-4 ~ ~4 sea_lantern
setblock ~4 ~ ~4 sea_lantern
setblock ~0 ~4 ~0 sea_lantern

# Central decoration
setblock ~0 ~1 ~0 conduit

# Furniture
setblock ~-3 ~ ~0 chest
setblock ~3 ~ ~0 crafting_table
setblock ~0 ~ ~-3 furnace
setblock ~0 ~ ~3 bed

# Entrance tunnel (going down)
fill ~0 ~-1 ~-8 ~0 ~1 ~-8 glass
fill ~0 ~-1 ~-9 ~0 ~1 ~-9 glass
fill ~0 ~-1 ~-10 ~0 ~1 ~-10 glass
fill ~0 ~-2 ~-10 ~0 ~-2 ~-10 ladder

# Kelp garden outside
setblock ~-6 ~-2 ~-6 kelp
setblock ~6 ~-2 ~-6 kelp
setblock ~-6 ~-2 ~6 kelp
setblock ~6 ~-2 ~6 kelp

# Coral decorations
setblock ~-5 ~-2 ~0 brain_coral_block
setblock ~5 ~-2 ~0 tube_coral_block
setblock ~0 ~-2 ~-5 fire_coral_block
setblock ~0 ~-2 ~5 bubble_coral_block

say Underwater Dome complete! Your ocean base awaits!
