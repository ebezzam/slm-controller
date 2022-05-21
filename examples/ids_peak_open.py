# \file    open_camera.py
# \author  IDS Imaging Development Systems GmbH
# \date    2021-03-25
# \since   1.2.0
#
# \brief   This application demonstrates how to use the device manager to open a camera
#
# \version 1.0.1
#
# Copyright (C) 2021, IDS Imaging Development Systems GmbH.
#
# The information in this document is subject to change without notice
# and should not be construed as a commitment by IDS Imaging Development Systems GmbH.
# IDS Imaging Development Systems GmbH does not assume any responsibility for any errors
# that may appear in this document.
#
# This document, or source code, is provided solely as an example of how to utilize
# IDS Imaging Development Systems GmbH software libraries in a sample application.
# IDS Imaging Development Systems GmbH does not assume any responsibility
# for the use or reliability of any portion of this document.
#
# General permission to copy or modify is hereby granted.


from ids_peak import ids_peak  # TODO installation

VERSION = "1.0.1"


def main():
    print("open_camera Sample v" + VERSION)

    # initialize library
    ids_peak.Library.Initialize()

    # create a device manager object
    device_manager = ids_peak.DeviceManager.Instance()

    try:
        # update the device manager
        device_manager.Update()

        # exit program if no device was found
        if device_manager.Devices().empty():
            print("No device found. Exiting Program.")
            return

        # list all available devices
        for i, device in enumerate(device_manager.Devices()):
            print(
                str(i)
                + ": "
                + device.ModelName()
                + " ("
                + device.ParentInterface().DisplayName()
                + "; "
                + device.ParentInterface().ParentSystem().DisplayName()
                + "v."
                + device.ParentInterface().ParentSystem().Version()
                + ")"
            )

        # select a device to open
        selected_device = None
        while True:
            try:
                selected_device = int(input("Select device to open: "))
                if selected_device in range(len(device_manager.Devices())):
                    break
                else:
                    print("Invalid ID.")
            except ValueError:
                print("Please enter a correct id.")
                continue

        # open selected device
        device = device_manager.Devices()[selected_device].OpenDevice(
            ids_peak.DeviceAccessType_Control
        )

        # get the remote device node map
        nodemap_remote_device = device.RemoteDevice().NodeMaps()[0]

        # print model name and user ID
        print("Model Name: " + nodemap_remote_device.FindNode("DeviceModelName").Value())
        try:
            print("User ID: " + nodemap_remote_device.FindNode("DeviceUserID").Value())
        except ids_peak.Exception:
            print("User ID: (unknown)")

        # print sensor information, not knowing if device has the node "SensorName"
        try:
            print("Sensor Name: " + nodemap_remote_device.FindNode("SensorName").Value())
        except ids_peak.Exception:
            print("Sensor Name: " + "(unknown)")

        # print resolution
        try:
            print(
                "Max. resolution (w x h): "
                + str(nodemap_remote_device.FindNode("WidthMax").Value())
                + " x "
                + str(nodemap_remote_device.FindNode("HeightMax").Value())
            )
        except ids_peak.Exception:
            print("Max. resolution (w x h): (unknown)")

    except Exception as e:
        print("Exception: " + str(e) + "")

    finally:
        input("Press Enter to continue...")
        ids_peak.Library.Close()


if __name__ == "__main__":
    main()
