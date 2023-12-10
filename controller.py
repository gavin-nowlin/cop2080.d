# controller.py

from model import *
from view import *

def main():
    file_types = [".wav", ".mp3"]
    
    # Setting up main window with tkinter
    root = tk.Tk()
    root.title("Audio Analysis")

    # Variable to store the selected file path
    selected_file_path = tk.StringVar()

    # Function to handle file selection
    def select_file():
        file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("Audio Files", file_types)])
        selected_file_path.set(file_path)

    # Function to run calculations when the "Submit" button is clicked
    def submit_file():
        file_path = selected_file_path.get()
        if file_path:
            # Specify a list of frequencies
            frequencies = [250, 1000, 5000]

            # Create a color map for different frequencies
            color_map = {250: 'blue', 1000: 'green', 5000: 'red'}

            # Calculate and plot RT60 for each frequency
            for frequency in frequencies:
                calculate_rt60(file_path, frequency, color_map[frequency])

    # Create a button to select an audio file
    select_button = tk.Button(root, text="Select Audio File", command=select_file)
    select_button.pack(pady=20)

    # Create a label to display the selected file path
    file_label = tk.Label(root, textvariable=selected_file_path)
    file_label.pack()

    # Create a button to submit the selected file and run calculations
    submit_button = tk.Button(root, text="Submit", command=submit_file)
    submit_button.pack(pady=20)

    root.mainloop()

    # file_gui()

if __name__ == "__main__":
    main()