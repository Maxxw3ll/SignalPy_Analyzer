# SignalPy_Analyzer
SignalPy_Analyzer is a technical application designed for the educational exploration of digital signal processing. The primary objective of this project is to provide a practical platform for consolidating theoretical knowledge regarding Fourier Transforms and the application of digital filters in an audio context. By bridging the gap between mathematical concepts and real-world audio data, the tool allows users to observe how complex signals are decomposed and manipulated.

To operate the software, the user simply needs to initialize the main.py script. Once the interface is active, the user can load any standard .wav file into the system. Upon loading, the application automatically generates and displays the signal spectrum, providing immediate visual feedback of the frequency content. From this point, the user can apply various digital filters according to their analytical needs. The system also allows for the processed audio to be exported and saved as a new .wav file, preserving the modifications made during the session.

The software facilitates the visualization of the Fast Fourier Transform, enabling a clear transition from time-domain waveforms to frequency-domain spectra. This process is essential for understanding the harmonic content of audio signals. Additionally, the application integrates Butterworth filter implementations, allowing for the active testing of Low-Pass, High-Pass, and Band-Pass filters. Users can modify parameters such as cutoff frequencies and bandwidth to observe the immediate attenuation effects on the spectral density of the signal.

The project is built on a modular architecture to ensure code clarity and maintainability. The core logic is separated into two main modules located in the core directory: loaders handles the input and output of audio files, while signals manages the digital signal processing and mathematical computations. The graphical interface, located in the gui directory, manages the integration of interactive plotting tools and the user control panel. The main script serves as the centralized entry point that coordinates these modules.

To execute the application, several Python libraries must be installed. The project utilizes numpy for numerical array processing and scipy for scientific computing and signal filtering. The graphical interface is powered by tkinter and matplotlib, which handle the layout and the dynamic plotting of frequencies respectively. Additionally, sounddevice is used for audio playback, and mplcursors provides interactive data inspection within the graphs.

The following dependencies are required to run the project:

numpy

scipy

sounddevice

matplotlib

mplcursors

These can be installed using the Python package manager by executing the command pip install followed by the library names. This project is distributed under the MIT License, which provides a standard legal framework for the use and modification of the source code.
