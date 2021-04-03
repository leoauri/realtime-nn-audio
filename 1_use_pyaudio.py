#!/usr/bin/env python
# coding: utf-8


import pyaudio
import math
import time


import operator

def test(a,b,comp):
    assert comp(a,b), f'{a} does not {comp.__name__} {b}'
    
def test_eq(a,b):
    test(a,b,operator.eq)


TEST = 'test'


test_eq(TEST, 'test')


def test_near(a,b,eps=1e-4):
    assert abs(a - b) < eps, f'{a} not within {eps} of {b}'


audioport = pyaudio.PyAudio()


framerate = 44100


class SineGen():
    def __init__(self, freq):
        self.freq = freq
    
    def get_frame(self, in_data, frame_count, time_info, status):
        frame = [self.sine_at_time(time_info['output_buffer_dac_time'] + i / framerate) 
                 for i in range(frame_count)]
        return (bytes(frame), pyaudio.paContinue)
        
    def sine_at_time(self, t):
        return math.sin(2 * math.pi * t * self.freq)


if __name__ == '__main__':
    sine = SineGen(440)


    test_near(0, sine.sine_at_time(0))
    test_near(0, sine.sine_at_time(1/440))
    test_near(0, sine.sine_at_time(2/440))
    test_near(0, sine.sine_at_time(1.5/440))
    test_near(1, sine.sine_at_time(1.25/440))


    stream = audioport.open(rate=framerate, channels=1, format=pyaudio.paFloat32, output=True, stream_callback=sine.get_frame)


    stream.start_stream()

    time.sleep(10)

    stream.stop_stream()
    stream.close()
    audioport.terminate()
