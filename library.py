import streamlit as st
import base64
import os
from database import get_all_books, get_avg_rating, is_in_wishlist, toggle_wishlist

GENRES = ["All", "Dark Romance", "Romance", "Horror", "Thriller", "Mystery", "Fantasy", "Sci-Fi", "Other"]

GENRE_CLASS = {
    "Dark Romance": "genre-dark-romance",
    "Romance": "genre-romance",
    "Horror": "genre-horror",
    "Thriller": "genre-thriller",
    "Mystery": "genre-mystery",
    "Fantasy": "genre-fantasy",
    "Sci-Fi": "genre-sci-fi",
    "Other": "genre-other",
}

def get_cover_html(cover_path, height=220):
    if cover_path and os.path.exists(cover_path):
        with open(cover_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = cover_path.split(".")[-1].lower()
        mime = "image/jpeg" if ext in ["jpg","jpeg"] else f"image/{ext}"
        return f'<img src="data:{mime};base64,{b64}" class="book-cover" style="height:{height}px;" />'
    return f'<div class="book-cover-placeholder" style="height:{height}px;">📖</div>'

def stars_html(avg, cnt):
    filled = round(avg)
    stars = "★" * filled + "☆" * (5 - filled)
    return f'<div class="star-display">{stars} <span style="color:#8b9bb4; font-size:0.8rem;">({cnt})</span></div>'

def genre_badge(genre):
    cls = GENRE_CLASS.get(genre, "genre-other")
    return f'<span class="genre-badge {cls}">{genre}</span>'

def show_library_page():
    user = st.session_state.user

    st.markdown('<div class="section-header">📚 Library</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 3])
    with col1:
        search = st.text_input("", placeholder="🔍 Search by title or author...", key="lib_search", label_visibility="collapsed")
    with col2:
        genre_filter = st.selectbox("", GENRES, key="lib_genre", label_visibility="collapsed")

    books = get_all_books(
        genre=genre_filter if genre_filter != "All" else None,
        search=search.strip() if search else None
    )

    if not books:
        st.markdown('<div class="alert-info">📭 No books found. Try a different search or filter.</div>', unsafe_allow_html=True)
        return

    st.markdown(f"<div style='color:#8b9bb4; font-size:0.9rem; margin-bottom:1rem;'>{len(books)} book{'s' if len(books)!=1 else ''} found</div>", unsafe_allow_html=True)

    cols_per_row = 4
    for i in range(0, len(books), cols_per_row):
        row_books = books[i:i+cols_per_row]
        cols = st.columns(cols_per_row)
        for j, book in enumerate(row_books):
            with cols[j]:
                avg, cnt = get_avg_rating(book["id"])
                cover_html = get_cover_html(book.get("cover_path"), height=200)
                gbadge = genre_badge(book["genre"])
                stars = stars_html(avg, cnt)

                st.markdown(f"""
                <div class="book-card">
                    {cover_html}
                    <div class="book-info">
                        <div class="book-title">{book['title']}</div>
                        <div class="book-author">{book['author']}</div>
                        {gbadge}
                        <br/><br/>
                        {stars}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("View", key=f"view_{book['id']}", use_container_width=True):
                        st.session_state.current_book_id = book["id"]
                        st.session_state.page = "book_detail"
                        st.rerun()
                with c2:
                    in_wl = is_in_wishlist(user["id"], book["id"])
                    wl_label = "💛" if in_wl else "🤍"
                    if st.button(wl_label, key=f"wl_{book['id']}", use_container_width=True):
                        toggle_wishlist(user["id"], book["id"])
                        st.rerun()