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

# Add a new TP1200 Comfort Panel HMI
hmi_name = "New_TP1200_Comfort"
print(f"Adding new HMI device: {hmi_name}")

# Get the device group
device_group = tia_client.project.DeviceGroups[0]  # Assuming the first device group is the correct one

# Check if the device already exists
existing_device = next((device for device in device_group.Devices if device.Name == hmi_name), None)

if existing_device is None:
    print("No TP1200 Comfort device found in the project. Adding a new one.")
    # Add a new HMI device
    new_hmi = device_group.Devices.CreateFrom("Siemens.Automation.ObjectFrame.ICoreHmiTarget.TP1200_Comfort", hmi_name)
    print(f"New HMI device created: {new_hmi.Name}")
else:
    print(f"TP1200 Comfort device already exists: {existing_device.Name}")
    new_hmi = existing_device

# Get the software container for the new HMI device
hmi_software = new_hmi.DeviceItems[1].SoftwareContainer
if not isinstance(hmi_software, HmiSoftware):
    print(f"No HMI software container found for device {new_hmi.Name}")
else:
    print(f"HMI software found for device: {new_hmi.Name}")

    # Add a simple screen to the new HMI device
    screen_folder = hmi_software.Screens
    new_screen = screen_folder.Create("SimpleScreen")
    print(f"New screen created: {new_screen.Name}")

    # Export the new screen
    export_dir = os.path.join(os.path.dirname(__file__), "exported_screens", new_hmi.Name)
    os.makedirs(export_dir, exist_ok=True)
    export_path = os.path.join(export_dir, f"{new_screen.Name}.xml")
    new_screen.Export(export_path, ExportOptions.WithDefaults)
    print(f"Exported screen: {new_screen.Name} to {export_path}")

print("\nHMI device addition and screen export process completed.")
input("Press Enter to continue...")
