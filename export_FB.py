import tia_portal.config as tia_config
from tia_portal import Client
import os

tia_config.load()

tia_client = Client()

# Open the specified project
#project_path = "C:\\Users\\Miguel\\Documents\\Openness-Automation"
#project_name = "08-15-2024(Production)_MiguelPID"
project_path = "C:\\Users\\MIGUEL\\Documents\\HMH Press TIA Archive\\09-09-2024"
project_name = "09_08_2024(Final Screen 34)"
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

    # Find the specific block "fbHmiInputs"
    print("Searching for block 'fbHmiInputs'...")
    fbHmiInputs = software.get_blocks().find("fbHmiInputs")

    if fbHmiInputs:
        print(f"Block 'fbHmiInputs' found. Attempting to export...")
        try:
            # Print additional information about the block
            print(f"Block name: {fbHmiInputs.name}")
            print(f"Block type: {fbHmiInputs.get_type()}")

            # Create a directory for exported blocks if it doesn't exist
            export_dir = os.path.join(os.path.dirname(__file__), "exported_blocks")
            os.makedirs(export_dir, exist_ok=True)

            # Export the block
            export_path = os.path.join(export_dir, f"{fbHmiInputs.name}.xml")
            fbHmiInputs.export()
            print(f"Successfully exported to: {export_path}")
        except Exception as e:
            print(f"Error exporting 'fbHmiInputs': {e}")
            print("Additional error information:")
            print(f"Block value: {fbHmiInputs.value}")
            print(f"Block parent: {fbHmiInputs.parent}")
    else:
        print("Block 'fbHmiInputs' not found in the project")
    
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