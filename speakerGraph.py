import audioVisualization as aV
import audioSegmentation as aS
from collections import defaultdict
import os
import time
import wave
import contextlib
import numpy as np
import matplotlib.pyplot as plt
import datetime
import warnings
warnings.filterwarnings("ignore")

durations = []
runtimes = []
diarizations = []
for file in os.listdir("AudioTest"):
	if file.endswith(".wav"):
		audio_path="AudioTest/"+file
		#audio_path="Audio/cpb-aacip-106-31cjt1bv.wav"
		with contextlib.closing(wave.open(audio_path,'r')) as f:
			frames = f.getnframes()
			rate = f.getframerate()
			duration = frames / float(rate)
			durations.append(duration)
		num_speakers = 0
		t0 = time.clock()
		speaker_array=aS.speakerDiarization(audio_path,num_speakers,PLOT=False)
		t1 = time.clock() - t0
		runtimes.append(t1)
		current = 0
		count = 0
		total = 0
		startResult = defaultdict(list)
		endResult = defaultdict(list)
		for i in speaker_array:
			total = total + 1
			if i == current:
				count += 1
			else:	
				start =datetime.timedelta(seconds=(total - count)*.2)
				end = datetime.timedelta(seconds=total*.2)
				start = start - datetime.timedelta(microseconds=start.microseconds)
				end = end - datetime.timedelta(microseconds=end.microseconds)
				startResult[i].append(str(start))
				endResult[i].append(str(end))
				count = 0
				current = i
		#result = zip(startResult,endResult)
		#d = dict((k, tuple(v)) for k, v in result.iteritems())
		#print(result)
		#print(str(startResult))
		#print(str(endResult))
		print "\n",file
		for speaker in startResult:
			start = startResult[speaker]
			end = endResult[speaker]
			print "Speaker ",speaker
			for i in range(len(start)):
				print "Time In: ",start[i]
				print "Time Out: ",end[i]
			
#print(diarizations)
d = np.array(durations)
r = np.array(runtimes)
fig = plt.figure()
plt.plot(d,r)
plt.xlabel("Duration")
plt.ylabel("Runtime")
fig.savefig('runtime.png')

#print(t1)
#current = 0
#count = 0
#result = defaultdict(list)
#for i in speaker_array:
#	if i == current:
#		count += 1
#	else:
#		result[i].append(count*.2)
#		count = 0
#		current = i
#d = dict((k, tuple(v)) for k, v in result.iteritems())
#print(file)
#print(d)
