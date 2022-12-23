from pylsl import StreamInlet, resolve_stream
import numpy as np
import tensorflow as tf
import serial
import time
# your model path here.
MODEL_NAME = "new_models\96.28-acc-64x3-batch-norm-7epoch-1667974849-loss-0.32.model"

model = tf.keras.models.load_model(MODEL_NAME)
reshape = (-1, 16, 50)
model.predict(np.zeros((32, 16, 50)).reshape(reshape), verbose=0)
FFT_MAX_HZ = 50

HM_SECONDS = 10  # this is approximate. Not 100%. do not depend on this.
TOTAL_ITERS = HM_SECONDS*25  # ~25 iters/sec

# Setting up the device
ser = serial.Serial('COM4', 9600) 

# first resolve an EEG stream on the lab network
print("looking for stream...")
streams = resolve_stream('type', 'FFT')
# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])
print("stream found!")
maxCount = 15
count = 0
move = ''
for i in range(TOTAL_ITERS):  # how many iterations. Eventually this would be a while True
    channel_data = []
    for i in range(16):  # each of the 16 channels here
        sample, timestamp = inlet.pull_sample()
        channel_data.append(sample[:FFT_MAX_HZ])

    network_input = np.array(channel_data).reshape(reshape)
    out = model.predict(network_input,verbose=0)
    print(np.rint(out[0]))
    if((np.rint(out[0]) == np.array([0, 0, 0, 1])).all()):
        if(move == 'bite'):
            count = count + 1
        else:
            move = 'bite'
            count = 1

        if(count >= maxCount):
            move = ''
            count = 0
            ser.write(b'G') 
            print('Send Signal')

        print('bite')
    elif((np.rint(out[0]) == np.array([0, 0, 1, 0])).all()):
        if(move == 'right'):
            count = count + 1
        else:
            move = 'right'
            count = 1

        if(count >= maxCount):
            move = ''
            count = 0
            ser.write(b'R')
            print('Send Signal')

        print('right')
    elif((np.rint(out[0]) == np.array([0, 1, 0, 0])).all()):
        if(move == 'none'):
            count = count + 1
        else:
            move = 'none'
            count = 1

        if(count >= maxCount):
            move = ''
            count = 0
            ser.write(b'O')
            print('Send Signal')

        print('none')
    elif((np.rint(out[0]) == np.array([1, 0, 0, 0])).all()):
        if(move == 'left'):
            count = count + 1
        else:
            move = 'left'
            count = 1

        if(count >= maxCount):
            move = ''
            count = 0
            ser.write(b'B')
            print('Send Signal')

        print('left')
        
    time.sleep(1)