from pylsl import StreamInlet, resolve_stream #pip install pylsl
import numpy as np # pip install numpy
import time
import os

ACTION = 'none' # THIS IS THE ACTION YOU'RE DOING, left wink right wink bite and none 

FFT_MAX_HZ = 50

HM_SECONDS = 10 # 
TOTAL_ITERS = HM_SECONDS*25  # ~25 iters/sec

# first resolve an EEG stream on the lab network
print("looking for stream...")
streams = resolve_stream('type', 'FFT')
# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])
print("stream found!")

channel_datas = []

for i in range(TOTAL_ITERS):  # how many iterations. Eventually this would be a while True
    channel_data = []
    for i in range(16): # each of the 16 channels here
        sample, timestamp = inlet.pull_sample()
        channel_data.append(sample[:FFT_MAX_HZ])

    channel_datas.append(channel_data)

datadir = "data"
if not os.path.exists(datadir):
    os.mkdir(datadir)

actiondir = f"{datadir}/{ACTION}"
if not os.path.exists(actiondir):
    os.mkdir(actiondir)

print(len(channel_datas))

print(f"saving {ACTION} data...")
np.save(os.path.join(actiondir, f"{int(time.time())}.npy"), np.array(channel_datas))
print("done.")