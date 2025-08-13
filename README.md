# �� Meeting Summarizer Pro

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](CONTRIBUTING.md)

**AI-Powered Meeting Documentation & Analysis Tool**

A professional desktop application that records, transcribes, and summarizes meetings using AI. Perfect for professionals, teams, and anyone who needs comprehensive meeting documentation.

## ✨ Features

### 🎙️ **Audio Recording & Transcription**
- Real-time audio recording from system audio
- Live transcription using Google Speech Recognition
- Timestamped transcript entries
- High-quality audio processing

### 🤖 **AI-Powered Summaries**
- OpenAI GPT integration for intelligent summaries
- Focus on key points and action items
- Professional meeting documentation
- Customizable summary length

### 📸 **Screenshot Integration**
- Capture important visual information during meetings
- Automatic timestamping and organization
- Screenshot viewer with scrollable interface
- Integrated with meeting data

### ✏️ **Comprehensive Note Taking**
- Manual note entry with timestamps
- Action item tracking
- Rich text formatting
- Searchable content

### 💾 **Advanced File Management**
- Load existing meetings for editing
- Save meetings with custom filenames
- Export to JSON format
- Separate screenshot storage

### 🎨 **Modern User Interface**
- Dark mode with professional styling
- Intuitive tabbed interface
- Responsive design
- Cross-platform compatibility

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (primary support)
- Microphone access
- Internet connection for transcription and AI features

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/satishkkrishnan/meeting-summarizer.git
   cd meeting-summarizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key** (optional, for AI summaries)
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Run the application and enter it in Settings tab
   - Or create a `.env` file with: `OPENAI_API_KEY=your_key_here`

4. **Run the application**
   ```bash
   python meeting_summarizer.py
   ```

## 📖 Usage Guide

### 🎯 **Basic Workflow**

1. **Start a Meeting**
   - Enter meeting title
   - Click "🎙️ Start Recording"
   - Speak clearly during your meeting
   - Click "⏹️ Stop Recording" when finished

2. **Process & Save**
   - Review transcript
   - Generate AI summary (if API key is set)
   - Add notes and take screenshots
   - Save meeting data

3. **Load & Edit**
   - Use "📂 Load Meeting" to open saved files
   - Add more notes or screenshots
   - Save changes with "💾 Save As"

### 🔧 **Advanced Features**

- **Screenshots**: Click "📸 Screenshot" to capture screen content
- **AI Summaries**: Requires OpenAI API key for intelligent analysis
- **File Management**: Organize meetings with custom naming
- **Export Options**: Save in JSON format for further processing

## 🛠️ Technical Details

### **Architecture**
- **Frontend**: CustomTkinter (modern Tkinter)
- **Audio Processing**: sounddevice, scipy
- **Speech Recognition**: Google Speech Recognition API
- **AI Integration**: OpenAI GPT API
- **Image Processing**: Pillow (PIL)

### **Data Structure**
```json
{
  "title": "Meeting Title",
  "start_time": "2024-01-01T10:00:00",
  "end_time": "2024-01-01T11:00:00",
  "transcript": [
    {"timestamp": "10:05:00", "text": "Meeting content..."}
  ],
  "summary": "AI-generated summary...",
  "notes": [
    {"timestamp": "10:10:00", "text": "Action item..."}
  ],
  "screenshots": [
    {"timestamp": "10:15:00", "image": "base64_encoded_image", "filename": "screenshot.png"}
  ]
}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **How to Contribute**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Development Setup**

1. **Clone and setup**
   ```bash
   git clone https://github.com/satishkkrishnan/meeting-summarizer.git
   cd meeting-summarizer
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

2. **Run tests**
   ```bash
   python -m pytest tests/
   ```

3. **Code style**
   ```bash
   black meeting_summarizer.py
   flake8 meeting_summarizer.py
   ```

## 📋 Requirements

### **Core Dependencies**
- `customtkinter>=5.2.0` - Modern GUI framework
- `speech_recognition>=3.10.0` - Speech recognition
- `openai>=1.3.0` - AI integration
- `Pillow>=10.0.1` - Image processing
- `sounddevice>=0.4.6` - Audio recording
- `scipy>=1.11.0` - Scientific computing
- `numpy>=1.26.0` - Numerical computing

### **System Requirements**
- **OS**: Windows 10/11 (primary), Linux/macOS (experimental)
- **Python**: 3.8+
- **Memory**: 4GB RAM minimum
- **Storage**: 100MB free space
- **Audio**: Working microphone

## 🐛 Troubleshooting

### **Common Issues**

1. **No Audio Recording**
   - Check microphone permissions
   - Ensure microphone is not muted
   - Close other audio applications

2. **Transcription Not Working**
   - Verify internet connection
   - Check microphone quality
   - Reduce background noise

3. **AI Summary Fails**
   - Verify OpenAI API key
   - Check API credits
   - Ensure stable internet

### **Getting Help**

- 📖 Check the [Wiki](https://github.com/satishkkrishnan/meeting-summarizer/wiki)
- 🐛 Report bugs via [Issues](https://github.com/satishkkrishnan/meeting-summarizer/issues)
- 💬 Join discussions in [Discussions](https://github.com/satishkkrishnan/meeting-summarizer/discussions)
- 📧 Contact: your.email@example.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **CustomTkinter** - Modern GUI framework
- **Google Speech Recognition** - Speech-to-text capabilities
- **OpenAI** - AI-powered summaries
- **Pillow** - Image processing capabilities
- **Open Source Community** - For inspiration and support

## 📊 Project Status

- **Version**: 1.0.0
- **Status**: Active Development
- **Last Updated**: January 2024
- **Maintainer**: [Satish Krishnan](https://github.com/satishkkrishnan)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=satishkkrishnan/meeting-summarizer&type=Date)](https://star-history.com/#satishkkrishnan/meeting-summarizer&Date)

---

**Made with ❤️ by the Meeting Summarizer Team**

If this project helps you, please give it a ⭐ star on GitHub!
