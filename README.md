# SignalPy_Analyzer

SignalPy_Analyzer is a technical application designed for the educational exploration of digital signal processing. The primary objective of this project is to provide a practical platform for consolidating theoretical knowledge regarding **Fourier Transforms** and the application of **digital filters** in an audio context. By bridging the gap between mathematical concepts and real-world audio data, the tool allows users to observe how complex signals are decomposed and manipulated.

---

## 🛠 Operation & Workflow

To operate the software, the user simply needs to initialize the `main.py` script. Once the interface is active, the following workflow is enabled:

1.  **Loading Data:** The user can load any standard `.wav` file into the system.
2.  **Spectral Analysis:** Upon loading, the application automatically generates and displays the signal spectrum, providing immediate visual feedback of the frequency content.
3.  **Applying Filters:** From this point, the user can apply various digital filters according to their analytical needs.
4.  **Exporting Results:** The system allows for the processed audio to be exported and saved as a new `.wav` file, preserving the modifications made during the session.

---

## 🔬 Technical Capabilities

The software facilitates the visualization of the **Fast Fourier Transform (FFT)**, enabling a clear transition from time-domain waveforms to frequency-domain spectra. This process is essential for understanding the harmonic content of audio signals.

### Digital Filter Implementation
The application integrates **Butterworth filter** implementations, allowing for the active testing of:
* **Low-Pass Filters**
* **High-Pass Filters**
* **Band-Pass Filters**

Users can modify parameters such as **cutoff frequencies** and **bandwidth** to observe the immediate attenuation effects on the spectral density of the signal.

---

## 📂 Modular Architecture

The project is built on a modular architecture to ensure code clarity and maintainability. The core logic is separated into distinct modules:

* **`core/` directory:**
    * `loaders`: Handles the input and output of audio files.
    * `signals`: Manages the digital signal processing and mathematical computations.
* **`gui/` directory:**
    * Manages the integration of interactive plotting tools and the user control panel.
* **`main.py`**: Serves as the centralized entry point that coordinates these modules.

---

## 💻 Requirements & Dependencies

To execute the application, several Python libraries must be installed. The project utilizes:

* **numpy**: For numerical array processing.
* **scipy**: For scientific computing and signal filtering.
* **tkinter**: Powers the graphical interface layout.
* **matplotlib**: Handles the dynamic plotting of frequencies.
* **sounddevice**: Used for audio playback.
* **mplcursors**: Provides interactive data inspection within the graphs.

### Installation
You can install the required dependencies using the Python package manager by executing:

```bash
pip install numpy scipy sounddevice matplotlib mplcursors
