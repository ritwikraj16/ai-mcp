# 🎬 Video RAG Usage Guide

This guide will help you get started with the Video RAG demo using Google's Gemini API.

## Quick Start

### 1. Setup Environment

```bash
# Clone or navigate to the video-rag-gemini directory
cd video-rag-gemini

# Install dependencies
pip install -r requirements.txt

# Test your setup
python test_setup.py
```

### 2. Set Up Your API Key

1.  **Get a Gemini API Key**:
    *   Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create a new API key.

2.  **Set the Environment Variable**:
    *   Create a file named `.env` in the project's root directory.
    *   Add your Gemini API key to this file:
        ```
        GEMINI_API_KEY='your_gemini_api_key_here'
        ```
    *   **Important**: The application reads the key from this file. Your friends or end-users will not need to enter a key.

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Using the App

### Step 1: Upload Video
- Click "Choose a video file" in the sidebar
- Supported formats: MP4, AVI, MOV, MKV, WEBM
- File size limit: ~100MB (larger files may fail)
- Wait for the video to be processed (this can take several minutes)

### Step 2: Start Chatting
- Once processing is complete, you'll see example questions
- Click on example questions or type your own
- Ask anything about the video content!

## Example Questions

### General Analysis
- "What is happening in this video?"
- "Summarize the main events"
- "Describe the overall scene"

### People & Objects
- "Who are the people in this video?"
- "What objects can you see?"
- "Describe the clothing or appearance of people"

### Actions & Events
- "What actions are taking place?"
- "What is the sequence of events?"
- "What happens at the beginning/middle/end?"

### Environment & Setting
- "What is the setting or location?"
- "Describe the environment"
- "What time of day is it?"

### Specific Details
- "What colors are prominent in the video?"
- "What sounds might be present?" (Note: Gemini analyzes visual content)
- "What emotions are expressed?"

## Tips for Best Results

### Video Quality
- Use clear, well-lit videos
- Avoid very shaky or blurry footage
- Higher resolution generally works better

### Question Types
- Be specific in your questions
- Ask about visual elements (Gemini can't hear audio)
- Break complex questions into simpler parts

### File Management
- Keep video files under 100MB when possible
- Use common formats (MP4 is most reliable)
- Compress large files if needed

## Troubleshooting

### Common Issues

**"Error uploading video"**
- Check file format and size
- Ensure stable internet connection
- Try a different video file

**"Video processing failed"**
- File may be too large or corrupted
- Try compressing the video
- Check if format is supported

**"Error generating response"**
- API key may be invalid or expired
- Check your API quota/billing
- Try a simpler question first

**App is slow or unresponsive**
- Large videos take time to process
- Wait a few minutes before trying again
- Refresh the page if needed

### Getting Help

1. **Check Setup**: Run `python test_setup.py`
2. **Verify API Key**: Make sure it's correct and has quota
3. **Test with Small Video**: Try a short, small video first
4. **Check Logs**: Look at the Streamlit terminal for error messages

## Advanced Usage

### Command Line Demo
```bash
# Run the command-line demo
python demo.py
```

### Environment Variables
```bash
# Set API key for session
export GEMINI_API_KEY=your_key_here

# Run app
streamlit run app.py
```

### Custom Configuration
You can modify `app.py` to:
- Change the Gemini model (e.g., gemini-1.5-flash for faster responses)
- Adjust file size limits
- Customize the UI theme
- Add additional video formats

## API Limits & Costs

- **Free Tier**: Limited requests per minute/day
- **File Size**: ~100MB per file
- **Processing Time**: Varies by video length and complexity
- **Rate Limits**: May need to wait between requests

Check [Gemini API pricing](https://ai.google.dev/pricing) for current limits and costs.

## Security Notes

- Never share your API key publicly
- Use environment variables for production
- The app doesn't store videos permanently
- Videos are uploaded to Google's servers for processing

---

*Happy video chatting! 🎬✨*

