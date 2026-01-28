import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from core.loaders import Loaders
from core.signals import Signals
import mplcursors
import scipy.io.wavfile as wav_writer

loaders = Loaders()
signals = None
current_figure = None
current_canvas = None
current_toolbar = None

# --- UPDATE SPECTRUM WITH FILTER ---

def update_spectrum_with_filter():
    global signals, current_figure, current_canvas, current_toolbar
    
    if loaders.data is None or signals is None:
        return
    
    cuttoff_freq = slider_cutoff.get()
    BandWidth_freq = Band_Width.get()
    filter_type = combo_filter.get()
    
    # Apply filter if selected
    if filter_type == "None":
        filtered_data = loaders.data
    else:
        filtered_data = signals.apply_filter(loaders.data, filter_type, cuttoff_freq, BandWidth_freq)
    
    # Get spectrum of filtered data
    spectrum_dB = signals.get_spectrum(filtered_data, 0)
    
    # Update the plot
    if current_figure is not None:
        ax = current_figure.get_axes()[0]
        ax.clear()
        ax.semilogx(signals.freqs, spectrum_dB, color="#ef7600")
        ax.set_xlim([20, loaders.sample_rate//2])
        ax.set_ylim([-60, 30])
        ax.set_xlabel("Freq (Hz)", color="black")   
        ax.set_ylabel("Ampl (dB)", color="black")
        ax.tick_params(colors="black")
        ax.grid(True, which="both", ls="-", alpha=0.2, color="black")
        current_figure.patch.set_facecolor("white")
        ax.set_facecolor("white")
        
        # Add cursor interaction
        import mplcursors
        cursor = mplcursors.cursor(ax, hover=True)
        
        @cursor.connect("add")
        def _(sel):
            sel.annotation.set_text(f"{sel.target[0]:.1f} Hz\n{sel.target[1]:.1f} dB")
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)
        
        current_canvas.draw()

# --- LOAD A FILE FUNCTION ---

def load_file():
    global signals, current_figure, current_canvas, current_toolbar
    try:
        file_path = filedialog.askopenfilename(
            title="Select a WAV file",
            filetypes=[("WAV files", "*.wav")]
        )
        
        if not file_path:
            return
        
        loaders.check_file_exists(file_path)

        sample_rate, data = loaders.process_wav_file(file_path)

        signals = Signals(sample_rate)
        spectrum_dB = signals.get_spectrum(data, 0)

        for widget in plot_container.winfo_children():
            widget.destroy()

        current_figure, ax = plt.subplots(figsize=(8,4))
        current_figure.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.semilogx(signals.freqs, spectrum_dB, color="#ef7600")

        ax.set_xlim([20, sample_rate//2])
        ax.set_ylim([-60, 30])
        ax.set_xlabel("Freq (Hz)", color="black")   
        ax.set_ylabel("Ampl (dB)", color="black")
        ax.tick_params(colors="black")
        ax.grid(True, which="both", ls="-", alpha=0.2, color="black")

        # Create a frame for the toolbar
        toolbar_frame = tk.Frame(plot_container, bg="white")
        toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Create canvas and toolbar
        current_canvas = FigureCanvasTkAgg(current_figure, master=plot_container)  
        current_toolbar = NavigationToolbar2Tk(current_canvas, toolbar_frame)
        current_toolbar.update()
        
        cursor = mplcursors.cursor(ax, hover=True)

        @cursor.connect("add")
        def _(sel):
            sel.annotation.set_text(f"{sel.target[0]:.1f} Hz\n{sel.target[1]:.1f} dB")
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.8)

        current_canvas.draw()
        current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        messagebox.showerror("File Load Error", f"Error loading file:\n{str(e)}")      

def save_file():
    global signals
    try:
        if loaders.data is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".wav",
                filetypes=[("WAV files", "*.wav")],
                title="Save Processed Audio"
            )

            if file_path:
                filter_type = combo_filter.get()

                if filter_type == "None" or signals is None:
                    date_saved = loaders.data
                else:
                    cuttoff_freq = slider_cutoff.get()
                    BandWidth_freq = Band_Width.get()
                    date_saved = signals.apply_filter(loaders.data, filter_type, cuttoff_freq, BandWidth_freq)
        
                wav_writer.write(file_path, loaders.sample_rate, date_saved)
                messagebox.showinfo("Success", f"File saved successfully at:\n{file_path}")
        else:
            messagebox.showwarning("Warning", "No audio data to save!")
    except Exception as e:
        messagebox.showerror("Save Error", f"Error saving file:\n{str(e)}")

def play_filter():
    global signals
    if loaders.data is not None and signals is not None:
        try:
            cuttoff_freq = slider_cutoff.get()
            BandWidth_freq = Band_Width.get()
            filter_type = combo_filter.get()

            if filter_type == "None":
                loaders.play_audio()
                return

            filtered_data = signals.apply_filter(loaders.data, filter_type, cuttoff_freq, BandWidth_freq)

            import sounddevice as sd
            sd.stop()
            sd.play(filtered_data, loaders.sample_rate)
        except Exception as e:
            messagebox.showerror("Playback Error", f"An error occurred during playback:\n{str(e)}")
    else:
        messagebox.showwarning("Warning", "Load a WAV file first")

# --- MAIN WINDOW CONFIGURATION ---
window = tk.Tk()
window.state('zoomed')
window.title("Spectrum Analyzer")
window.configure(bg="black")

# --- SIDEBAR PANEL (Left) ---
sidebar_frame = tk.Frame(window, bg="grey", width=280)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
sidebar_frame.pack_propagate(False)

# Sidebar Header
label_settings = tk.Label(
    sidebar_frame, 
    text="Configuration Settings",
    font=("Helvetica", 18),
    fg="white",
    bg="grey"
)
label_settings.pack(pady=20)

# Load Button
btn_load = tk.Button(
    sidebar_frame, 
    text="Load wav file 📁", 
    bg="lightgrey",
    fg="black",
    font=("Helvetica", 15),
    relief="flat",
    cursor="hand2",
    height=2,
    command=load_file
) 
btn_load.pack(pady=10, fill=tk.X, padx=10)

btn_save_model = tk.Button(
    sidebar_frame, 
    text="Save model 📁", 
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 15),
    relief="flat",
    cursor="hand2",
    height=2,
    command=save_file
) 
btn_save_model.pack(pady=10, fill=tk.X, padx=10)


# --- FILTER CONTROLS ---

# Cutoff Frequency Section
label_cutoff = tk.Label(
    sidebar_frame, 
    text="Cutoff Frequency (Hz)", 
    font=("Helvetica", 12), 
    fg="white", 
    bg="grey"
)
label_cutoff.pack(pady=(30, 0), padx=10, anchor="w")

slider_cutoff = tk.Scale(
    sidebar_frame, 
    from_=20, 
    to=20000, 
    orient=tk.HORIZONTAL,
    bg="grey", 
    fg="white", 
    highlightthickness=0,
    command=lambda v: update_spectrum_with_filter()
)
slider_cutoff.set(1000) 
slider_cutoff.pack(fill=tk.X, padx=10)

label_BW = tk.Label(
    sidebar_frame, 
    text="Band Width (Hz)", 
    font=("Helvetica", 12), 
    fg="white", 
    bg="grey"
)
label_BW.pack(pady=(30, 0), padx=10, anchor="w")

Band_Width = tk.Scale(
    sidebar_frame, 
    from_=20, 
    to=20000, 
    orient=tk.HORIZONTAL,
    bg="grey", 
    fg="white", 
    highlightthickness=0,
    command=lambda v: update_spectrum_with_filter()
)
Band_Width.set(500) 
Band_Width.pack(fill=tk.X, padx=10, pady=5)

# Filter Type Section
label_filter = tk.Label(
    sidebar_frame, 
    text="Filter Type", 
    font=("Helvetica", 12), 
    fg="white", 
    bg="grey"
)
label_filter.pack(pady=(20, 0), padx=10, anchor="w")

combo_filter = ttk.Combobox(
    sidebar_frame, 
    values=["None","Low Pass", "High Pass", "Band Pass"], 
    state="readonly"
)
combo_filter.current(0)
combo_filter.bind("<<ComboboxSelected>>", lambda e: update_spectrum_with_filter())
combo_filter.pack(fill=tk.X, padx=10, pady=5)


# --- AUDIO PLAYBACK CONTROLS ---
playback_frame = tk.Frame(sidebar_frame, bg="grey")
playback_frame.pack(pady=30)

btn_play_original = tk.Button(playback_frame, text="▶ Play Original", width=12, command=loaders.play_audio)
btn_play_original.pack(side=tk.LEFT, padx=5)

btn_play_filtered = tk.Button(playback_frame, text="▶ Play Filtered", width=12, command=play_filter)
btn_play_filtered.pack(side=tk.LEFT, padx=5)


btn_stop = tk.Button(playback_frame, text="⏹ Stop", width=8, command=loaders.stop_audio)
btn_stop.pack(side=tk.LEFT, padx=5)

# --- MAIN PANEL (Right) ---
main_panel = tk.Frame(window, bg="black")
main_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Main Title
label_main_title = tk.Label(
    main_panel, 
    text="Spectrum Analyzer Interface", 
    font=("Helvetica", 24), 
    fg="white", 
    bg="black", 
    padx=20, 
    pady=20
)
label_main_title.pack(anchor="nw")

# Visualization Area (Plot Area)
plot_container = tk.Frame(main_panel, bg="white")
plot_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

label_placeholder = tk.Label(
    plot_container,
    text="(Plot Area)",
    bg="white",
    fg="grey",
    font=("Helvetica", 16)
)
label_placeholder.place(relx=0.5, rely=0.5, anchor="center")

# --- START APPLICATION ---
window.mainloop()