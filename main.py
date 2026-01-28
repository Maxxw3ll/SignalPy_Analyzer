import sys 
from pathlib import Path
from gui.interface import window

root = Path(__file__).parent
sys.path.insert(0, str(root))

if __name__ == "__main__":
    try:
        print("--- SigPy_Analyzer: Starting the analyzer ---")
        print("Initializing GUI...")
        print("✓ Application started successfully")
        print("Load a WAV file to begin analyzing audio spectra\n")
        
        # Start the Tkinter event loop
        window.mainloop()
        
    except KeyboardInterrupt:
        print("\n--- SigPy_Analyzer: Shutdown requested ---")
        window.quit()
        
    except Exception as e:
        print(f"--- SigPy_Analyzer: Error occurred ---")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    finally:
        print("--- SigPy_Analyzer: Application closed ---")
