from abc import ABCMeta, abstractmethod
from ids_peak import ids_peak  # TODO installation
from ids_peak_ipl import ids_peak_ipl  # TODO installation


class Camera(metaclass=ABCMeta):
    def __init__(self):
        self._width = 0
        self._height = 0
        self._frame = 0

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def frame(self):
        return self._frame

    @abstractmethod
    def acquire_image(self):
        return


class IDS(Camera):
    def __init__(self):
        super().__init__()

        # initialize library
        ids_peak.Library.Initialize()

        # create a device manager object
        device_manager = ids_peak.DeviceManager.Instance()

        self.__datastream = None

        # update device manager
        device_manager.Update()

        # # exit program if no device was found
        # if device_manager.Devices().empty():
        #     return #TODO what?

        # open selected device
        self.__device = device_manager.Devices()[0].OpenDevice(
            ids_peak.DeviceAccessType_Control
        )

        # Get nodemap of the remote device for all accesses to the genicam nodemap tree
        node_map = self.__device.RemoteDevice().NodeMaps()[0]

        # load default settings
        node_map.FindNode("UserSetSelector").SetCurrentEntry("Default")
        node_map.FindNode("UserSetLoad").Execute()
        node_map.FindNode("UserSetLoad").WaitUntilDone()

        node_map.FindNode("AcquisitionMode").SetCurrentEntry(
            node_map.FindNode("EnumEntry_AcquisitionMode_SingleFrame")
        )

        # change exposure time
        # node_map.FindNode("ExposureTime").SetValue(33.189)
        node_map.FindNode("ExposureTime").SetValue(42)

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

        self._width = node_map.FindNode("WidthMax").Value()
        self._height = node_map.FindNode("HeightMax").Value()

    def acquire_image(self):
        self._frame += 1

        # Get nodemap of the remote device for all accesses to the genicam nodemap tree
        node_map = self.__device.RemoteDevice().NodeMaps()[0]

        acquisition_start = node_map.FindNode("AcquisitionStart")

        # Start acquisition on camera
        self.__datastream.StartAcquisition()
        acquisition_start.Execute()
        acquisition_start.WaitUntilDone()

        # Get buffer from device's datastream
        buffer = self.__datastream.WaitForFinishedBuffer(5000)

        self.__datastream.StopAcquisition()

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

        return ipl_image.get_numpy_2D()

    def __del__(self):
        if self.__datastream:
            # Stop and flush the datastream
            self.__datastream.KillWait()
            # self.__datastream.StopAcquisition(ids_peak.AcquisitionStopMode_Default)
            self.__datastream.Flush(ids_peak.DataStreamFlushMode_DiscardAll)

            for buffer in self.__datastream.AnnouncedBuffers():
                self.__datastream.RevokeBuffer(buffer)

        ids_peak.Library.Close()
