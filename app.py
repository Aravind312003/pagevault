import streamlit as st
from database import init_db, get_featured_books, get_avg_rating
from styles import inject_css
from auth import show_auth_page
from library import show_library_page, get_cover_html, genre_badge, stars_html
from reader import show_book_detail, show_reader
from profile import show_profile_page
from requests_page import show_request_page
from admin import show_admin_dashboard

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PageVault",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_db()
st.markdown(inject_css(), unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── AUTH GATE ─────────────────────────────────────────────────────────────────
if not st.session_state.user:
    show_auth_page()
    st.stop()

user = st.session_state.user
is_admin = user.get("role") == "admin"

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding:1.5rem 0 1rem 0;'>
        <div style='font-family:Playfair Display,serif; font-size:1.8rem; font-weight:900;
                    color:#c9a84c; letter-spacing:2px;'>📚 PageVault</div>
        <div style='color:#8b9bb4; font-size:0.82rem; margin-top:4px; font-style:italic;'>Your personal library</div>
    </div>
    <hr style='border-color:#2a3448; margin:0 0 1rem 0;'/>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:rgba(201,168,76,0.08); border:1px solid rgba(201,168,76,0.2);
                border-radius:10px; padding:0.75rem 1rem; margin-bottom:1.25rem;
                display:flex; align-items:center; gap:0.75rem;'>
        <div style='width:36px; height:36px; border-radius:50%;
                    background:linear-gradient(135deg,#c9a84c,#a08030);
                    display:flex; align-items:center; justify-content:center;
                    font-weight:700; color:#0d1117; flex-shrink:0;'>
            {user['name'][0].upper()}
        </div>
        <div>
            <div style='color:#f0e6d3; font-weight:600; font-size:0.95rem;'>{user['name']}</div>
            <div style='color:#8b9bb4; font-size:0.75rem;'>{"👑 Admin" if is_admin else "📖 Reader"}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='color:#8b9bb4; font-size:0.75rem; text-transform:uppercase;"
        " letter-spacing:1px; margin-bottom:0.5rem;'>Navigation</div>",
        unsafe_allow_html=True
    )

    def nav_btn(label, page_key):
        if st.button(label, key=f"nav_{page_key}", use_container_width=True):
            st.session_state.page = page_key
            st.rerun()

    nav_btn("🏠  Home", "home")
    nav_btn("📚  Library", "library")
    nav_btn("👤  My Profile", "profile")
    nav_btn("📬  Request a Book", "request")

    if is_admin:
        st.markdown(
            "<br><div style='color:#8b9bb4; font-size:0.75rem; text-transform:uppercase;"
            " letter-spacing:1px; margin-bottom:0.5rem;'>Admin</div>",
            unsafe_allow_html=True
        )
        nav_btn("👑  Admin Dashboard", "admin")

    st.markdown("<br><hr style='border-color:#2a3448;'/>", unsafe_allow_html=True)
    st.markdown("""
    <style>
    div[data-testid="stSidebar"] div[data-testid="stButton"]:last-child > button {
        background: rgba(224,82,82,0.15) !important;
        color: #e87878 !important;
        border: 1px solid rgba(224,82,82,0.4) !important;
        font-weight: 700 !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stButton"]:last-child > button:hover {
        background: rgba(224,82,82,0.3) !important;
        color: #ff9999 !important;
        transform: none !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("🚪  Logout", use_container_width=True, key="logout_btn"):
        st.session_state.user = None
        st.session_state.page = "home"
        st.rerun()


# ── HOME PAGE ─────────────────────────────────────────────────────────────────
def show_home():
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-title">📚 PageVault</div>
        <div class="hero-subtitle">Welcome back, {user['name']}. Your next great read awaits.</div>
        <div style='margin-top:1.5rem; display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;'>
            <span style='background:rgba(201,168,76,0.15); border:1px solid rgba(201,168,76,0.3);
                         color:#c9a84c; padding:4px 14px; border-radius:20px; font-size:0.85rem;'>Dark Romance</span>
            <span style='background:rgba(224,82,82,0.12); border:1px solid rgba(224,82,82,0.3);
                         color:#e87878; padding:4px 14px; border-radius:20px; font-size:0.85rem;'>Horror</span>
            <span style='background:rgba(74,158,218,0.12); border:1px solid rgba(74,158,218,0.3);
                         color:#78b8e8; padding:4px 14px; border-radius:20px; font-size:0.85rem;'>Mystery</span>
            <span style='background:rgba(82,183,136,0.12); border:1px solid rgba(82,183,136,0.3);
                         color:#78d0a8; padding:4px 14px; border-radius:20px; font-size:0.85rem;'>Fantasy</span>
            <span style='background:rgba(74,196,183,0.12); border:1px solid rgba(74,196,183,0.3);
                         color:#78ddd0; padding:4px 14px; border-radius:20px; font-size:0.85rem;'>Sci-Fi</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Browse Library →", use_container_width=True, key="home_lib"):
            st.session_state.page = "library"
            st.rerun()
    with c2:
        if st.button("Request a Book →", use_container_width=True, key="home_req"):
            st.session_state.page = "request"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">⭐ Featured Books</div>', unsafe_allow_html=True)

    featured = get_featured_books(6)
    if not featured:
        st.markdown("""
        <div style='background:#1a2030; border:1px dashed #2a3448; border-radius:12px;
                    padding:3rem; text-align:center; color:#8b9bb4;'>
            <div style='font-size:3rem; margin-bottom:1rem;'>📭</div>
            <div style='font-family:Playfair Display,serif; font-size:1.2rem; color:#c9a84c;'>Library is empty</div>
            <div style='margin-top:0.5rem;'>The admin hasn't uploaded any books yet.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    batch_size = 3
    for batch_start in range(0, min(len(featured), 6), batch_size):
        batch = featured[batch_start:batch_start + batch_size]
        cols = st.columns(batch_size)
        for i, book in enumerate(batch):
            with cols[i]:
                avg, cnt = get_avg_rating(book["id"])
                cover_html = get_cover_html(book.get("cover_path"), height=200)
                stars = stars_html(avg, cnt)
                gbadge = genre_badge(book["genre"])
                st.markdown(f"""
                <div class="book-card">
                    {cover_html}
                    <div class="book-info">
                        <div class="book-title">{book['title']}</div>
                        <div class="book-author">{book['author']}</div>
                        {gbadge}<br/><br/>
                        {stars}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("View Book", key=f"feat_{batch_start}_{book['id']}", use_container_width=True):
                    st.session_state.current_book_id = book["id"]
                    st.session_state.page = "book_detail"
                    st.rerun()
        if batch_start + batch_size < min(len(featured), 6):
            st.markdown("<br>", unsafe_allow_html=True)


# ── ROUTER ────────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    show_home()
elif page == "library":
    show_library_page()
elif page == "book_detail":
    show_book_detail()
elif page == "reader":
    show_reader()
elif page == "profile":
    show_profile_page()
elif page == "request":
    show_request_page()
elif page == "admin" and is_admin:
    show_admin_dashboard()
else:
    st.session_state.page = "home"
    st.rerun()