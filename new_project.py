import tia_portal.config as tia_config
from tia_portal import Client

tia_config.load()

tia_client = Client()

tia_client.open_project("C:\\Users\\user\\Documents\\Automation", "NAME")

tia_client.project.save_as("NAME_2")

plcs = tia_client.project.get_plcs()

if len(plcs) == 0:
    print("No PLCs found in project")
elif len(plcs) > 1:
    print("Multiple PLCs found in project")
else:
    plc = plcs[0]

    software = plc.get_software()

    software_blocks = software.get_all_blocks(True)

    print("Compiling project...", end="\r")
    tia_client.project.compile()
    print("Compiling project... Done")

    for block in software_blocks:
        print(block.name, end="\r")
        try:
            block.export()
        except Exception as e:
            print(e)
            continue

input("Press Enter to continue...")