import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Function to load IoT device data
def load_data():
    uploaded_file = st.file_uploader("Upload your IoT device data CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    else:
        st.warning("Please upload a CSV file containing IoT device data.")
        return None

# Sample data format expected:
# DeviceID | BatteryLevel | SignalStrength | LastActive | Status

# Load the IoT device data
data = load_data()

if data is not None:
    # Display dataset overview
    st.write("## IoT Device Data Overview")
    st.write(data.head())

    # Display summary statistics
    st.write("## Summary Statistics")
    st.write(data.describe())

    # Plot battery levels of devices
    st.write("### Device Battery Levels")
    plt.figure(figsize=(10, 5))
    plt.bar(data["DeviceID"], data["BatteryLevel"], color='skyblue')
    plt.xlabel("Device ID")
    plt.ylabel("Battery Level (%)")
    plt.title("Battery Levels of IoT Devices")
    st.pyplot(plt)

    # Plot signal strength of devices
    st.write("### Device Signal Strength")
    plt.figure(figsize=(10, 5))
    plt.bar(data["DeviceID"], data["SignalStrength"], color='salmon')
    plt.xlabel("Device ID")
    plt.ylabel("Signal Strength (dB)")
    plt.title("Signal Strength of IoT Devices")
    st.pyplot(plt)

    # Identify and display inactive or low-battery devices
    st.write("## Device Health Alerts")
    
    # Devices with low battery
    low_battery = data[data["BatteryLevel"] < 20]
    if not low_battery.empty:
        st.warning("Devices with Low Battery (< 20%):")
        st.write(low_battery[["DeviceID", "BatteryLevel"]])
    else:
        st.success("All devices have sufficient battery.")

    # Devices with low signal strength
    low_signal = data[data["SignalStrength"] < -80]
    if not low_signal.empty:
        st.warning("Devices with Low Signal Strength (< -80 dB):")
        st.write(low_signal[["DeviceID", "SignalStrength"]])
    else:
        st.success("All devices have adequate signal strength.")

    # Devices not active for a long time
    inactive_devices = data[data["Status"] == "Inactive"]
    if not inactive_devices.empty:
        st.warning("Inactive Devices:")
        st.write(inactive_devices[["DeviceID", "LastActive"]])
    else:
        st.success("All devices are currently active.")
    
    # Add interactivity: Choose a device to view its details
    st.write("## Device Details")
    selected_device = st.selectbox("Select a Device ID to view details", data["DeviceID"].unique())
    device_data = data[data["DeviceID"] == selected_device]
    st.write(device_data)

    # Alerts for individual device health status
    if device_data["BatteryLevel"].values[0] < 20:
        st.error("Warning: Selected device has low battery.")
    if device_data["SignalStrength"].values[0] < -80:
        st.error("Warning: Selected device has low signal strength.")
    if device_data["Status"].values[0] == "Inactive":
        st.error("Warning: Selected device is inactive.")

    # Summarize alerts
    st.write("## Overall Health Summary")
    total_devices = len(data)
    low_battery_count = len(low_battery)
    low_signal_count = len(low_signal)
    inactive_count = len(inactive_devices)

    st.write(f"Total Devices: {total_devices}")
    st.write(f"Devices with Low Battery: {low_battery_count}")
    st.write(f"Devices with Low Signal Strength: {low_signal_count}")
    st.write(f"Inactive Devices: {inactive_count}")
