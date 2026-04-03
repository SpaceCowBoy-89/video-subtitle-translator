# Video Subtitle Translator

A Python desktop GUI application that translates and adds subtitles to videos using DeepL API and OpenAI Whisper.

## Features

- **Multiple subtitle sources**: Auto-detect, Whisper speech recognition, or embedded subtitles
- **DeepL translation**: High-quality translation supporting 30+ languages
- **Batch processing**: Process multiple files sequentially
- **Subtitle burning**: Optionally burn subtitles into video files
- **Drag-and-drop**: Easy file management
- **Multiple formats**: SRT and VTT subtitle formats

## Requirements

- Python 3.8+
- ffmpeg (for video processing and subtitle burning)
- DeepL API key (get one at https://www.deepl.com/pro-api)

## Installation

### Option 1: Standalone Application (Recommended for macOS)

Build a double-clickable .app bundle:

1. **Install ffmpeg**:
   ```bash
   brew install ffmpeg
   ```

2. **Run the build script**:
   ```bash
   ./build.sh
   ```

3. **Launch the application**:
   - Open `dist/Video Subtitle Translator.app` by double-clicking
   - Or copy to Applications: `cp -r "dist/Video Subtitle Translator.app" /Applications/`

See [BUILD.md](BUILD.md) for detailed build instructions and troubleshooting.

### Option 2: Run from Terminal

1. **Install ffmpeg** (if not already installed):
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - Windows: Download from https://ffmpeg.org/download.html

2. **Clone or download this repository**

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Standalone Application
Double-click **Video Subtitle Translator.app** (after building)

### Terminal
```bash
python main.py
```

2. **Configure settings** (first time):
   - Go to **Settings → Preferences**
   - Enter your DeepL API key
   - Choose Whisper model size (default: base)
   - Optionally set a default output directory

3. **Process files**:
   - Select source and target languages
   - Add files by clicking "Add Files..." or drag-and-drop
   - Choose subtitle source (Auto/Whisper/Embedded)
   - Select output format (SRT/VTT)
   - Optionally enable "Burn subtitles into video"
   - Click "Start"

## Supported File Types

- **Video**: .mp4, .mkv, .avi, .mov, .webm, .flv, .wmv
- **Subtitles**: .srt, .vtt

## How It Works

1. **Subtitle Extraction**:
   - For subtitle files: loads directly
   - For videos with "Auto": checks for embedded subtitles first, falls back to Whisper
   - For videos with "Whisper": transcribes audio using OpenAI Whisper
   - For videos with "Embedded": extracts embedded subtitle track

2. **Translation**: Uses DeepL API to translate subtitles in batches

3. **Output**:
   - Saves translated subtitles as `{filename}.{lang}.srt` or `.vtt`
   - Optionally burns subtitles into video as `{filename}.{lang}.{ext}`

## Whisper Models

Choose based on your needs (accuracy vs. speed):
- **tiny**: Fastest, lowest accuracy (~1GB VRAM)
- **base**: Fast, good for simple speech (~1GB VRAM)
- **small**: Balanced (~2GB VRAM)
- **medium**: High accuracy (~5GB VRAM)
- **large**: Best accuracy, slowest (~10GB VRAM)

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

## Project Structure

```
Translator/
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
├── app/
│   ├── config.py           # Settings management
│   ├── languages.py        # Language mappings
│   ├── core/               # Business logic (no GUI dependencies)
│   │   ├── subtitle_parser.py
│   │   ├── translator.py
│   │   ├── transcriber.py
│   │   ├── extractor.py
│   │   ├── burner.py
│   │   └── pipeline.py
│   ├── workers/            # Background threading
│   │   ├── base_worker.py
│   │   ├── pipeline_worker.py
│   │   └── batch_worker.py
│   └── gui/                # PySide6 UI components
│       ├── main_window.py
│       ├── file_list_widget.py
│       ├── settings_dialog.py
│       ├── progress_panel.py
│       └── language_selector.py
└── tests/                  # Unit tests
```

## Troubleshooting

### "ffmpeg not found"
- Install ffmpeg and ensure it's in your system PATH
- Video burning will be disabled without ffmpeg
- Subtitle extraction and translation still work

### "DeepL API Error"
- Verify your API key in Settings
- Check your DeepL account has available characters
- Ensure you're using the correct API key type (Free vs. Pro)

### Slow Whisper transcription
- Try a smaller model (tiny/base) for faster processing
- Whisper uses GPU if available (CUDA/Metal)
- Transcription time depends on video length and model size

### Out of memory
- Use a smaller Whisper model
- Process files one at a time instead of batch
- Close other applications to free up RAM/VRAM

## License

This project is for educational purposes. Ensure you comply with:
- DeepL API Terms of Service
- OpenAI Whisper license
- ffmpeg license

## Credits

Built with:
- [PySide6](https://pypi.org/project/PySide6/) - Qt for Python
- [DeepL Python Library](https://github.com/DeepLcom/deepl-python)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [ffmpeg](https://ffmpeg.org/)
- [pysrt](https://github.com/byroot/pysrt)
