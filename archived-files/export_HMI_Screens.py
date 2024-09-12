import tia_portal.config as tia_config
from tia_portal import Client, HmiSoftware, ExportOptions
import os

# Load TIA Portal configuration
tia_config.load()

# Initialize TIA Portal client
tia_client = Client()

# Define project path and name
project_path = "C:\\Users\\MIGUEL\\Documents\\HMH Press TIA Archive\\09-07-2024"
project_name = "09_06_2024(Final)"

# Open the specified project
print(f"Opening project: {project_path}\\{project_name}")
tia_client.open_project(project_path, project_name)

# Get all devices in the project
devices = tia_client.project.get_devices()
print(f"Total devices found: {len(devices)}")

# Print detailed information for each device
for device in devices:
    print(f"\nDevice found: {device.name}")
    print(f"Device type: {device.TypeIdentifier}")
    software = device.get_software()
    if software:
        print(f"Software type: {type(software).__name__}")
    else:
        print("No software found for this device")

# Filter HMI devices
hmi_devices = [device for device in devices if isinstance(device.get_software(), HmiSoftware)]
print(f"\nHMI devices found: {len(hmi_devices)}")

if not hmi_devices:
    print("No HMI devices found in the project")
    print("Available devices:")
    for device in devices:
        print(f"- {device.name} (Type: {device.TypeIdentifier})")
else:
    for hmi_device in hmi_devices:
        print(f"\nProcessing HMI device: {hmi_device.name}")
        
        hmi_target = hmi_device.get_software()
        
        if hmi_target:
            print(f"HMI software found for device: {hmi_device.name}")
            
            screen_folder = hmi_target.ScreenFolder
            print(f"Screen folder accessed for device: {hmi_device.name}")
            
            export_dir = os.path.join(os.path.dirname(__file__), "exported_screens", hmi_device.name)
            os.makedirs(export_dir, exist_ok=True)
            print(f"Export directory created: {export_dir}")
            
            screens = list(screen_folder.Screens)
            print(f"Total screens found: {len(screens)}")
            for screen in screens:
                export_path = os.path.join(export_dir, f"{screen.Name}.xml")
                print(f"Exporting screen: {screen.Name} to {export_path}")
                hmi_target.export_screen(screen, export_path)
            
            popup_folder = hmi_target.ScreenPopupFolder
            popups = list(popup_folder.Screens)
            print(f"Total pop-up screens found: {len(popups)}")
            for popup in popups:
                export_path = os.path.join(export_dir, f"Popup_{popup.Name}.xml")
                print(f"Exporting pop-up screen: {popup.Name} to {export_path}")
                hmi_target.export_screen(popup, export_path)
        else:
            print(f"No software found for HMI device: {hmi_device.name}")

print("\nScreen export process completed.")
input("Press Enter to continue...")
