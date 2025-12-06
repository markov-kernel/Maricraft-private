# Maricraft: Underwater Dome (Bedrock Edition)
# Builds a glass dome base - perfect for underwater!

# Clear area for dome
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-8 ~-1 ~-8 ~8 ~10 ~8 air

# Floor (prismarine)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 prismarine
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 prismarine_bricks
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 dark_prismarine

# Dome layer 1 (base, r=7)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-7 ~ ~-7 ~7 ~ ~7 glass hollow
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-7 ~1 ~-7 ~7 ~1 ~7 glass hollow

# Dome layer 2 (r=6)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-6 ~2 ~-6 ~6 ~2 ~6 glass hollow
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-6 ~3 ~-6 ~6 ~3 ~6 glass hollow

# Dome layer 3 (r=5)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-5 ~4 ~-5 ~5 ~4 ~5 glass hollow
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-5 ~5 ~-5 ~5 ~5 ~5 glass hollow

# Dome layer 4 (r=4)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-4 ~6 ~-4 ~4 ~6 ~4 glass hollow

# Dome layer 5 (r=3)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-3 ~7 ~-3 ~3 ~7 ~3 glass hollow

# Dome top (r=2)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-2 ~8 ~-2 ~2 ~8 ~2 glass hollow

# Dome cap
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-1 ~9 ~-1 ~1 ~9 ~1 glass

# Clear interior (air pocket)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-6 ~ ~-6 ~6 ~1 ~6 air
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-5 ~2 ~-5 ~5 ~3 ~5 air
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-4 ~4 ~-4 ~4 ~5 ~4 air
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-3 ~6 ~-3 ~3 ~6 ~3 air
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~-2 ~7 ~-2 ~2 ~7 ~2 air

# Sea lantern lighting
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~ ~0 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-4 ~ ~-4 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~4 ~ ~-4 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-4 ~ ~4 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~4 ~ ~4 sea_lantern
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~4 ~0 sea_lantern

# Central decoration
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~1 ~0 conduit

# Furniture
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-3 ~ ~0 chest
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~3 ~ ~0 crafting_table
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~ ~-3 furnace
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~ ~3 red_bed

# Entrance tunnel (going down)
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~0 ~-1 ~-8 ~0 ~1 ~-8 glass
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~0 ~-1 ~-9 ~0 ~1 ~-9 glass
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~0 ~-1 ~-10 ~0 ~1 ~-10 glass
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ fill ~0 ~-2 ~-10 ~0 ~-2 ~-10 ladder

# Kelp garden outside
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-6 ~-2 ~-6 kelp
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~6 ~-2 ~-6 kelp
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-6 ~-2 ~6 kelp
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~6 ~-2 ~6 kelp

# Coral decorations
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~-5 ~-2 ~0 brain_coral_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~5 ~-2 ~0 tube_coral_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-2 ~-5 fire_coral_block
execute @e[type=armor_stand,name="mc_anchor",c=1] ~ ~ ~ setblock ~0 ~-2 ~5 bubble_coral_block

say Underwater Dome complete! Your ocean base awaits!

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]