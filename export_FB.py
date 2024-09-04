import tia_portal.config as tia_config
from tia_portal import Client
import os

tia_config.load()

tia_client = Client()

# Open the specified project
project_path = "C:\\Users\\Miguel\\Documents\\Openness-Automation"
project_name = "08-15-2024(Production)_MiguelPID"
print(f"Opening project: {project_path}\\{project_name}")
tia_client.open_project(project_path, project_name)

plcs = tia_client.project.get_plcs()

if len(plcs) == 0:
    print("No PLCs found in project")
elif len(plcs) > 1:
    print("Multiple PLCs found in project")
else:
    plc = plcs[0]
    software = plc.get_software()

    # Find the specific block "fbMain"
    print("Searching for block 'Block_1'...")
    Block_1 = software.get_blocks().find("Block_1")

    if Block_1:
        print(f"Block 'Block_1' found. Attempting to export...")
        try:
            # Print additional information about the block
            print(f"Block name: {Block_1.name}")
            print(f"Block type: {Block_1.get_type()}")

            # Create a directory for exported blocks if it doesn't exist
            export_dir = os.path.join(os.path.dirname(__file__), "exported_blocks")
            os.makedirs(export_dir, exist_ok=True)

            # Export the block
            export_path = os.path.join(export_dir, f"{Block_1.name}.xml")
            Block_1.export()
            print(f"Successfully exported to: {export_path}")
        except Exception as e:
            print(f"Error exporting 'Block_1': {e}")
            print("Additional error information:")
            print(f"Block value: {Block_1.value}")
            print(f"Block parent: {Block_1.parent}")
    else:
        print("Block 'Block_1' not found in the project")
    
    # List all blocks in the project for debugging
    print("\nListing all blocks in the project:")
    all_blocks = software.get_all_blocks(recursive=True)
    for block in all_blocks:
        print(f"- {block.name} ({block.get_type()})")

    # Try to compile the project
    print("\nAttempting to compile the project...")
    try:
        tia_client.project.compile()
        print("Project compilation successful")
    except Exception as e:
        print(f"Error compiling project: {e}")

    # Try to export all blocks
    print("\nAttempting to export all blocks...")
    for block in all_blocks:
        print(f"Exporting {block.name}...", end="\r")
        try:
            block.export()
            print(f"Exported {block.name}    ")
        except Exception as e:
            print(f"Error exporting {block.name}: {e}")

input("Press Enter to continue...")