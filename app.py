import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

from main import run_pipeline
from core.rag_engine import ask_question

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
)

# ── Session state ─────────────────────────────────────────────────────────────
for key in ["result", "chat_history", "processed"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🎬 AI Video Assistant")
    st.caption("Powered by Whisper + Mistral + RAG")
    st.divider()

    st.subheader("Input")
    input_type = st.radio("Source type", ["YouTube URL", "Local Audio File"])

    source = None

    if input_type == "YouTube URL":
        source = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    else:
        uploaded = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a", "webm"])
        if uploaded:
            os.makedirs("downloads", exist_ok=True)
            save_path = os.path.join("downloads", uploaded.name)
            with open(save_path, "wb") as f:
                f.write(uploaded.read())
            source = save_path
            st.success(f"Saved: {uploaded.name}")

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    process_btn = st.button("🚀 Process", type="primary", use_container_width=True)

    # Show title after processing
    if st.session_state.result:
        st.divider()
        st.markdown(f"**{st.session_state.result['title']}**")
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.rerun()

# ── Pipeline trigger ──────────────────────────────────────────────────────────
if process_btn:
    if not source:
        st.warning("Please enter a YouTube URL or upload a file first.")
    else:
        st.session_state.chat_history = []
        with st.status("Processing...", expanded=True) as status:
            st.write("⬇️ Downloading / preparing audio...")
            st.write("🎙️ Transcribing with Whisper (this may take a few minutes)...")
            st.write("🤖 Summarising and extracting insights with Mistral AI...")
            st.write("🔍 Building RAG index for Q&A...")
            try:
                result = run_pipeline(source, language)
                st.session_state.result = result
                status.update(label="✅ Done!", state="complete")
            except Exception as e:
                status.update(label="❌ Failed", state="error")
                st.error(f"Error: {e}")

# ── Main content ──────────────────────────────────────────────────────────────
if st.session_state.result:
    result = st.session_state.result

    st.title(result["title"])
    st.divider()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Transcript",
        "📋 Summary",
        "✅ Action Items",
        "🏛️ Key Decisions",
        "❓ Open Questions",
        "💬 Chat",
    ])

    # ── Transcript ────────────────────────────────────────────────────────────
    with tab1:
        st.subheader("Full Transcript")
        st.text_area(
            label="transcript",
            value=result["transcript"],
            height=450,
            label_visibility="collapsed"
        )
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download as TXT",
                data=result["transcript"],
                file_name="transcript.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ── Summary ───────────────────────────────────────────────────────────────
    with tab2:
        st.subheader("Summary")
        st.markdown(result["summary"])

    # ── Action Items ──────────────────────────────────────────────────────────
    with tab3:
        st.subheader("Action Items")
        st.markdown(result["action_items"])

    # ── Key Decisions ─────────────────────────────────────────────────────────
    with tab4:
        st.subheader("Key Decisions")
        st.markdown(result["key_decisions"])

    # ── Open Questions ────────────────────────────────────────────────────────
    with tab5:
        st.subheader("Open Questions")
        st.markdown(result["open_questions"])

    # ── Chat ──────────────────────────────────────────────────────────────────
    with tab6:
        st.subheader("Chat with your video")
        st.caption("Ask anything about the content — powered by RAG")

        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_q = st.chat_input("Ask a question about the video...")

        if user_q:
            st.session_state.chat_history.append({"role": "user", "content": user_q})
            with st.chat_message("user"):
                st.markdown(user_q)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_question(result["rag_chain"], user_q)
                st.markdown(answer)

            st.session_state.chat_history.append({"role": "assistant", "content": answer})

else:
    # ── Welcome screen ────────────────────────────────────────────────────────
    st.title("🎬 AI Video Assistant")
    st.markdown("### What this app does:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🎙️ Transcribe**\nConverts any YouTube video or audio file to text using Whisper AI")
    with col2:
        st.info("**📋 Analyse**\nExtracts summary, action items, key decisions and open questions")
    with col3:
        st.info("**💬 Chat**\nAsk any question about the video using RAG-powered Q&A")

    st.markdown("---")
    st.markdown("👈 **Paste a YouTube URL or upload a file in the sidebar to get started.**")
