from pylsl import StreamInlet, resolve_stream
import time  
import serial

# set up Arduino serial port - replace with the one you are using
ser = serial.Serial('COM4', 9600) 

# resolve an EMG stream on the lab network and notify the user
print("Looking for an EMG stream...")
streams = resolve_stream('type', 'EMG')
inlet = StreamInlet(streams[0])
print("EMG stream found!")

# initialize time threshold and variables for storing time
time_thres = 500
prev_time = 0
flex_thres = 0.6
time_thres1 = 500
prev_time1 = 0
blink_thres1 = 0.6

biteCount = 0
leftCount = 0
start = time.time()
while True:
    samples, timestamp = inlet.pull_sample() 
    curr_time = int(round(time.time() * 1000))
    if ((samples[0] >=  flex_thres) & (curr_time - time_thres > prev_time)) : # if an EMG spike is detected from the cheek muscles send 'G'
        prev_time = int(round(time.time() * 1000)) # update time
        leftCount = 1 + leftCount
        ser.write(b'G') # send a signal indecating it is a blink
        end = time.time()
        print('wink Done')
        if end - start >= 15: # if no action is done then return to startmode and reset the count 
            start = time.time()
            leftCount = 0
        while (leftCount >= 5):
            samples, timestamp = inlet.pull_sample() # get EMG data sample and its timestamp
            curr_time = int(round(time.time() * 1000)) # get current time in milliseconds
            end = time.time()
            if end - start >= 15:
                start = time.time()
                leftCount = 0
                break
            if ((samples[0] >=  blink_thres1) & (samples[1] >=  blink_thres1) & (curr_time - time_thres1 > prev_time1)):  # two eye blink 
                prev_time1 = int(round(time.time() * 1000)) # update time 
                ser.write(b'S') # no action 
            elif ((samples[0] >=  flex_thres) & (curr_time - time_thres > prev_time)):
                prev_time = int(round(time.time() * 1000)) # update time
                ser.write(b'L') # left eye ====> 45 degree right
                start = time.time()
            elif((samples[1] >=  flex_thres) & (curr_time - time_thres > prev_time)): 
                prev_time = int(round(time.time() * 1000)) # update time
                ser.write(b'R') # right eye =====> 45 degree right
                start = time.time()
            elif((samples[2] >=  flex_thres) & (curr_time - time_thres > prev_time)): 
                prev_time = int(round(time.time() * 1000)) # update time
                ser.write(b'F') # forward
                start = time.time()
            elif((samples[3] >=  flex_thres) & (curr_time - time_thres > prev_time)): 
                prev_time = int(round(time.time() * 1000)) # update time
                ser.write(b'F') #Forward
                start = time.time()
            elif(curr_time - time_thres > prev_time): # if no spike is detected send 'O'
                prev_time = int(round(time.time() * 1000)) # update time
                ser.write(b'S')
