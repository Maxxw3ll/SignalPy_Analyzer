import numpy as np
import scipy.io.wavfile as wav
import scipy.signal as signal
import os
import sounddevice as sd


class Loaders:
    def check_file_exists(self, file_path):
        if os.path.exists(file_path):
            print(f"File found: {file_path}")
        else:
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def __init__(self): 
        self.data = None
        self.sample_rate = None

    def process_wav_file(self, file_path):
        # Check if file exists
        self.check_file_exists(file_path)
        
        # Load WAV file
        self.sample_rate, self.data = wav.read(file_path)

        # Normalize data
        self.data = self.data / np.max(np.abs(self.data))

        if len(self.data.shape) > 1:
            self.data = self.data.mean(axis=1) # Use only the first channel for stereo files

        # Calculate duration
        self.duration = len(self.data) / self.sample_rate
        
        # Create time array
        self.time = np.linspace(0, self.duration, len(self.data))
        
        return self.sample_rate, self.data
    
    def play_audio(self, start_time = 0):
        if self.data is not None and self.sample_rate is not None:
            try:
                import sounddevice as sd
                start_index = int(start_time * self.sample_rate)
                sd.play(self.data[start_index:], self.sample_rate)
            except Exception as e:
                print(f"Audio playback error: {e}")
        else:
            raise ValueError("No audio data loaded. Please load a WAV file first.")
        

    def stop_audio(self):
        if self.data is not None and self.sample_rate is not None:
            try:
                sd.stop()
            except Exception as e:
                print(f"Audio stop error: {e}")
        else:
            raise ValueError("No audio data loaded. Please load a WAV file first.")
    

    