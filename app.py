import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

st.set_page_config(
    page_title="Summify · AI Document Summarizer",
    page_icon="✦",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

:root {
    --bg:         #08080F;
    --surface:    #0F0F1C;
    --surface2:   #141428;
    --border:     rgba(255,255,255,0.07);
    --border-lit: rgba(125,249,255,0.35);
    --white:      #F0F0FF;
    --muted:      #5A5A7A;
    --cyan:       #7DF9FF;
    --cyan-dim:   rgba(125,249,255,0.12);
    --purple:     #BF5FFF;
    --purple-dim: rgba(191,95,255,0.12);
    --pink:       #FF2D78;
    --pink-dim:   rgba(255,45,120,0.12);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    color: var(--white);
    background: var(--bg);
}

/* ── Remove Streamlit chrome ── */
.stApp > header, div[data-testid="stDecoration"],
.stAppDeployButton { display: none !important; }
#MainMenu, footer { visibility: hidden !important; }

/* ── App background — dark with subtle neon glow blobs ── */
.stApp {
    background-color: var(--bg);
    background-image:
        radial-gradient(ellipse 55% 40% at 10% 15%,  rgba(125,249,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 90% 10%,  rgba(191,95,255,0.07)  0%, transparent 60%),
        radial-gradient(ellipse 45% 40% at 80% 90%,  rgba(255,45,120,0.05)  0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 15% 85%,  rgba(125,249,255,0.04) 0%, transparent 55%);
    min-height: 100vh;
}

/* ── Container ── */
.main .block-container {
    max-width: 780px;
    padding-top: 0.8rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1.6rem;
    padding-right: 1.6rem;
}

label[data-testid="stWidgetLabel"] { display: none !important; }

/* ── Hero ── */
.hero { text-align: center; padding: 0.6rem 1rem 0.6rem; }

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--cyan-dim);
    color: var(--cyan);
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 999px;
    margin-bottom: 0.5rem;
    border: 1px solid rgba(125,249,255,0.3);
}

.hero-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 6px var(--cyan);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(1.2rem, 2.4vw, 1.75rem);
    font-weight: 800;
    line-height: 1.15;
    color: var(--white);
    margin-bottom: 0.35rem;
    white-space: nowrap;
    letter-spacing: -0.3px;
}

.hero-title .neon-cyan {
    background: linear-gradient(90deg, var(--cyan), var(--purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    color: var(--muted);
    font-size: 0.875rem;
    white-space: nowrap;
    text-align: center;
    font-weight: 400;
}

/* ── Section label ── */
.sec-label {
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.22rem;
    margin-top: 0.55rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

.sec-label span {
    color: var(--cyan);
    font-size: 0.7rem;
}

/* ── Select box ── */
.stSelectbox > div[data-baseweb="select"] > div {
    background:    var(--surface) !important;
    border:        1px solid var(--border) !important;
    border-radius: 10px !important;
    font-family:   'Space Grotesk', sans-serif !important;
    font-size:     0.92rem !important;
    color:         var(--white) !important;
    padding:       2px 8px !important;
    transition:    border-color 0.2s !important;
}

.stSelectbox > div[data-baseweb="select"] > div:hover {
    border-color: var(--border-lit) !important;
}

/* Dropdown menu */
ul[role="listbox"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

ul[role="listbox"] li {
    color: var(--white) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"] {
    background: var(--cyan-dim) !important;
    color: var(--cyan) !important;
}

/* ── File uploader — dark theme makes black natural ── */
section[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 0.55rem 1rem !important;
    box-shadow: none !important;
    transition: border-color 0.2s !important;
}

section[data-testid="stFileUploader"]:hover {
    border-color: var(--border-lit) !important;
}

section[data-testid="stFileUploader"] *:not(button):not(button *) {
    background:          transparent !important;
    background-color:    transparent !important;
    background-image:    none !important;
    border:              none !important;
    box-shadow:          none !important;
    color:               var(--muted) !important;
}

section[data-testid="stFileUploader"] > div,
section[data-testid="stFileUploader"] > div > div {
    display:        flex !important;
    flex-direction: row !important;
    align-items:    center !important;
    gap:            12px !important;
    flex-wrap:      nowrap !important;
    padding:        0 !important;
    margin:         0 !important;
}

section[data-testid="stFileUploader"] small { display: none !important; }

section[data-testid="stFileUploader"] button {
    background:    transparent !important;
    color:         var(--cyan) !important;
    border:        1px solid var(--cyan) !important;
    border-radius: 8px !important;
    font-family:   'Space Grotesk', sans-serif !important;
    font-weight:   600 !important;
    font-size:     0.82rem !important;
    padding:       5px 14px !important;
    white-space:   nowrap !important;
    flex-shrink:   0 !important;
    cursor:        pointer !important;
    box-shadow:    0 0 12px rgba(125,249,255,0.2) !important;
    transition:    all 0.2s !important;
}

section[data-testid="stFileUploader"] button * {
    color: var(--cyan) !important;
    background: transparent !important;
}

section[data-testid="stFileUploader"] button:hover {
    background:  var(--cyan-dim) !important;
    box-shadow:  0 0 20px rgba(125,249,255,0.35) !important;
}

/* ── Textarea ── */
textarea {
    background:    var(--surface) !important;
    border:        1px solid var(--border) !important;
    border-radius: 12px !important;
    padding:       12px 14px !important;
    font-size:     0.93rem !important;
    font-family:   'Space Grotesk', sans-serif !important;
    color:         var(--white) !important;
    line-height:   1.6 !important;
    resize:        vertical !important;
    box-shadow:    none !important;
    width:         100% !important;
    transition:    border-color 0.2s, box-shadow 0.2s !important;
    caret-color:   var(--cyan) !important;
}

textarea:focus {
    border-color: rgba(125,249,255,0.5) !important;
    box-shadow:   0 0 0 3px rgba(125,249,255,0.08), 0 0 20px rgba(125,249,255,0.06) !important;
    outline:      none !important;
}

textarea::placeholder { color: var(--muted) !important; }

/* ── Generate button — neon glow, truly full width ── */
.stButton, .stButton > button {
    width: 100% !important;
    display: block !important;
}

.stButton > button {
    background: transparent;
    color: var(--white);
    border: 1px solid var(--purple);
    border-radius: 10px;
    padding: 12px 20px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.97rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    cursor: pointer;
    transition: all 0.22s ease;
    box-shadow: 0 0 18px rgba(191,95,255,0.25), inset 0 0 18px rgba(191,95,255,0.04);
    margin-top: 0.3rem;
    text-shadow: 0 0 12px rgba(191,95,255,0.6);
}

.stButton > button:hover {
    background:  var(--purple-dim);
    border-color: var(--purple);
    box-shadow:   0 0 30px rgba(191,95,255,0.45), inset 0 0 24px rgba(191,95,255,0.08);
    transform:    translateY(-1px);
}

.stButton > button:active { transform: translateY(0); }

/* ── Download button ── */
.stDownloadButton > button {
    width: 100%;
    background:   transparent !important;
    color:        var(--cyan) !important;
    border:       1px solid var(--cyan) !important;
    border-radius: 10px !important;
    padding:      11px 20px !important;
    font-family:  'Space Grotesk', sans-serif !important;
    font-size:    0.92rem !important;
    font-weight:  600 !important;
    letter-spacing: 0.03em !important;
    box-shadow:   0 0 16px rgba(125,249,255,0.2) !important;
    transition:   all 0.22s ease !important;
    margin-top:   0.4rem;
    text-shadow:  0 0 10px rgba(125,249,255,0.5) !important;
}

.stDownloadButton > button:hover {
    background:  var(--cyan-dim) !important;
    box-shadow:  0 0 28px rgba(125,249,255,0.38) !important;
    transform:   translateY(-1px) !important;
}

/* ── Result card ── */
.result-card {
    background:    var(--surface);
    border:        1px solid var(--border-lit);
    border-radius: 12px;
    padding:       1.2rem;
    margin-top:    0.3rem;
    box-shadow:    0 0 24px rgba(125,249,255,0.06);
    line-height:   1.8;
    font-size:     0.92rem;
    color:         var(--white);
    max-height:    220px;
    overflow-y:    auto;
}

.result-card strong { color: var(--cyan); }
.result-card ul { padding-left: 1.2rem; }
.result-card li { margin-bottom: 0.3rem; }

.result-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 0.8rem;
    margin-bottom: 0.3rem;
}

.result-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 8px var(--cyan);
    flex-shrink: 0;
}

.result-label {
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--cyan);
}

/* ── Alerts ── */
.stSuccess > div {
    background: rgba(0,255,180,0.07) !important;
    border: 1px solid rgba(0,255,180,0.35) !important;
    border-radius: 10px !important;
    color: #00FFB4 !important;
    font-size: 0.85rem !important;
}

div[data-testid="stAlert"],
.stWarning, .stWarning > div, div[role="alert"] {
    background: var(--pink-dim) !important;
    border: 1px solid rgba(255,45,120,0.35) !important;
    border-radius: 10px !important;
    color: #FF6FA3 !important;
    font-size: 0.85rem !important;
}

.stWarning svg, div[role="alert"] svg { color: var(--pink) !important; fill: var(--pink) !important; }

.stError > div {
    background: rgba(255,45,45,0.08) !important;
    border: 1px solid rgba(255,80,80,0.35) !important;
    border-radius: 10px !important;
    color: #FF8080 !important;
    font-size: 0.85rem !important;
}

/* ── Spinner ── */
.stSpinner > div { color: var(--muted) !important; font-size: 0.85rem !important; }

/* ── Footer ── */
.footer {
    text-align: center;
    padding-top: 0.8rem;
    color: var(--muted);
    font-size: 0.72rem;
    letter-spacing: 0.05em;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(125,249,255,0.25); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(125,249,255,0.45); }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by AI</div>
    <div class="hero-title">Turn long docs into <span class="neon-cyan">clear summaries</span></div>
    <p class="hero-sub">Upload a PDF or paste any text — get structured summaries in seconds.</p>
</div>
""", unsafe_allow_html=True)

# ── SUMMARY FORMAT ────────────────────────────────────────────
st.markdown('<div class="sec-label"><span>⊹</span> Summary Format</div>', unsafe_allow_html=True)
summary_type = st.selectbox("", ["Bullet Points", "Short Summary", "Detailed Summary"])

# ── UPLOAD PDF ────────────────────────────────────────────────
st.markdown('<div class="sec-label"><span>↑</span> Upload PDF</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["pdf"])

# ── PASTE TEXT ────────────────────────────────────────────────
st.markdown('<div class="sec-label"><span>✎</span> Or Paste Text</div>', unsafe_allow_html=True)
text = st.text_area("", height=130, placeholder="Paste your document content here…")

# ── PDF EXTRACTION ────────────────────────────────────────────
pdf_text = ""
if uploaded_file is not None:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            pdf_text += extracted
    st.success("✅ PDF loaded — ready to summarise!")

final_text = pdf_text if pdf_text else text

# ── PROMPT BUILDER ────────────────────────────────────────────
def generate_prompt(summary_type, content):
    if summary_type == "Bullet Points":
        return f"""You are a professional AI document summarizer.
Read the following document and provide:
- Concise bullet point summary
- Key insights and takeaways
- Important decisions or findings
- Action items if present
Document:\n{content}"""
    elif summary_type == "Short Summary":
        return f"""Provide a short professional summary in 5–6 clear sentences.\nDocument:\n{content}"""
    else:
        return f"""Provide a detailed professional summary including overview, major points, key insights, conclusions.\nDocument:\n{content}"""

# ── GENERATE ──────────────────────────────────────────────────
if st.button("✦  Generate Summary"):
    if final_text.strip():
        with st.spinner("Thinking…"):
            try:
                prompt = generate_prompt(summary_type, final_text[:12000])
                response = client.chat.completions.create(
                    model="nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                    messages=[{"role": "user", "content": prompt}]
                )
                summary = response.choices[0].message.content

                st.markdown("""
                <div class="result-header">
                    <div class="result-dot"></div>
                    <div class="result-label">Generated Summary</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f'<div class="result-card">{summary}</div><br>', unsafe_allow_html=True)

                st.download_button(
                    label="⬇  Download as .txt",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("⚠  Please upload a PDF or paste some text first.")

# ── FOOTER ────────────────────────────────────────────────────
st.markdown('<div class="footer">SUMMIFY · PASTE · SUMMARIZE · DONE</div>', unsafe_allow_html=True)
