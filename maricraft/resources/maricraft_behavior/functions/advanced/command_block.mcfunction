# Maricraft: Command Block
# Gives all types of command blocks
# Anchor point for building
summon armor_stand "mc_anchor" ~1 ~ ~1

give @s command_block 1
give @s chain_command_block 1
give @s repeating_command_block 1

# Clean up anchor
kill @e[type=armor_stand,name="mc_anchor"]