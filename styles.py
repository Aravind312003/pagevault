def inject_css():
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Crimson+Pro:ital,wght@0,300;0,400;0,600;1,400&display=swap');

/* ── ROOT VARS ── */
:root {
    --bg-primary: #0d1117;
    --bg-secondary: #161b22;
    --bg-card: #1a2030;
    --bg-hover: #1f2840;
    --gold: #c9a84c;
    --gold-light: #e6c87a;
    --gold-dim: #a08030;
    --cream: #f0e6d3;
    --cream-dim: #b8a99a;
    --text-muted: #8b9bb4;
    --border: #2a3448;
    --red: #e05252;
    --green: #52b788;
    --purple: #9d6db5;
    --blue: #4a9eda;
    --orange: #e8834a;
    --teal: #4ac4b7;
}

/* ── GLOBAL ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--cream) !important;
    font-family: 'Crimson Pro', Georgia, serif !important;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--cream) !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── HEADINGS ── */
h1, h2, h3, h4 {
    font-family: 'Playfair Display', serif !important;
    color: var(--gold) !important;
}

/* ── INPUTS ── */
input, textarea, select,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    background-color: var(--bg-card) !important;
    color: var(--cream) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'Crimson Pro', serif !important;
}

input:focus, textarea:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.2) !important;
}

/* ── SELECT BOX ── */
[data-baseweb="select"] > div {
    background-color: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--cream) !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, var(--gold-dim), var(--gold)) !important;
    color: #0d1117 !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.5rem !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--gold), var(--gold-light)) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.4) !important;
}

/* ── BOOK CARD ── */
.book-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: pointer;
    height: 100%;
    position: relative;
}

.book-card:hover {
    border-color: var(--gold);
    transform: translateY(-4px);
    box-shadow: 0 8px 32px rgba(201,168,76,0.25), 0 2px 8px rgba(0,0,0,0.5);
}

.book-cover {
    width: 100%;
    height: 220px;
    object-fit: cover;
    display: block;
}

.book-cover-placeholder {
    width: 100%;
    height: 220px;
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-hover));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}

.book-info {
    padding: 14px;
}

.book-title {
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--cream);
    margin: 0 0 4px 0;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.book-author {
    font-size: 0.85rem;
    color: var(--cream-dim);
    margin: 0 0 8px 0;
    font-style: italic;
}

.star-display {
    color: var(--gold);
    font-size: 0.85rem;
    margin-bottom: 6px;
}

/* ── GENRE BADGE ── */
.genre-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'Crimson Pro', serif;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}

.genre-dark-romance { background: rgba(157,109,181,0.25); color: #c49ee0; border: 1px solid rgba(157,109,181,0.4); }
.genre-romance { background: rgba(224,82,130,0.2); color: #f0789a; border: 1px solid rgba(224,82,130,0.35); }
.genre-horror { background: rgba(224,82,82,0.2); color: #e87878; border: 1px solid rgba(224,82,82,0.35); }
.genre-thriller { background: rgba(232,131,74,0.2); color: #f0a070; border: 1px solid rgba(232,131,74,0.35); }
.genre-mystery { background: rgba(74,158,218,0.2); color: #78b8e8; border: 1px solid rgba(74,158,218,0.35); }
.genre-fantasy { background: rgba(82,183,136,0.2); color: #78d0a8; border: 1px solid rgba(82,183,136,0.35); }
.genre-sci-fi { background: rgba(74,196,183,0.2); color: #78ddd0; border: 1px solid rgba(74,196,183,0.35); }
.genre-other { background: rgba(139,155,180,0.2); color: #aabbcc; border: 1px solid rgba(139,155,180,0.35); }

/* ── HERO BANNER ── */
.hero-banner {
    background: linear-gradient(135deg, #0d1117 0%, #1a1520 40%, #1a2030 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    text-align: center;
}

.hero-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 60% 50%, rgba(201,168,76,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: var(--gold);
    margin: 0 0 0.5rem 0;
    text-shadow: 0 2px 20px rgba(201,168,76,0.3);
    letter-spacing: 2px;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: var(--cream-dim);
    font-style: italic;
    margin: 0;
}

/* ── STAT CARD ── */
.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
}

.stat-card:hover { border-color: var(--gold-dim); }

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--gold);
    line-height: 1;
    margin-bottom: 0.4rem;
}

.stat-label {
    font-size: 0.9rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── SECTION HEADER ── */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--gold);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.6rem;
    margin-bottom: 1.5rem;
}

/* ── REVIEW CARD ── */
.review-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}

.review-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}

.reviewer-name {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    color: var(--gold);
    font-size: 0.95rem;
}

.review-date {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.review-text {
    color: var(--cream-dim);
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
}

/* ── ALERT ── */
.alert-success {
    background: rgba(82,183,136,0.15);
    border: 1px solid rgba(82,183,136,0.4);
    color: #78d0a8;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}

.alert-error {
    background: rgba(224,82,82,0.15);
    border: 1px solid rgba(224,82,82,0.4);
    color: #e87878;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}

.alert-info {
    background: rgba(74,158,218,0.15);
    border: 1px solid rgba(74,158,218,0.4);
    color: #78b8e8;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}

/* ── STATUS BADGE ── */
.status-pending {
    background: rgba(232,131,74,0.2);
    color: #f0a070;
    border: 1px solid rgba(232,131,74,0.4);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status-fulfilled {
    background: rgba(82,183,136,0.2);
    color: #78d0a8;
    border: 1px solid rgba(82,183,136,0.4);
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

/* ── TABS ── */
[data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border) !important;
}

[data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-family: 'Crimson Pro', serif !important;
}

[aria-selected="true"] {
    color: var(--gold) !important;
    border-bottom: 2px solid var(--gold) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--gold-dim); }

/* ── SIDEBAR NAV BUTTON ── */
.nav-btn {
    display: block;
    width: 100%;
    background: transparent;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    text-align: left;
    color: var(--cream-dim);
    font-family: 'Crimson Pro', serif;
    font-size: 1.05rem;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 4px;
}

.nav-btn:hover, .nav-btn.active {
    background: rgba(201,168,76,0.12);
    color: var(--gold);
}

/* ── DETAIL PAGE ── */
.book-detail-cover {
    border-radius: 10px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
    width: 100%;
    max-width: 280px;
}

.book-detail-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 900;
    color: var(--cream);
    margin-bottom: 0.25rem;
    line-height: 1.2;
}

.book-detail-author {
    font-size: 1.15rem;
    color: var(--gold);
    font-style: italic;
    margin-bottom: 1rem;
}

.book-detail-desc {
    color: var(--cream-dim);
    line-height: 1.8;
    font-size: 1.05rem;
}

/* Stray white backgrounds fix */
[data-testid="stMarkdownContainer"],
[data-testid="stVerticalBlock"],
[data-testid="column"] {
    background: transparent !important;
}
</style>
"""