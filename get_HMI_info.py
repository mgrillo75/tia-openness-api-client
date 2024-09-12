import tia_portal.config as tia_config
from tia_portal import Client, HmiSoftware, ExportOptions
import os

tia_config.load()

tia_client = Client()

# Open the specified project
project_path = "C:\\Users\\Miguel\\Documents\\Openness-Automation"
project_name = "08-15-2024(Production)_MiguelPID"
print(f"Opening project: {project_path}\\{project_name}")
tia_client.open_project(project_path, project_name)

# Get all devices in the project
devices = tia_client.project.get_devices()
print(f"Total devices found: {len(devices)}")

hmi_devices = []

# List of known HMI device names
known_hmi_names = ["TP1200 Comfort", "HMI_1"]

for device in devices:
    print(f"\nDevice: {device.name}")
    print(f"Type: {device.TypeIdentifier}")
    print(f"Device value: {device.value}")
    print(f"Device properties: {dir(device)}")
    print(f"Device value properties: {dir(device.value)}")  # Print available attributes of device.value
    
    # Use the Name attribute to identify HMI devices
    device_name = device.value.Name if hasattr(device.value, 'Name') else "Unknown"
    print(f"Device name identified as: {device_name}")
    
    if device_name in known_hmi_names or device.TypeIdentifier == "HMI":
        print(f"HMI device found: {device.name}")
        hmi_software = device.get_software()
        if isinstance(hmi_software, HmiSoftware):
            hmi_devices.append((device, hmi_software))
            print(f"HMI software found for device: {device.name}")
        else:
            print(f"Device {device.name} does not have HMI software.")

print(f"\nHMI devices found: {len(hmi_devices)}")

if not hmi_devices:
    print("No HMI devices found in the project")
else:
    for device, hmi_software in hmi_devices:
        print(f"Processing HMI device: {device.name}")
        
        screen_folder = hmi_software.ScreenFolder
        print(f"Screen folder accessed for device: {device.name}")
        
        export_dir = os.path.join(os.path.dirname(__file__), "exported_screens", device.name)
        os.makedirs(export_dir, exist_ok=True)
        print(f"Export directory created: {export_dir}")
        
        screens = list(screen_folder.Screens)
        print(f"Total screens found: {len(screens)}")
        for screen in screens:
            export_path = os.path.join(export_dir, f"{screen.Name}.xml")
            print(f"Exporting screen: {screen.Name} to {export_path}")
            hmi_software.export_screen(screen, export_path)
        
        popup_folder = hmi_software.ScreenPopupFolder
        popups = list(popup_folder.Screens)
        print(f"Total pop-up screens found: {len(popups)}")
        for popup in popups:
            export_path = os.path.join(export_dir, f"Popup_{popup.Name}.xml")
            print(f"Exporting pop-up screen: {popup.Name} to {export_path}")
            hmi_software.export_screen(popup, export_path)

print("\nScreen export process completed.")
input("Press Enter to continue...")
