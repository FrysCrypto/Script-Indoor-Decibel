"""
Decibel Miner ver. 2.0.1

This script captures decibel levels using a microphone and logs these levels.
Sensitive operations such as encryption, decryption, and SFTP uploading have been redacted for security reasons.
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

import pyaudio
import numpy as np
import datetime
import os
import uuid
import json

def get_decibel(data):
    fourier = np.fft.fft(data)
    fourier = np.delete(fourier, len(fourier) // 2)
    power = np.abs(fourier) ** 2
    mean_power = np.average(power)
    return 10 * np.log10(mean_power)

def write_to_log(db, current_file):
    now = datetime.datetime.now()
    with open(current_file, 'a') as f:
        f.write(f"{now.strftime('%H:%M:%S')} - {db}\n")

# Functionality for uploading to SFTP and decrypting data has been removed for security reasons.

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
mac = '-'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])

last_upload_hour = datetime.datetime.now().hour
# Initialize the current_file variable
now = datetime.datetime.now()
current_file = f"DecibelLog_{mac}_{now.strftime('%m%d%Y_%H%M%S')}.log"

while True:
    now = datetime.datetime.now()
    
    data = np.frombuffer(stream.read(1024), dtype=np.int16)
    decibel = get_decibel(data)
    write_to_log(decibel, current_file)
    print(f"Recorded {decibel} dB at {now.strftime('%H:%M:%S')}")  # printing for visibility
    
    
