import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import pillow_heif
import threading

def convert_to_jpg(file_path, progress_callback):
    try:
        heif_file = pillow_heif.read_heif(file_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        jpg_path = file_path.rsplit('.', 1)[0] + '.jpg'
        image.save(jpg_path, 'JPEG')
        progress_callback(f"Converted {file_path} to {jpg_path}", image)
    except Exception as e:
        progress_callback(f"Failed to convert {file_path}: {str(e)}", None)

def drop(event):
    file_paths = root.tk.splitlist(event.data)
    total_files = len(file_paths)
    thread = threading.Thread(target=process_files, args=(file_paths, total_files))
    thread.start()

def process_files(file_paths, total_files):
    for i, file_path in enumerate(file_paths):
        if file_path.lower().endswith('.heic'):
            convert_to_jpg(file_path, lambda message, img: update_progress(i, total_files, message, img))
    update_progress(total_files, total_files, "All files have been converted.", None)  # Notify completion

def update_progress(index, total, message, image):
    progress = ((index + 1) / total) * 100
    text.insert('end', message + '\n')
    text.see(tk.END)  # Auto-scroll to the end
    progress_bar['value'] = progress
    if image:
        display_image(image)
    root.update_idletasks()  # Update the GUI to reflect progress

def display_image(image):
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

def set_window_size_and_position():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = int(screen_width * 0.75)
    height = int(screen_height * 0.75)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')

root = TkinterDnD.Tk()
root.title('HEIC to JPG Converter')

# Set window size and position
set_window_size_and_position()

# Explanation label
explanation = tk.Label(root, text="Drag and drop HEIC files into the window to convert them to JPG. The progress will be displayed below.", font=("Helvetica", 14))
explanation.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

# Text widget for log output
text = tk.Text(root, font=("Helvetica", 12))
text.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate')
progress_bar.grid(row=2, column=0, columnspan=2, sticky='ew', padx=10, pady=(10, 0))

# Image preview label (square field)
image_label = tk.Label(root, relief="sunken", width=200, height=200, text="Image Preview")
image_label.grid(row=1, column=2, rowspan=2, padx=10, pady=10, sticky='se')

# Configure grid to expand
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=0)
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)

# Register drop target
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.mainloop()
