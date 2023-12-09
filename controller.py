# This file will manage the flow of the application and the sequencing
# of interactions between the user and the system

from model import *
from view import *

def main():
    file_types = ["*.wav", "*.mp3"]
    file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", file_types)])
    #checks if user selects a file
    if file_path:
        calculate_rt60(file_path)
    # file_gui()

if __name__ == "__main__":
    main()
