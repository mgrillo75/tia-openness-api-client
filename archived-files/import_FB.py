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

    # Path to the modified XML file
    xml_path = "C:\\Users\\MIGUEL\\Documents\\tia-openness-api-client\\Block_1.xml"
    
    print(f"Importing modified Block_1 from: {xml_path}")
    try:
        # Using the create method to import the block
        imported_block = software.get_blocks().create(xml_path, "Block_1")
        print(f"Successfully imported block: {imported_block.name}")
        
        # Save the project after importing the block
        tia_client.project.save()
        print("Project saved successfully")
    except Exception as e:
        print(f"Error importing block: {e}")

    print("\nAttempting to compile the project...")
    try:
        tia_client.project.compile()
        print("Project compilation successful")
    except Exception as e:
        print(f"Error compiling project: {e}")

input("Press Enter to continue...")