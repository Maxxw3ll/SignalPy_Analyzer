import numpy as np
import scipy.signal as signal


class Signals:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.nyquist = sample_rate//2
        self.N = 1024
        self.freqs = np.linspace(0, self.nyquist, self.N//2)
        self.window = np.hanning(self.N)
    
    def apply_filter(self, audio_data, filter_type, cutoff_freq, bandwidth):
        norm_freq = cutoff_freq / self.nyquist
        norm_freq = max(0.001, min(0.999, norm_freq))
        
        if filter_type == "Band Pass":
            low_Hz = max(10, cutoff_freq - (bandwidth/2)) 
            high_Hz = min(self.nyquist-10, cutoff_freq + (bandwidth/2))  
            
            under_freq = low_Hz/self.nyquist 
            over_freq = high_Hz/self.nyquist

            if under_freq >= over_freq:
                over_freq = max(0.001, min(0.999, under_freq + 0.01))

            b, a = signal.butter(4, [under_freq, over_freq], btype="bandpass")
        
        elif filter_type == "Low Pass":
            b, a = signal.butter(4, norm_freq, btype="low")
        
        elif filter_type == "High Pass":
            b, a = signal.butter(4, norm_freq, btype="high")
        
        else:
            raise ValueError("Filter not recognised")
        
        return signal.lfilter(b,a, audio_data)
    
    def get_spectrum(self, data_to_analyze, start_index):
        if start_index + self.N > len(data_to_analyze):
            extraction = np.zeros(self.N)
            actual_data = data_to_analyze[start_index:]
            extraction[:len(actual_data)] = actual_data
        else:
            extraction = data_to_analyze[start_index:start_index + self.N]
        
        Hamming = np.multiply(self.window, extraction)
        extraction_fft = np.fft.fft(Hamming)
        spectrum = np.abs(extraction_fft)
        spectrum_dB = 20*np.log10(spectrum[:(self.N)//2] + 1e-10)
        return spectrum_dB



    

    


    