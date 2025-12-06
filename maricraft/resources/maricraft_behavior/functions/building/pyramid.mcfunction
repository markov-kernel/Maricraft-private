# Maricraft: Pyramid (Bedrock Edition)
# Builds a sandstone pyramid with hidden treasure chamber

# Base layer 1 (largest, 21x21)
fill ~-10 ~ ~-10 ~10 ~2 ~10 sandstone

# Layer 2 (19x19)
fill ~-9 ~3 ~-9 ~9 ~4 ~9 sandstone

# Layer 3 (17x17)
fill ~-8 ~5 ~-8 ~8 ~6 ~8 sandstone

# Layer 4 (15x15)
fill ~-7 ~7 ~-7 ~7 ~8 ~7 sandstone

# Layer 5 (13x13)
fill ~-6 ~9 ~-6 ~6 ~10 ~6 sandstone

# Layer 6 (11x11)
fill ~-5 ~11 ~-5 ~5 ~12 ~5 sandstone

# Layer 7 (9x9)
fill ~-4 ~13 ~-4 ~4 ~14 ~4 sandstone

# Layer 8 (7x7)
fill ~-3 ~15 ~-3 ~3 ~16 ~3 sandstone

# Layer 9 (5x5)
fill ~-2 ~17 ~-2 ~2 ~18 ~2 sandstone

# Top cap (3x3)
fill ~-1 ~19 ~-1 ~1 ~20 ~1 gold_block

# Entrance (front)
fill ~0 ~ ~-10 ~0 ~3 ~-10 air
fill ~0 ~4 ~-10 ~0 ~4 ~-10 chiseled_sandstone

# Entrance stairs going down
fill ~0 ~-1 ~-9 ~0 ~-1 ~-6 sandstone_stairs
fill ~0 ~-2 ~-5 ~0 ~-2 ~-2 sandstone_stairs

# Hidden treasure chamber (inside pyramid)
fill ~-3 ~-3 ~-3 ~3 ~-1 ~3 air
fill ~-3 ~-4 ~-3 ~3 ~-4 ~3 smooth_sandstone

# Treasure!
setblock ~0 ~-3 ~0 gold_block
setblock ~-2 ~-3 ~-2 chest
setblock ~2 ~-3 ~-2 chest
setblock ~-2 ~-3 ~2 chest
setblock ~2 ~-3 ~2 chest

# Gold block accents
setblock ~-2 ~-3 ~0 gold_block
setblock ~2 ~-3 ~0 gold_block
setblock ~0 ~-3 ~-2 gold_block
setblock ~0 ~-3 ~2 gold_block

# Torches in chamber
setblock ~-3 ~-2 ~0 torch
setblock ~3 ~-2 ~0 torch
setblock ~0 ~-2 ~-3 torch
setblock ~0 ~-2 ~3 torch

# Decorative terracotta stripes (hieroglyphic style)
fill ~-10 ~1 ~-10 ~10 ~1 ~-10 orange_terracotta
fill ~-9 ~4 ~-9 ~9 ~4 ~-9 orange_terracotta
fill ~-8 ~6 ~-8 ~8 ~6 ~-8 orange_terracotta
fill ~-7 ~8 ~-7 ~7 ~8 ~-7 orange_terracotta

# Chiseled sandstone accents on corners
setblock ~-10 ~1 ~-10 chiseled_sandstone
setblock ~10 ~1 ~-10 chiseled_sandstone
setblock ~-10 ~1 ~10 chiseled_sandstone
setblock ~10 ~1 ~10 chiseled_sandstone

# Sphinx-like decoration (small)
fill ~-6 ~ ~-14 ~-4 ~2 ~-12 sandstone
setblock ~-5 ~3 ~-13 carved_pumpkin

# Oasis palm tree
setblock ~8 ~ ~-14 jungle_log
setblock ~8 ~1 ~-14 jungle_log
setblock ~8 ~2 ~-14 jungle_log
setblock ~8 ~3 ~-14 jungle_log
fill ~6 ~4 ~-16 ~10 ~4 ~-12 jungle_leaves

# Water pool
fill ~6 ~-1 ~-16 ~10 ~-1 ~-12 water

say Pyramid complete! Ancient treasures await within!
