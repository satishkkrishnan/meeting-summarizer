import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import threading
import time
import json
import os
from datetime import datetime
import speech_recognition as sr
import openai
from dotenv import load_dotenv
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from PIL import Image, ImageTk, ImageGrab
import io
import base64

# Load environment variables
load_dotenv()

class MeetingSummarizer:
    def __init__(self):
        # Set up OpenAI API
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Audio recording variables
        self.is_recording = False
        self.audio_data = []
        self.sample_rate = 44100
        self.recording_thread = None
        
        # Meeting data
        self.current_meeting = {
            'title': '',
            'start_time': None,
            'transcript': [],
            'summary': '',
            'notes': [],
            'screenshots': []
        }
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Configure customtkinter with modern theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window with modern styling
        self.root = ctk.CTk()
        self.root.title("🎯 Meeting Summarizer Pro")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Set minimum window size
        self.root.minsize(1000, 700)
        
        # Create menu bar
        self.create_menu()
        
        # Create main container with gradient-like effect
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header section with modern design
        header_frame = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=20)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Modern title with gradient-like effect
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(fill="x", padx=30, pady=30)
        
        # Main title with modern styling
        title_label = ctk.CTkLabel(
            title_container, 
            text="🎯 Meeting Summarizer Pro", 
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#4a9eff", "#66b3ff")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_container,
            text="AI-Powered Meeting Documentation & Analysis",
            font=ctk.CTkFont(size=16),
            text_color=("#888888", "#aaaaaa")
        )
        subtitle_label.pack()
        
        # Create content area with modern card design
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.pack(fill="both", expand=True)
        
        # Meeting info card with modern styling
        meeting_card = ctk.CTkFrame(content_container, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        meeting_card.pack(fill="x", pady=(0, 20))
        
        # Meeting title section with modern input
        title_section = ctk.CTkFrame(meeting_card, fg_color="transparent")
        title_section.pack(fill="x", padx=25, pady=25)
        
        title_label = ctk.CTkLabel(
            title_section, 
            text="📝 Meeting Title", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#4a9eff", "#66b3ff")
        )
        title_label.pack(anchor="w", pady=(0, 15))
        
        # Modern title input with better styling
        self.title_entry = ctk.CTkEntry(
            title_section, 
            placeholder_text="Enter a descriptive meeting title...", 
            height=45,
            font=ctk.CTkFont(size=16),
            fg_color=("#3a3a3a", "#2a2a2a"),
            border_color=("#4a9eff", "#66b3ff"),
            border_width=2,
            corner_radius=10
        )
        self.title_entry.pack(fill="x", pady=(0, 20))
        
        # Control buttons section with modern design
        controls_section = ctk.CTkFrame(meeting_card, fg_color="transparent")
        controls_section.pack(fill="x", padx=25, pady=(0, 25))
        
        # Modern button container
        button_container = ctk.CTkFrame(controls_section, fg_color="transparent")
        button_container.pack(fill="x")
        
        # Recording button with modern styling
        self.record_button = ctk.CTkButton(
            button_container, 
            text="🎙️ Start Recording", 
            command=self.toggle_recording, 
            fg_color=("#00c853", "#00e676"),
            hover_color=("#00a047", "#00c853"),
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12
        )
        self.record_button.pack(side="left", padx=(0, 15))
        
        # Stop button with modern styling
        self.stop_button = ctk.CTkButton(
            button_container, 
            text="⏹️ Stop Recording", 
            command=self.stop_recording, 
            fg_color=("#ff5252", "#ff7676"),
            hover_color=("#d32f2f", "#ff5252"),
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=(0, 15))
        
        # Generate summary button with modern styling
        self.summary_button = ctk.CTkButton(
            button_container, 
            text="🤖 Generate AI Summary", 
            command=self.generate_summary,
            fg_color=("#9c27b0", "#ba68c8"),
            hover_color=("#7b1fa2", "#9c27b0"),
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12,
            state="disabled"
        )
        self.summary_button.pack(side="left", padx=(0, 15))
        
        # Save button with modern styling
        self.save_button = ctk.CTkButton(
            button_container, 
            text="💾 Save Meeting", 
            command=self.save_meeting,
            fg_color=("#ff9800", "#ffb74d"),
            hover_color=("#f57c00", "#ff9800"),
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12,
            state="disabled"
        )
        self.save_button.pack(side="left", padx=(0, 15))
        
        # Load meeting button with modern styling
        self.load_button = ctk.CTkButton(
            button_container, 
            text="📂 Load Meeting", 
            command=self.load_meeting,
            fg_color=("#607d8b", "#90a4ae"),
            hover_color=("#455a64", "#607d8b"),
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12
        )
        self.load_button.pack(side="left", padx=(0, 15))
        
        # Save As button with modern styling
        self.save_as_button = ctk.CTkButton(
            button_container, 
            text="💾 Save As", 
            command=self.save_meeting_as,
            fg_color=("#795548", "#8d6e63"),
            hover_color=("#5d4037", "#795548"),
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12,
            state="disabled"
        )
        self.save_as_button.pack(side="left", padx=(0, 15))
        
        # Status indicator with modern design
        status_container = ctk.CTkFrame(controls_section, fg_color="transparent")
        status_container.pack(fill="x", pady=(20, 0))
        
        # Modern status label
        self.status_label = ctk.CTkLabel(
            status_container, 
            text="✨ Ready to record your next meeting", 
            font=ctk.CTkFont(size=16),
            text_color=("#4caf50", "#66bb6a")
        )
        self.status_label.pack(side="right")
        
        # Create modern tabbed interface
        tabs_container = ctk.CTkFrame(content_container, fg_color="transparent")
        tabs_container.pack(fill="both", expand=True)
        
        # Modern notebook styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2b2b2b', borderwidth=0)
        style.configure('TNotebook.Tab', background='#3a3a3a', foreground='white', padding=[20, 10], borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', '#4a9eff'), ('active', '#5a5a5a')])
        
        # Notebook for tabs with modern styling
        self.notebook = ttk.Notebook(tabs_container)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Transcript tab with modern design
        transcript_frame = ctk.CTkFrame(self.notebook, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        self.notebook.add(transcript_frame, text="📄 Live Transcript")
        
        # Transcript header
        transcript_header = ctk.CTkFrame(transcript_frame, fg_color="transparent")
        transcript_header.pack(fill="x", padx=20, pady=(20, 10))
        
        transcript_title = ctk.CTkLabel(
            transcript_header,
            text="🎯 Real-time Meeting Transcription",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#4a9eff", "#66b3ff")
        )
        transcript_title.pack(anchor="w")
        
        # Modern transcript text area
        self.transcript_text = ctk.CTkTextbox(
            transcript_frame, 
            wrap="word",
            fg_color=("#3a3a3a", "#2a2a2a"),
            text_color=("#ffffff", "#ffffff"),
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            border_color=("#4a9eff", "#66b3ff"),
            border_width=1
        )
        self.transcript_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Summary tab with modern design
        summary_frame = ctk.CTkFrame(self.notebook, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        self.notebook.add(summary_frame, text="🤖 AI Summary")
        
        # Summary header
        summary_header = ctk.CTkFrame(summary_frame, fg_color="transparent")
        summary_header.pack(fill="x", padx=20, pady=(20, 10))
        
        summary_title = ctk.CTkLabel(
            summary_header,
            text="🧠 AI-Generated Meeting Summary",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#9c27b0", "#ba68c8")
        )
        summary_title.pack(anchor="w")
        
        # Modern summary text area
        self.summary_text = ctk.CTkTextbox(
            summary_frame, 
            wrap="word",
            fg_color=("#3a3a3a", "#2a2a2a"),
            text_color=("#ffffff", "#ffffff"),
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            border_color=("#9c27b0", "#ba68c8"),
            border_width=1
        )
        self.summary_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Notes tab with modern design
        notes_frame = ctk.CTkFrame(self.notebook, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        self.notebook.add(notes_frame, text="✏️ Notes")
        
        # Notes header
        notes_header = ctk.CTkFrame(notes_frame, fg_color="transparent")
        notes_header.pack(fill="x", padx=20, pady=(20, 10))
        
        notes_title = ctk.CTkLabel(
            notes_header,
            text="📝 Manual Notes & Action Items",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#ff9800", "#ffb74d")
        )
        notes_title.pack(anchor="w")
        
        # Modern notes input section
        notes_input_frame = ctk.CTkFrame(notes_frame, fg_color="transparent")
        notes_input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        note_label = ctk.CTkLabel(
            notes_input_frame, 
            text="Add Note:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#ff9800", "#ffb74d")
        )
        note_label.pack(side="left", padx=(0, 15))
        
        # Modern note input
        self.note_entry = ctk.CTkEntry(
            notes_input_frame, 
            placeholder_text="Type your note or action item here...",
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color=("#3a3a3a", "#2a2a2a"),
            border_color=("#ff9800", "#ffb74d"),
            border_width=2,
            corner_radius=10
        )
        self.note_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        # Screenshot button
        screenshot_button = ctk.CTkButton(
            notes_input_frame, 
            text="📸 Screenshot", 
            command=self.take_screenshot,
            fg_color=("#4caf50", "#66bb6a"),
            hover_color=("#388e3c", "#4caf50"),
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        screenshot_button.pack(side="right", padx=(0, 10))
        
        # Modern add note button
        add_note_button = ctk.CTkButton(
            notes_input_frame, 
            text="➕ Add Note", 
            command=self.add_note,
            fg_color=("#ff9800", "#ffb74d"),
            hover_color=("#f57c00", "#ff9800"),
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        add_note_button.pack(side="right")
        
        # Modern notes text area
        self.notes_text = ctk.CTkTextbox(
            notes_frame, 
            wrap="word",
            fg_color=("#3a3a3a", "#2a2a2a"),
            text_color=("#ffffff", "#ffffff"),
            font=ctk.CTkFont(size=14),
            corner_radius=10,
            border_color=("#ff9800", "#ffb74d"),
            border_width=1
        )
        self.notes_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Screenshot viewer button
        view_screenshots_button = ctk.CTkButton(
            notes_frame, 
            text="🖼️ View Screenshots", 
            command=self.view_screenshots,
            fg_color=("#2196f3", "#42a5f5"),
            hover_color=("#1976d2", "#2196f3"),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        view_screenshots_button.pack(pady=(0, 20))
        
        # Settings tab with modern design
        settings_frame = ctk.CTkFrame(self.notebook, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # Settings header
        settings_header = ctk.CTkFrame(settings_frame, fg_color="transparent")
        settings_header.pack(fill="x", padx=20, pady=(20, 10))
        
        settings_title = ctk.CTkLabel(
            settings_header,
            text="🔧 Application Configuration",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("#607d8b", "#90a4ae")
        )
        settings_title.pack(anchor="w")
        
        # API key setting with modern design
        api_frame = ctk.CTkFrame(settings_frame, fg_color=("#3a3a3a", "#2a2a2a"), corner_radius=10)
        api_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        api_header = ctk.CTkLabel(
            api_frame,
            text="🔑 OpenAI API Configuration",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#4a9eff", "#66b3ff")
        )
        api_header.pack(anchor="w", padx=20, pady=(20, 15))
        
        api_input_frame = ctk.CTkFrame(api_frame, fg_color="transparent")
        api_input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        api_label = ctk.CTkLabel(
            api_input_frame, 
            text="API Key:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#ffffff", "#ffffff")
        )
        api_label.pack(side="left", padx=(0, 15))
        
        # Modern API key input
        self.api_key_entry = ctk.CTkEntry(
            api_input_frame, 
            placeholder_text="Enter your OpenAI API key...", 
            show="*", 
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color=("#2a2a2a", "#1a1a1a"),
            border_color=("#4a9eff", "#66b3ff"),
            border_width=2,
            corner_radius=10
        )
        self.api_key_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        if self.api_key:
            self.api_key_entry.insert(0, self.api_key)
        
        # Modern save API button
        save_api_button = ctk.CTkButton(
            api_input_frame, 
            text="💾 Save API Key", 
            command=self.save_api_key,
            fg_color=("#4a9eff", "#66b3ff"),
            hover_color=("#1976d2", "#4a9eff"),
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        save_api_button.pack(side="right")
        
        # Instructions section with modern design
        instructions_frame = ctk.CTkFrame(settings_frame, fg_color=("#3a3a3a", "#2a2a2a"), corner_radius=10)
        instructions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        instructions_header = ctk.CTkLabel(
            instructions_frame,
            text="📚 Quick Start Guide",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#4caf50", "#66bb6a")
        )
        instructions_header.pack(anchor="w", padx=20, pady=(20, 15))
        
        instructions_text = """
🎯 GETTING STARTED:

1️⃣ SETUP (First Time Only):
   • Enter your OpenAI API key above
   • Click 'Save API Key' to enable AI summaries

2️⃣ RECORD A MEETING:
   • Enter a descriptive meeting title
   • Click '🎙️ Start Recording' to begin
   • Speak clearly during the meeting
   • Click '⏹️ Stop Recording' when finished

3️⃣ PROCESS & SAVE:
   • Choose to save immediately or edit first
   • Click '🤖 Generate AI Summary' for AI-powered insights
   • Add manual notes and action items
   • Take screenshots with 📸 button during or after meeting
   • Click '💾 Save Meeting' to store everything

4️⃣ NEXT MEETING:
   • Interface automatically clears
   • Ready for your next recording!

💡 TIP: The app will ask if you want to save after stopping recording.
📸 TIP: Use the screenshot feature to capture important visual information!
"""
        
        instructions_label = ctk.CTkLabel(
            instructions_frame, 
            text=instructions_text, 
            justify="left",
            font=ctk.CTkFont(size=14),
            text_color=("#cccccc", "#cccccc")
        )
        instructions_label.pack(padx=20, pady=(0, 20))
    
    def create_menu(self):
        """Create the menu bar with help options"""
        # Create menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # File menu items
        file_menu.add_command(label="📂 Load Meeting", command=self.load_meeting)
        file_menu.add_command(label="💾 Save Meeting", command=self.save_meeting)
        file_menu.add_command(label="💾 Save As", command=self.save_meeting_as)
        file_menu.add_separator()
        file_menu.add_command(label="🔄 New Meeting", command=self.clear_old_recording)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Help menu items
        help_menu.add_command(label="📖 Quick Start Guide", command=self.show_quick_start)
        help_menu.add_command(label="🎯 How to Use", command=self.show_how_to_use)
        help_menu.add_command(label="⚙️ Settings Help", command=self.show_settings_help)
        help_menu.add_command(label="🔧 Troubleshooting", command=self.show_troubleshooting)
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ About", command=self.show_about)
        
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def clear_old_recording(self):
        """Clear old recording data and reset interface"""
        # Clear audio data
        self.audio_data = []
        
        # Clear transcript text
        self.transcript_text.delete("1.0", "end")
        
        # Clear summary text
        self.summary_text.delete("1.0", "end")
        
        # Clear notes text
        self.notes_text.delete("1.0", "end")
        
        # Reset meeting data
        self.current_meeting['transcript'] = []
        self.current_meeting['summary'] = ''
        self.current_meeting['notes'] = []
        self.current_meeting['screenshots'] = []
        
        # Reset button states
        self.summary_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.save_as_button.configure(state="disabled")
        
        # Reset status
        self.status_label.configure(text="✨ Ready to record your next meeting", text_color=("#4caf50", "#66bb6a"))
    
    def start_recording(self):
        if not self.title_entry.get().strip():
            messagebox.showerror("Error", "Please enter a meeting title first!")
            return
        
        # Clear old recording data
        self.clear_old_recording()
        
        self.is_recording = True
        self.current_meeting['title'] = self.title_entry.get().strip()
        self.current_meeting['start_time'] = datetime.now()
        self.current_meeting['transcript'] = []
        self.current_meeting['summary'] = ''
        
        self.record_button.configure(text="⏸️ Pause Recording", fg_color=("#ff9800", "#ffb74d"))
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="🔴 Recording in progress...", text_color=("#ff5252", "#ff7676"))
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self.record_audio)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
        # Start live transcription
        self.transcribe_live()
    
    def stop_recording(self):
        self.is_recording = False
        self.record_button.configure(text="🎙️ Start Recording", fg_color=("#00c853", "#00e676"))
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="🟡 Recording stopped", text_color=("#ff9800", "#ffb74d"))
        
        # Ask user if they want to save
        if self.current_meeting['transcript']:
            response = messagebox.askyesno(
                "Save Meeting?", 
                "Do you want to save this meeting?\n\nYes: Save and clear interface\nNo: Keep current data for editing"
            )
            
            if response:
                # User wants to save
                self.save_meeting()
            else:
                # User wants to keep data for editing
                self.status_label.configure(text="📝 Recording stopped - data ready for editing", text_color=("#4a9eff", "#66b3ff"))
                # Enable summary and save buttons for manual use
                self.summary_button.configure(state="normal")
                self.save_button.configure(state="normal")
                self.save_as_button.configure(state="normal")
        else:
            # No transcript, just enable buttons normally
            self.summary_button.configure(state="normal")
            self.save_button.configure(state="normal")
            self.save_as_button.configure(state="normal")
    
    def record_audio(self):
        """Record audio from system audio"""
        try:
            with sd.InputStream(callback=self.audio_callback, 
                              channels=1, 
                              samplerate=self.sample_rate,
                              dtype=np.float32):
                while self.is_recording:
                    time.sleep(0.1)
        except Exception as e:
            print(f"Audio recording error: {e}")
    
    def audio_callback(self, indata, frames, time, status):
        """Callback for audio recording"""
        if self.is_recording:
            self.audio_data.extend(indata.copy())
    
    def transcribe_live(self):
        """Live transcription of audio"""
        def transcribe_loop():
            while self.is_recording:
                try:
                    # Process audio in chunks
                    if len(self.audio_data) > self.sample_rate * 5:  # 5 second chunks
                        audio_chunk = np.array(self.audio_data[:self.sample_rate * 5])
                        self.audio_data = self.audio_data[self.sample_rate * 5:]
                        
                        # Convert to audio data
                        audio_data = sr.AudioData(
                            (audio_chunk * 32767).astype(np.int16).tobytes(),
                            self.sample_rate, 2
                        )
                        
                        # Transcribe
                        try:
                            text = self.recognizer.recognize_google(audio_data)
                            if text.strip():
                                timestamp = datetime.now().strftime("%H:%M:%S")
                                transcript_entry = f"[{timestamp}] {text}\n"
                                
                                self.current_meeting['transcript'].append({
                                    'timestamp': timestamp,
                                    'text': text
                                })
                                
                                # Update GUI in main thread
                                self.root.after(0, self.update_transcript, transcript_entry)
                                
                        except sr.UnknownValueError:
                            pass
                        except sr.RequestError as e:
                            print(f"Speech recognition error: {e}")
                    
                    time.sleep(1)
                except Exception as e:
                    print(f"Transcription error: {e}")
                    time.sleep(1)
        
        transcribe_thread = threading.Thread(target=transcribe_loop)
        transcribe_thread.daemon = True
        transcribe_thread.start()
    
    def update_transcript(self, text):
        """Update transcript text box"""
        self.transcript_text.insert("end", text)
        self.transcript_text.see("end")
    
    def generate_summary(self):
        """Generate AI summary of the meeting"""
        if not self.current_meeting['transcript']:
            messagebox.showwarning("Warning", "No transcript available to summarize!")
            return
        
        if not self.api_key:
            messagebox.showerror("Error", "OpenAI API key required for summaries!")
            return
        
        # Prepare transcript text
        transcript_text = "\n".join([f"[{entry['timestamp']}] {entry['text']}" 
                                   for entry in self.current_meeting['transcript']])
        
        try:
            self.status_label.configure(text="🤖 Generating AI summary...", text_color=("#ff9800", "#ffb74d"))
            
            # Use OpenAI to generate summary
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise, professional meeting summaries. Focus on key points, action items, and important decisions."},
                    {"role": "user", "content": f"Please summarize this meeting transcript:\n\n{transcript_text}"}
                ],
                max_tokens=500
            )
            
            summary = response.choices[0].message.content
            self.current_meeting['summary'] = summary
            
            # Update GUI
            self.summary_text.delete("1.0", "end")
            self.summary_text.insert("1.0", summary)
            
            self.status_label.configure(text="✅ AI summary generated successfully!", text_color=("#4caf50", "#66bb6a"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate summary: {str(e)}")
            self.status_label.configure(text="❌ Summary generation failed", text_color=("#ff5252", "#ff7676"))
    
    def add_note(self):
        """Add a manual note"""
        note_text = self.note_entry.get().strip()
        if note_text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            note_entry = f"[{timestamp}] {note_text}\n"
            
            self.current_meeting['notes'].append({
                'timestamp': timestamp,
                'text': note_text
            })
            
            self.notes_text.insert("end", note_entry)
            self.notes_text.see("end")
            self.note_entry.delete(0, "end")
    
    def take_screenshot(self):
        """Take a screenshot and add it to notes"""
        try:
            # Minimize the app window temporarily
            self.root.iconify()
            time.sleep(0.5)  # Wait for window to minimize
            
            # Take screenshot
            screenshot = ImageGrab.grab()
            
            # Restore the app window
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
            # Add screenshot to meeting data
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Convert to base64 for storage
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            screenshot_data = {
                'timestamp': timestamp,
                'image': img_str,
                'filename': f"screenshot_{timestamp.replace(':', '-')}.png"
            }
            
            self.current_meeting['screenshots'].append(screenshot_data)
            
            # Add screenshot entry to notes
            screenshot_entry = f"[{timestamp}] 📸 Screenshot captured: {screenshot_data['filename']}\n"
            self.notes_text.insert("end", screenshot_entry)
            self.notes_text.see("end")
            
            # Show success message
            self.status_label.configure(text="📸 Screenshot captured and added to notes!", text_color=("#4caf50", "#66bb6a"))
            
        except Exception as e:
            # Restore window if error occurs
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
            messagebox.showerror("Screenshot Error", f"Failed to take screenshot: {str(e)}")
            self.status_label.configure(text="❌ Screenshot failed", text_color=("#ff5252", "#ff7676"))
    
    def save_screenshot_to_file(self, screenshot_data, base_path):
        """Save screenshot to file"""
        try:
            # Create screenshots directory
            screenshots_dir = os.path.join(base_path, "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            
            # Decode and save image
            img_data = base64.b64decode(screenshot_data['image'])
            img = Image.open(io.BytesIO(img_data))
            
            filepath = os.path.join(screenshots_dir, screenshot_data['filename'])
            img.save(filepath, 'PNG')
            
            return filepath
        except Exception as e:
            print(f"Error saving screenshot: {e}")
            return None
    
    def view_screenshots(self):
        """Open a window to view all screenshots"""
        if not self.current_meeting['screenshots']:
            messagebox.showinfo("No Screenshots", "No screenshots have been taken yet.")
            return
        
        # Create screenshot viewer window
        viewer_window = ctk.CTkToplevel(self.root)
        viewer_window.title("🖼️ Screenshot Viewer")
        viewer_window.geometry("800x600")
        viewer_window.resizable(True, True)
        
        # Make it modal
        viewer_window.transient(self.root)
        viewer_window.grab_set()
        
        # Center the window
        viewer_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Create scrollable frame for screenshots
        main_frame = ctk.CTkScrollableFrame(viewer_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add title
        title_label = ctk.CTkLabel(
            main_frame,
            text="📸 Meeting Screenshots",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#4a9eff", "#66b3ff")
        )
        title_label.pack(pady=(0, 20))
        
        # Display each screenshot
        for i, screenshot_data in enumerate(self.current_meeting['screenshots']):
            # Screenshot container
            screenshot_frame = ctk.CTkFrame(main_frame, fg_color=("#3a3a3a", "#2a2a2a"), corner_radius=10)
            screenshot_frame.pack(fill="x", pady=(0, 20))
            
            # Screenshot header
            header_frame = ctk.CTkFrame(screenshot_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(15, 10))
            
            timestamp_label = ctk.CTkLabel(
                header_frame,
                text=f"📸 {screenshot_data['timestamp']} - {screenshot_data['filename']}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=("#4caf50", "#66bb6a")
            )
            timestamp_label.pack(side="left")
            
            # Image display
            try:
                # Decode base64 image
                img_data = base64.b64decode(screenshot_data['image'])
                img = Image.open(io.BytesIO(img_data))
                
                # Resize image to fit window (max width 700px)
                max_width = 700
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_width = int(img.width * ratio)
                    new_height = int(img.height * ratio)
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage for tkinter
                photo = ImageTk.PhotoImage(img)
                
                # Create label to display image
                img_label = ctk.CTkLabel(screenshot_frame, image=photo, text="")
                img_label.image = photo  # Keep a reference
                img_label.pack(pady=(0, 15))
                
            except Exception as e:
                error_label = ctk.CTkLabel(
                    screenshot_frame,
                    text=f"❌ Error displaying image: {str(e)}",
                    font=ctk.CTkFont(size=14),
                    text_color=("#ff5252", "#ff7676")
                )
                error_label.pack(pady=(0, 15))
        
        # Add close button
        close_button = ctk.CTkButton(
            viewer_window, 
            text="Close Viewer", 
            command=viewer_window.destroy,
            fg_color=("#4a9eff", "#66b3ff"),
            hover_color=("#1976d2", "#4a9eff"),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        close_button.pack(pady=(0, 20))
        
        # Focus on the viewer window
        viewer_window.focus_set()
    
    def save_meeting(self):
        """Save meeting data to file"""
        if not self.current_meeting['title']:
            messagebox.showerror("Error", "No meeting data to save!")
            return
        
        # Prepare meeting data
        meeting_data = {
            'title': self.current_meeting['title'],
            'start_time': self.current_meeting['start_time'].isoformat() if self.current_meeting['start_time'] else None,
            'end_time': datetime.now().isoformat(),
            'transcript': self.current_meeting['transcript'],
            'summary': self.current_meeting['summary'],
            'notes': self.current_meeting['notes'],
            'screenshots': self.current_meeting['screenshots']
        }
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"meeting_{timestamp}_{self.current_meeting['title'].replace(' ', '_')}.json"
        
        # Save to file
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(meeting_data, f, indent=2, ensure_ascii=False)
            
            # Save screenshots to separate folder if any exist
            if self.current_meeting['screenshots']:
                try:
                    # Create screenshots directory
                    screenshots_dir = f"screenshots_{timestamp}_{self.current_meeting['title'].replace(' ', '_')}"
                    os.makedirs(screenshots_dir, exist_ok=True)
                    
                    # Save each screenshot
                    for screenshot_data in self.current_meeting['screenshots']:
                        self.save_screenshot_to_file(screenshot_data, screenshots_dir)
                    
                    messagebox.showinfo("Success", f"Meeting saved as {filename}\nScreenshots saved to {screenshots_dir}/")
                except Exception as screenshot_error:
                    print(f"Warning: Could not save screenshots: {screenshot_error}")
                    messagebox.showinfo("Success", f"Meeting saved as {filename}\nNote: Screenshots could not be saved separately")
            else:
                messagebox.showinfo("Success", f"Meeting saved as {filename}")
            
            self.status_label.configure(text="💾 Meeting saved successfully!", text_color=("#4caf50", "#66bb6a"))
            
            # Clear interface after saving
            self.clear_interface_after_save()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save meeting: {str(e)}")
    
    def load_meeting(self):
        """Load an existing meeting from file"""
        try:
            # Open file dialog to select meeting file
            filename = filedialog.askopenfilename(
                title="Select Meeting File",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir="."
            )
            
            if not filename:
                return  # User cancelled
            
            # Load meeting data
            with open(filename, 'r', encoding='utf-8') as f:
                meeting_data = json.load(f)
            
            # Clear current interface
            self.clear_old_recording()
            
            # Load meeting data into interface
            self.current_meeting = {
                'title': meeting_data.get('title', ''),
                'start_time': datetime.fromisoformat(meeting_data['start_time']) if meeting_data.get('start_time') else None,
                'transcript': meeting_data.get('transcript', []),
                'summary': meeting_data.get('summary', ''),
                'notes': meeting_data.get('notes', []),
                'screenshots': meeting_data.get('screenshots', [])
            }
            
            # Update title entry
            self.title_entry.delete(0, "end")
            self.title_entry.insert(0, self.current_meeting['title'])
            
            # Update transcript text
            if self.current_meeting['transcript']:
                transcript_text = ""
                for entry in self.current_meeting['transcript']:
                    transcript_text += f"[{entry['timestamp']}] {entry['text']}\n"
                self.transcript_text.delete("1.0", "end")
                self.transcript_text.insert("1.0", transcript_text)
            
            # Update summary text
            if self.current_meeting['summary']:
                self.summary_text.delete("1.0", "end")
                self.summary_text.insert("1.0", self.current_meeting['summary'])
            
            # Update notes text
            if self.current_meeting['notes']:
                notes_text = ""
                for note in self.current_meeting['notes']:
                    notes_text += f"[{note['timestamp']}] {note['text']}\n"
                self.notes_text.delete("1.0", "end")
                self.notes_text.insert("1.0", notes_text)
            
            # Enable buttons for editing
            self.summary_button.configure(state="normal")
            self.save_button.configure(state="normal")
            self.save_as_button.configure(state="normal")
            
            # Update status
            self.status_label.configure(
                text=f"📂 Meeting loaded: {os.path.basename(filename)}", 
                text_color=("#4a9eff", "#66b3ff")
            )
            
            # Show success message
            messagebox.showinfo(
                "Meeting Loaded", 
                f"Successfully loaded meeting:\n\n"
                f"Title: {self.current_meeting['title']}\n"
                f"Transcript entries: {len(self.current_meeting['transcript'])}\n"
                f"Notes: {len(self.current_meeting['notes'])}\n"
                f"Screenshots: {len(self.current_meeting['screenshots'])}\n\n"
                f"You can now edit, add notes, take screenshots, or save changes."
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load meeting: {str(e)}")
            self.status_label.configure(text="❌ Failed to load meeting", text_color=("#ff5252", "#ff7676"))
    
    def save_meeting_as(self):
        """Save meeting data to a new file with custom filename"""
        if not self.current_meeting['title']:
            messagebox.showerror("Error", "No meeting data to save!")
            return
        
        try:
            # Open file dialog to choose save location and filename
            filename = filedialog.asksaveasfilename(
                title="Save Meeting As",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir=".",
                initialname=f"meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.current_meeting['title'].replace(' ', '_')}.json"
            )
            
            if not filename:
                return  # User cancelled
            
            # Prepare meeting data
            meeting_data = {
                'title': self.current_meeting['title'],
                'start_time': self.current_meeting['start_time'].isoformat() if self.current_meeting['start_time'] else None,
                'end_time': datetime.now().isoformat(),
                'transcript': self.current_meeting['transcript'],
                'summary': self.current_meeting['summary'],
                'notes': self.current_meeting['notes'],
                'screenshots': self.current_meeting['screenshots']
            }
            
            # Save to file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(meeting_data, f, indent=2, ensure_ascii=False)
            
            # Save screenshots to separate folder if any exist
            if self.current_meeting['screenshots']:
                try:
                    # Create screenshots directory
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshots_dir = f"screenshots_{timestamp}_{self.current_meeting['title'].replace(' ', '_')}"
                    os.makedirs(screenshots_dir, exist_ok=True)
                    
                    # Save each screenshot
                    for screenshot_data in self.current_meeting['screenshots']:
                        self.save_screenshot_to_file(screenshot_data, screenshots_dir)
                    
                    messagebox.showinfo("Success", f"Meeting saved as {filename}\nScreenshots saved to {screenshots_dir}/")
                except Exception as screenshot_error:
                    print(f"Warning: Could not save screenshots: {screenshot_error}")
                    messagebox.showinfo("Success", f"Meeting saved as {filename}\nNote: Screenshots could not be saved separately")
            else:
                messagebox.showinfo("Success", f"Meeting saved as {filename}")
            
            self.status_label.configure(text="💾 Meeting saved successfully!", text_color=("#4caf50", "#66bb6a"))
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save meeting: {str(e)}")
    
    def clear_interface_after_save(self):
        """Clear interface after saving meeting data"""
        # Clear title entry
        self.title_entry.delete(0, "end")
        
        # Clear all text areas
        self.transcript_text.delete("1.0", "end")
        self.summary_text.delete("1.0", "end")
        self.notes_text.delete("1.0", "end")
        
        # Reset meeting data
        self.current_meeting = {
            'title': '',
            'start_time': None,
            'transcript': [],
            'summary': '',
            'notes': [],
            'screenshots': []
        }
        
        # Reset button states
        self.record_button.configure(text="🎙️ Start Recording", fg_color=("#00c853", "#00e676"))
        self.stop_button.configure(state="disabled")
        self.summary_button.configure(state="disabled")
        self.save_button.configure(state="disabled")
        self.save_as_button.configure(state="disabled")
        
        # Reset status
        self.status_label.configure(text="✨ Ready to record your next meeting", text_color=("#4caf50", "#66bb6a"))
        
        # Clear audio data
        self.audio_data = []
    
    def save_api_key(self):
        """Save OpenAI API key"""
        api_key = self.api_key_entry.get().strip()
        if api_key:
            try:
                # Save to .env file
                with open('.env', 'w') as f:
                    f.write(f'OPENAI_API_KEY={api_key}')
                
                self.api_key = api_key
                openai.api_key = api_key
                
                messagebox.showinfo("Success", "API key saved successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save API key: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter an API key!")
    
    def show_quick_start(self):
        """Show quick start guide"""
        quick_start_text = """
🎯 QUICK START GUIDE

1️⃣ SETUP (First Time Only):
   • Go to Settings tab
   • Enter your OpenAI API key
   • Click 'Save API Key'

2️⃣ RECORD A MEETING:
   • Enter meeting title
   • Click '🎙️ Start Recording'
   • Speak clearly during meeting
   • Click '⏹️ Stop Recording'

3️⃣ SAVE & SUMMARIZE:
   • Choose to save immediately or edit first
   • Click '🤖 Generate AI Summary' (if you have API key)
   • Add notes if needed
   • Click '💾 Save Meeting'

4️⃣ LOAD & EDIT:
   • Use '📂 Load Meeting' to open saved meetings
   • Add more notes or take screenshots
   • Use '💾 Save As' to save changes with new filename

5️⃣ NEXT MEETING:
   • Interface automatically clears
   • Ready for new recording!

💡 TIP: The app will ask if you want to save after stopping recording.
📸 TIP: Use the screenshot feature to capture important visual information!
"""
        self.show_help_dialog("🚀 Quick Start Guide", quick_start_text)
    
    def show_how_to_use(self):
        """Show detailed how-to-use guide"""
        how_to_use_text = """
🎯 DETAILED USAGE GUIDE

📝 MEETING TITLE:
   • Enter a descriptive title for your meeting
   • This will be used in the saved filename
   • Example: "Weekly Team Standup - March 15"

🎙️ RECORDING:
   • Ensure your microphone is working
   • Speak clearly and avoid background noise
   • The app records in real-time
   • Live transcript appears as you speak

⏹️ STOPPING RECORDING:
   • App asks if you want to save immediately
   • YES: Saves and clears interface
   • NO: Keeps data for editing

📋 TRANSCRIPT:
   • View live transcript in real-time
   • Each entry shows timestamp
   • Edit manually if needed

🤖 AI SUMMARY:
   • Requires OpenAI API key
   • Generates professional meeting summary
   • Focuses on key points and action items
   • Can be edited before saving

✏️ NOTES:
   • Add manual notes during or after meeting
   • Each note is timestamped
   • Useful for action items or reminders

📸 SCREENSHOTS:
   • Click '📸 Screenshot' button to capture screen
   • App minimizes briefly to capture full screen
   • Screenshots are timestamped and stored
   • Use '🖼️ View Screenshots' to review all captures
   • Screenshots saved with meeting data

💾 SAVING:
   • Data saved as JSON file
   • Filename includes timestamp and title
   • Screenshots saved to separate folder
   • Interface automatically clears after saving
   • Ready for next meeting

📂 LOADING MEETINGS:
   • Use '📂 Load Meeting' button to open saved files
   • All data (transcript, notes, screenshots) is restored
   • Can add more notes or take additional screenshots
   • Use '💾 Save As' to save changes with new filename
   • Perfect for continuing work on previous meetings

🔄 WORKFLOW OPTIONS:
   Option 1: Record → Stop → Save → Clear
   Option 2: Record → Stop → Edit → Save → Clear
   Option 3: Load → Edit → Save As → Continue
   Option 4: Load → Add Notes/Screenshots → Save As
"""
        self.show_help_dialog("📚 How to Use", how_to_use_text)
    
    def show_settings_help(self):
        """Show settings help"""
        settings_text = """
⚙️ SETTINGS HELP

🔑 OPENAI API KEY:
   • Required for AI-powered summaries
   • Get one at: https://platform.openai.com/api-keys
   • Costs ~$0.01 per meeting summary
   • Key is saved locally in .env file

🎤 MICROPHONE SETTINGS:
   • Ensure microphone is enabled in Windows
   • Check microphone permissions
   • Test microphone in Windows settings
   • Close other apps using microphone

💾 FILE LOCATION:
   • Meetings saved in current directory
   • Filename format: meeting_YYYYMMDD_HHMMSS_Title.json
   • Can be moved or copied to other locations

🔧 TECHNICAL SETTINGS:
   • Sample rate: 44.1 kHz (CD quality)
   • Audio format: 16-bit PCM
   • Recording: System audio input
   • Transcription: Google Speech Recognition
"""
        self.show_help_dialog("⚙️ Settings Help", settings_text)
    
    def show_troubleshooting(self):
        """Show troubleshooting guide"""
        troubleshooting_text = """
🔧 TROUBLESHOOTING GUIDE

❌ NO AUDIO RECORDING:
   • Check microphone permissions
   • Ensure microphone is not muted
   • Close other audio applications
   • Restart the application

❌ TRANSCRIPTION NOT WORKING:
   • Check internet connection
   • Ensure clear speech
   • Reduce background noise
   • Try speaking louder

❌ CAN'T GENERATE SUMMARY:
   • Check OpenAI API key is set
   • Verify API key is valid
   • Check internet connection
   • Ensure you have API credits

❌ APP CRASHES:
   • Update Python packages
   • Check available disk space
   • Restart the application
   • Check Windows audio drivers

❌ POOR TRANSCRIPTION QUALITY:
   • Speak clearly and slowly
   • Reduce background noise
   • Use good quality microphone
   • Ensure stable internet

💡 COMMON SOLUTIONS:
   • Restart the application
   • Check Windows audio settings
   • Update audio drivers
   • Clear browser cache (if using web version)
"""
        self.show_help_dialog("🔧 Troubleshooting", troubleshooting_text)
    
    def show_about(self):
        """Show about information"""
        about_text = """
ℹ️ ABOUT MEETING SUMMARIZER PRO

🎯 PURPOSE:
   • Record and transcribe meetings
   • Generate AI-powered summaries
   • Save meeting data for future reference
   • Streamline meeting documentation

🛠️ TECHNOLOGIES:
   • Python with CustomTkinter GUI
   • Google Speech Recognition
   • OpenAI GPT for summaries
   • Real-time audio processing

📱 FEATURES:
   • Live audio recording
   • Real-time transcription
   • AI-powered summaries
   • Manual note taking
   • Automatic file saving
   • Clean interface reset
   • Modern, professional UI

👨‍💻 DEVELOPER:
   • Built with Python
   • Open source project
   • Designed for productivity
   • User-friendly interface

📄 LICENSE:
   • Free to use
   • Open source
   • Educational purposes
   • Personal and commercial use
"""
        self.show_help_dialog("ℹ️ About", about_text)
    
    def show_help_dialog(self, title, content):
        """Show a help dialog with the given content"""
        # Create help window
        help_window = ctk.CTkToplevel(self.root)
        help_window.title(title)
        help_window.geometry("700x600")
        help_window.resizable(True, True)
        
        # Make it modal (user must close it first)
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Center the window
        help_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Create text widget
        text_widget = ctk.CTkTextbox(
            help_window, 
            wrap="word",
            fg_color=("#2b2b2b", "#1a1a1a"),
            text_color=("#ffffff", "#ffffff"),
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        text_widget.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Insert content
        text_widget.insert("1.0", content)
        
        # Make text read-only
        text_widget.configure(state="disabled")
        
        # Add close button
        close_button = ctk.CTkButton(
            help_window, 
            text="Close", 
            command=help_window.destroy,
            fg_color=("#4a9eff", "#66b3ff"),
            hover_color=("#1976d2", "#4a9eff"),
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        )
        close_button.pack(pady=(0, 20))
        
        # Focus on the help window
        help_window.focus_set()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MeetingSummarizer()
    app.run()
