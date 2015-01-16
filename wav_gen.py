import numpy as np
from scipy.io import wavfile

def sine(f, t):
    return np.sin( 2 * np.pi * f * t )

def sample(t):
    s = 0
    for x in [1]:
        s += sine( 50 + np.power(1-t, 4) * 800, t )
    return s

rate = 44100
wave = []

for x in range( 0, 44100 ):
    time = float(x) / rate
    wave.append( sample( time ) )

max = np.max( np.abs( wave ) )
scaled = np.int16( wave / max * 32767 )
wavfile.write( "test.wav", rate, scaled )
