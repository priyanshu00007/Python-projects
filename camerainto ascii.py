import tkinter as tk
from tkinter import font as tkfont
import cv2
from PIL import Image, ImageTk
import threading
import time

# ASCII characters used for different brightness levels
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

class ASCIICam:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        self.video_source = 0  # Default camera
        
        # Open video source
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.video_source)
        
        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.pack()
        
        # Create a Text widget to display ASCII art
        self.text = tk.Text(window, wrap=tk.NONE)
        self.text.pack(expand=True, fill='both')
        
        # Use a fixed-width font
        fixed_font = tkfont.Font(family="Courier", size=10)
        self.text.configure(font=fixed_font)
        
        # Button to take snapshot
        self.btn_snapshot = tk.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)
        
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()
        
        self.window.mainloop()
    
    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.read()
        
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
            # Convert frame to ASCII
            ascii_frame = self.frame_to_ascii(frame)
            
            # Update Text widget
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, ascii_frame)
        
        self.window.after(self.delay, self.update)
    
    def frame_to_ascii(self, frame, new_width=70):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Resize the image
        height, width = gray.shape
        aspect_ratio = height/width
        new_height = int(aspect_ratio * new_width * 0.55)
        resized = cv2.resize(gray, (new_width, new_height))
        
        # Convert pixels to ASCII
        ascii_str = ''
        for row in resized:
            for pixel in row:
                ascii_str += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
            ascii_str += '\n'
        
        return ascii_str

# Create a window and pass it to ASCIICam
root = tk.Tk()
ASCIICam(root, "ASCII Camera")