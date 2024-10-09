import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import ffmpeg
import re
import subprocess, sys, os

def select_video():
    video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
    if video_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, video_path)
        set_time_slider(video_path)

def update_value(new_value):
    disp_label.config(text=f"Selected Value: {new_value}")
    
    

def select_audio():
    audio_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.aac;*.flac")])
    if audio_path:
        audio_entry.delete(0, tk.END)
        audio_entry.insert(0, audio_path)

def set_time_slider(video_path):
    try:
        # Get video duration using ffmpeg
        probe = ffmpeg.probe(video_path)
        duration = float(probe['format']['duration'])
        
        time_slider.config(from_=0, to=int(duration))
        time_label.config(text=f'Set Start Time (0 - {int(duration)} seconds):')
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not get video duration: {e}")

def merge_audio_video():
    video_path = video_entry.get()
    audio_path = audio_entry.get()
    start_time = time_slider.get()

    if video_path and audio_path:
        output_path = video_path.rsplit('.', 1)[0] + '_merged.mp4'
        try:
            # Run FFmpeg to merge audio into video
            
            re ="ffmpeg -i " + video_path + " " +"-itsoffset " + str(start_time) + " -i " +audio_path + " -map 0:0 -map 1:0 -c:v copy " + output_path
            
            subprocess.call(re, shell=True)
           
            
                
            #"ffmpeg -fflags +genpts -y -i " + video_path + audio_path + "ss=start_timecodec='copy', shortest=None" + output_path
            
            messagebox.showinfo("Success", f"Merged video created at: {output_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not merge video and audio: {e}")
    else:
        messagebox.showwarning("Warning", "Please select both video and audio files.")

# Create the main window
root = tk.Tk()
root.title("Video and Audio Merger")
root.geometry("400x400")

# Video selection
tk.Label(root, text="Selected Video:").pack(pady=5)
video_entry = tk.Entry(root, width=50)
video_entry.pack(pady=5)
tk.Button(root, text="Select Video", command=select_video).pack(pady=5)

# Audio selection
tk.Label(root, text="Selected Audio:").pack(pady=5)
audio_entry = tk.Entry(root, width=50)
audio_entry.pack(pady=5)
tk.Button(root, text="Select Audio", command=select_audio).pack(pady=5)

# Time slider
time_label = tk.Label(root, text="Set Start Time:")
time_label.pack(pady=5)
time_slider = ttk.Scale(root, from_=0, to=100, orient='horizontal',command=update_value)
time_slider.pack(pady=5, fill=tk.X)

# dipslay selcted time
disp_label = tk.Label(root, text="Selected Value:")
disp_label.pack(pady=5)

# Merge button
tk.Button(root, text="Merge Audio to Video", command=merge_audio_video).pack(pady=20)

# Run the application
root.mainloop()
