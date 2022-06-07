import abc
from ids_peak import ids_peak  # TODO installation
from ids_peak_ipl import ids_peak_ipl  # TODO installation

from slm_controller.hardware import CamDevices, CamParam, cam_devices


class Camera:
    def __init__(self):
        """
        Abstract capturing the functionalities of the cameras used in this project.
        """
        self._width = -1
        self._height = -1
        self._frame = -1

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def frame(self):
        return self._frame

    @abc.abstractmethod
    def acquire_images(self, number=1):
        """
        Triggers the acquisition of images(s).

        Parameters
        ----------
        number : int, optional
            The number of images taken, by default 1
        """
        pass


class IDS(Camera):
    def __init__(self):
        """
        Initializes the camera and sets all the parameters such that acquisition
        in out setting can be started right away.

        Raises
        ------
        IOError
            If no compatible devices cameras are detected by the system
        """
        super().__init__()

        # Set height and width
        self._height, self._width = cam_devices[CamDevices.IDS.value][
            CamParam.IMG_SHAPE
        ]

        # Initialize library
        ids_peak.Library.Initialize()

        # Create a device manager object
        device_manager = ids_peak.DeviceManager.Instance()

        self.__datastream = None

        # Update device manager
        device_manager.Update()

        # Raise exception if no device was found
        if device_manager.Devices().empty():
            raise IOError("Failed to load IDS camera. Check its connection and setup.")

        # Open first device
        self.__device = device_manager.Devices()[0].OpenDevice(
            ids_peak.DeviceAccessType_Control
        )

        # Get nodemap of the remote device for all accesses to the genicam nodemap tree
        node_map = self.__device.RemoteDevice().NodeMaps()[0]

        # Load default settings
        node_map.FindNode("UserSetSelector").SetCurrentEntry("Default")
        node_map.FindNode("UserSetLoad").Execute()
        node_map.FindNode("UserSetLoad").WaitUntilDone()

        # Set acquisition mode to single frame
        node_map.FindNode("AcquisitionMode").SetCurrentEntry(
            node_map.FindNode("EnumEntry_AcquisitionMode_SingleFrame")
        )

        # Change exposure time (in milliseconds)
        node_map.FindNode("ExposureTime").SetValue(200)

        # Lock critical features to prevent them from changing during acquisition
        node_map.FindNode("TLParamsLocked").SetValue(1)

        # Open standard data stream
        self.__datastream = self.__device.DataStreams()[0].OpenDataStream()

        # Get the payload size for correct buffer allocation
        payload_size = node_map.FindNode("PayloadSize").Value()

        # Get minimum number of buffers that must be announced
        buffer_count_min = self.__datastream.NumBuffersAnnouncedMinRequired()

        # Allocate and announce image buffers and queue them
        for _ in range(buffer_count_min):
            buffer = self.__datastream.AllocAndAnnounceBuffer(payload_size)
            self.__datastream.QueueBuffer(buffer)

        # Hacky fix for a bug with exposure time
        self.acquire_images()  # TODO Bug, first image seems not use newly set parameters

    def acquire_images(self, number=1):
        """
        Acquire image(s).

        Parameters
        ----------
        number : int, optional
            The number of images to be taken, by default 1

        Returns
        -------
        list
            The list of acquired images
        """
        images = []

        for _ in range(number):
            self._frame += 1

            # Get nodemap of the remote device for all accesses to the genicam nodemap tree
            node_map = self.__device.RemoteDevice().NodeMaps()[0]

            # Start acquisition on camera
            acquisition_start = node_map.FindNode("AcquisitionStart")
            self.__datastream.StartAcquisition()
            acquisition_start.Execute()
            acquisition_start.WaitUntilDone()

            # Get buffer from device's datastream
            buffer = self.__datastream.WaitForFinishedBuffer(5000)

            # Stop acquisition on camera
            self.__datastream.StopAcquisition()

            # Flush datastream
            self.__datastream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)

            # Queue buffer so that it can be used again
            self.__datastream.QueueBuffer(buffer)

            # Create IDS peak IPL image
            ipl_image = ids_peak_ipl.Image_CreateFromSizeAndBuffer(
                buffer.PixelFormat(),
                buffer.BasePtr(),
                buffer.Size(),
                self._width,
                self._height,
            )

            # Append images as numpy array to list of acquired images
            images.append(ipl_image.get_numpy_2D())

        return images

    def __del__(self):
        """
        Clean up before exit.
        """
        if self.__datastream:
            # Stop and flush the datastream
            self.__datastream.KillWait()
            self.__datastream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)

            for buffer in self.__datastream.AnnouncedBuffers():
                self.__datastream.RevokeBuffer(buffer)

        ids_peak.Library.Close()
