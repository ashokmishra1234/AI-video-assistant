# 🎬 AI Video Assistant

An AI-powered tool that transcribes YouTube videos or local audio files, summarises the content, extracts key insights, and lets you chat with the video using RAG (Retrieval-Augmented Generation).

---

## ✨ Features

- 🎙️ **Transcription** — Converts YouTube videos or local audio files to text using OpenAI Whisper (runs locally)
- 📋 **Summary** — Generates a concise bullet-point summary using Mistral AI
- ✅ **Action Items** — Extracts tasks, owners, and deadlines from the transcript
- 🏛️ **Key Decisions** — Lists all important decisions made
- ❓ **Open Questions** — Identifies unresolved topics needing follow-up
- 💬 **RAG Chat** — Ask any question about the video and get accurate answers powered by ChromaDB + Mistral
- 🌐 **Hinglish Support** — Works with Hindi/English mixed audio

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Speech-to-Text | OpenAI Whisper (local) |
| LLM | Mistral AI (`mistral-small-latest`) |
| LLM Orchestration | LangChain LCEL |
| Vector Store | ChromaDB |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Audio Download | yt-dlp |
| Audio Processing | pydub + FFmpeg |

---

## 📁 Project Structure

```
AI-video-assistant-project/
│
├── app.py                  # Streamlit UI
├── main.py                 # Core pipeline (run_pipeline function)
├── requirements.txt        # Python dependencies
├── packages.txt            # System dependencies (FFmpeg for deployment)
├── .env                    # API keys (never commit this)
│
├── utils/
│   └── audio_processor.py  # Download, convert, and chunk audio
│
├── core/
│   ├── transcriber.py      # Whisper transcription
│   ├── summariser.py       # Summarisation (Map-Reduce)
│   ├── extractor.py        # Action items, decisions, questions
│   ├── rag_engine.py       # RAG pipeline for Q&A
│   └── vector_score.py     # ChromaDB vector store
│
└── downloads/              # Audio files saved here (auto-created)
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-video-assistant.git
cd ai-video-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

**Windows:**
```bash
winget install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 5. Set up your API key

Create a `.env` file in the project root:
```
MISTRAL_API_KEY=your_mistral_api_key_here
```

Get your free Mistral API key at [console.mistral.ai](https://console.mistral.ai)

### 6. Run the app

```bash
streamlit run app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push the project to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set `MISTRAL_API_KEY` in **Advanced Settings → Secrets**
5. Click **Deploy**

---

## 🔄 How It Works

```
YouTube URL / Local File
        ↓
   yt-dlp / pydub
 (download & convert)
        ↓
   chunk_audio()
 (split into 10min parts)
        ↓
   Whisper (local)
   (transcribe each chunk)
        ↓
   Full Transcript
        ↓
   ┌────────────────────────────────┐
   │  Mistral AI (via LangChain)   │
   ├────────────┬───────────────────┤
   │  Summary   │  Action Items     │
   │  Title     │  Key Decisions    │
   │            │  Open Questions   │
   └────────────┴───────────────────┘
        ↓
   ChromaDB (vector store)
   + HuggingFace Embeddings
        ↓
   RAG Q&A Chat
```

---

## ⚠️ Notes

- Whisper `small` model (~250MB) is downloaded on first run automatically
- Large videos (>1 hour) may take several minutes to transcribe
- All audio files are saved in the `downloads/` folder
- ChromaDB index is saved in `vector_db/` folder

---

## 📄 License

MIT License — free to use and modify.
