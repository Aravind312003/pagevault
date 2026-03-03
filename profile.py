import streamlit as st
from database import (get_reading_history, get_user_wishlist, get_user_requests,
                       get_books_read_count, toggle_wishlist)
from library import get_cover_html, genre_badge, stars_html
from database import get_avg_rating

def show_profile_page():
    user = st.session_state.user

    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #161b22, #1a2030); border:1px solid #2a3448;
                border-radius:16px; padding:2rem; margin-bottom:2rem; display:flex; align-items:center; gap:1.5rem;'>
        <div style='width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg,#c9a84c,#a08030);
                    display:flex; align-items:center; justify-content:center; font-size:1.8rem; font-weight:700;
                    color:#0d1117; flex-shrink:0;'>
            {user['name'][0].upper()}
        </div>
        <div>
            <div style='font-family:Playfair Display,serif; font-size:1.6rem; font-weight:700; color:#c9a84c;'>{user['name']}</div>
            <div style='color:#8b9bb4; font-size:0.9rem;'>{user['email']}</div>
            <div style='color:#8b9bb4; font-size:0.85rem; margin-top:4px;'>Member since {str(user.get('joined_at','')[:10])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    books_read = get_books_read_count(user["id"])
    wishlist = get_user_wishlist(user["id"])
    requests = get_user_requests(user["id"])

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{books_read}</div><div class="stat-label">Books Read</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{len(wishlist)}</div><div class="stat-label">Wishlist</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{len(requests)}</div><div class="stat-label">Requests</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["  📖 Reading History  ", "  💛 Wishlist  ", "  📬 My Requests  "])

    with tab1:
        history = get_reading_history(user["id"])
        if not history:
            st.markdown('<div class="alert-info">📭 You haven\'t read any books yet. Head to the library!</div>', unsafe_allow_html=True)
        else:
            cols_per_row = 4
            for i in range(0, len(history), cols_per_row):
                row_books = history[i:i+cols_per_row]
                cols = st.columns(cols_per_row)
                for j, book in enumerate(row_books):
                    with cols[j]:
                        avg, cnt = get_avg_rating(book["id"])
                        cover_html = get_cover_html(book.get("cover_path"), height=180)
                        st.markdown(f"""
                        <div class="book-card">
                            {cover_html}
                            <div class="book-info">
                                <div class="book-title">{book['title']}</div>
                                <div class="book-author">{book['author']}</div>
                                {genre_badge(book['genre'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("View", key=f"hist_view_{book['id']}", use_container_width=True):
                            st.session_state.current_book_id = book["id"]
                            st.session_state.page = "book_detail"
                            st.rerun()

    with tab2:
        if not wishlist:
            st.markdown('<div class="alert-info">💭 Your wishlist is empty. Browse the library and add books!</div>', unsafe_allow_html=True)
        else:
            cols_per_row = 4
            for i in range(0, len(wishlist), cols_per_row):
                row_books = wishlist[i:i+cols_per_row]
                cols = st.columns(cols_per_row)
                for j, book in enumerate(row_books):
                    with cols[j]:
                        cover_html = get_cover_html(book.get("cover_path"), height=180)
                        st.markdown(f"""
                        <div class="book-card">
                            {cover_html}
                            <div class="book-info">
                                <div class="book-title">{book['title']}</div>
                                <div class="book-author">{book['author']}</div>
                                {genre_badge(book['genre'])}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("View", key=f"wl_view_{book['id']}", use_container_width=True):
                                st.session_state.current_book_id = book["id"]
                                st.session_state.page = "book_detail"
                                st.rerun()
                        with c2:
                            if st.button("Remove", key=f"wl_rm_{book['id']}", use_container_width=True):
                                toggle_wishlist(user["id"], book["id"])
                                st.rerun()

    with tab3:
        if not requests:
            st.markdown('<div class="alert-info">📭 No requests submitted yet.</div>', unsafe_allow_html=True)
        else:
            for req in requests:
                status_cls = "status-fulfilled" if req["status"] == "fulfilled" else "status-pending"
                st.markdown(f"""
                <div class="review-card">
                    <div class="review-header">
                        <span class="reviewer-name">📚 {req['book_title']}</span>
                        <span class="{status_cls}">{req['status'].upper()}</span>
                    </div>
                    <div style="color:#8b9bb4; font-size:0.85rem;">by {req.get('author') or 'Unknown'} · {str(req.get('created_at',''))[:10]}</div>
                    {f'<p class="review-text">{req["reason"]}</p>' if req.get("reason") else ''}
                </div>
                """, unsafe_allow_html=True)