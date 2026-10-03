import numpy as np
from ALP4 import *
import os
import time
# # from fields import generate_target_field
from packages.dmd_holograms import amplitude_off_axis
# # import pyplon.pylon as pylon

alp_dir = "packages/ALP-4.3"

# dll_path = os.path.join(alp_dir, "x64", "alp4395.dll")

# if not os.path.isfile(dll_path):
#     raise FileNotFoundError(f"ALP DLL not found: {dll_path}")

# os.add_dll_directory(os.path.join(alp_dir, "x64"))

DMD = ALP4(version="4.3", libDir=alp_dir)

NUM_PHASES = 8                         # Phase values to test per segment
DMD_SYNCH_PULSE_WIDTH = 1000           # Sync pulse width to camera (us)
DMD_EXPOSURE_MARGIN_US = 10000         # Safety margin: pictureTime = exposure + this
SATURATION_THRESHOLD = 240.0           # ROI intensity above this triggers exposure reduction
MIN_EXPOSURE_US = 5000                 # Floor for auto-exposure reduction
PROGRESS_INTERVAL = 5                  # Show interim hologram every N segments (0 = never)


def dmd_times(exposure_us):
    """Return (pictureTime, illuminationTime) in microseconds for the given exposure.

    pictureTime must exceed exposure_us so the camera finishes readout
    before the next trigger fires.
    """
    picture = exposure_us + DMD_EXPOSURE_MARGIN_US
    return picture, exposure_us


# DMD = ALP4(version='4.3', libDir='ALP-4.3')
DMD.Initialize()
DMD.DevControl(ALP_SYNCH_POLARITY, ALP_LEVEL_LOW)

# =========================================================
# 2. Initial Hologram Projection (single-frame for live view)
# =========================================================
patch_size = 256
height, width = 1600, 2560

# SQUARE
side = 600
half_side = side//2
cy, cx = height // 2, width // 2

square = np.zeros((height,width), dtype=np.float64)
square[cy - half_side : cy + half_side, cx - half_side : cx + half_side] = 255
working_bitmap = amplitude_off_axis(square)

exposure_time = 60000  # 50ms exposure

seqid = DMD.SeqAlloc(nbImg=1, bitDepth=8)
DMD.ProjControl(ALP_PROJ_INVERSION, 1)
DMD.SeqPut(imgData=working_bitmap.reshape(1, *working_bitmap.shape))
init_p, init_i = dmd_times(exposure_time)
DMD.SetTiming(SequenceId=seqid, illuminationTime=init_i, pictureTime=init_p,
                synchDelay=0, synchPulseWidth=DMD_SYNCH_PULSE_WIDTH, triggerInDelay=None)
DMD.Run(loop=True)

# # Initialize the device
# DMD.Initialize()
# # Binary amplitude image (0 or 1)
# bitDepth = 1    
# imgBlack = np.zeros([DMD.nSizeY,DMD.nSizeX])
# imgWhite = np.ones([DMD.nSizeY,DMD.nSizeX])*(2**8-1)
# imgSeq  = np.concatenate([imgBlack.ravel(),imgWhite.ravel()])

# # Allocate the onboard memory for the image sequence
# DMD.SeqAlloc(nbImg = 2, bitDepth = bitDepth)
# # Send the image sequence as a 1D list/array/numpy array
# DMD.SeqPut(imgData = imgSeq)
# # Set image rate to 50 Hz
# DMD.SetTiming(pictureTime = 20000)

# # Run the sequence in an infinite loop
# DMD.Run()

time.sleep(10)

# Stop the sequence display
DMD.Halt()
# Free the sequence from the onboard memory
DMD.FreeSeq()
# De-allocate the device
DMD.Free()

