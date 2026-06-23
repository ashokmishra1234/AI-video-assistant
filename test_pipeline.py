from utils.audio_processor import download_youtube_audio, chunk_audio
from core.transcriber import transcribe_all
from core.summariser import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions

# Step 1: Download audio from YouTube (short video for testing)
print("=" * 40)
print("STEP 1: Downloading audio...")
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
wav_file = download_youtube_audio(url)
print(f"Downloaded: {wav_file}")

# Step 2: Split into chunks
print("=" * 40)
print("STEP 2: Splitting into chunks...")
chunks = chunk_audio(wav_file)
print(f"Total chunks: {len(chunks)}")

# Step 3: Transcribe
print("=" * 40)
print("STEP 3: Transcribing...")
transcript = transcribe_all(chunks)
print("Transcript:")
print(transcript)

# Step 4: Summarize
print("=" * 40)
print("STEP 4: Summarizing...")
summary = summarize(transcript)
print("Summary:")
print(summary)

# Step 5: Generate Title
print("=" * 40)
print("STEP 5: Generating Title...")
title = generate_title(transcript)
print("Title:")
print(title)

# Step 6: Extract Action Items
print("=" * 40)
print("STEP 6: Extracting Action Items...")
action_items = extract_action_items(transcript)
print("Action Items:")
print(action_items)

# Step 7: Extract Key Decisions
print("=" * 40)
print("STEP 7: Extracting Key Decisions...")
key_decisions = extract_key_decisions(transcript)
print("Key Decisions:")
print(key_decisions)

# Step 8: Extract Questions
print("=" * 40)
print("STEP 8: Extracting Questions...")
questions = extract_questions(transcript)
print("Questions:")
print(questions)