import streamlit as st
import base64
import os
from database import (get_book, get_book_ratings, get_avg_rating, get_user_rating,
                       upsert_rating, is_in_wishlist, toggle_wishlist, mark_as_read)
from library import get_cover_html, stars_html, genre_badge

def show_book_detail():
    book_id = st.session_state.get("current_book_id")
    if not book_id:
        st.session_state.page = "library"
        st.rerun()
        return

    book = get_book(book_id)
    if not book:
        st.markdown('<div class="alert-error">Book not found.</div>', unsafe_allow_html=True)
        return

    user = st.session_state.user
    avg, cnt = get_avg_rating(book_id)
    in_wl = is_in_wishlist(user["id"], book_id)

    if st.button("← Back to Library"):
        st.session_state.page = "library"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        cover_html = get_cover_html(book.get("cover_path"), height=360)
        st.markdown(f'<div style="border-radius:12px; overflow:hidden; box-shadow: 0 8px 32px rgba(0,0,0,0.6);">{cover_html}</div>', unsafe_allow_html=True)

    with col2:
        gbadge = genre_badge(book["genre"])
        stars = stars_html(avg, cnt)
        st.markdown(f"""
        <div class="book-detail-title">{book['title']}</div>
        <div class="book-detail-author">by {book['author']}</div>
        {gbadge}&nbsp;&nbsp;{stars}
        <br/>
        <div class="book-detail-desc">{book.get('description') or 'No description available.'}</div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if book.get("file_path") and os.path.exists(book["file_path"]):
                if st.button("📖 Read Now", use_container_width=True):
                    st.session_state.reading_book_id = book_id
                    st.session_state.page = "reader"
                    mark_as_read(user["id"], book_id)
                    st.rerun()
            else:
                st.button("📖 No File", disabled=True, use_container_width=True)
        with c2:
            wl_txt = "💛 Wishlisted" if in_wl else "🤍 Wishlist"
            if st.button(wl_txt, use_container_width=True):
                toggle_wishlist(user["id"], book_id)
                st.rerun()
        with c3:
            if book.get("file_path") and os.path.exists(book["file_path"]):
                with open(book["file_path"], "rb") as f:
                    file_bytes = f.read()
                st.download_button("⬇ Download", data=file_bytes,
                                   file_name=f"{book['title']}.pdf",
                                   mime="application/pdf",
                                   use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── RATING & REVIEW ──────────────────────────────────────────────────────
    st.markdown('<div class="section-header">⭐ Rate & Review</div>', unsafe_allow_html=True)

    user_rating = get_user_rating(user["id"], book_id)
    existing_stars = user_rating["stars"] if user_rating else 3
    existing_review = user_rating["review_text"] if user_rating else ""

    with st.form(f"rating_form_{book_id}"):
        star_val = st.slider("Your Rating", 1, 5, existing_stars, format="%d ⭐")
        review_txt = st.text_area("Your Review (optional)", value=existing_review, placeholder="What did you think of this book?", height=100)
        submitted = st.form_submit_button("Submit Rating →")
        if submitted:
            upsert_rating(user["id"], book_id, star_val, review_txt.strip())
            st.markdown('<div class="alert-success">✅ Rating saved!</div>', unsafe_allow_html=True)
            st.rerun()

    # ── REVIEWS ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">💬 All Reviews</div>', unsafe_allow_html=True)

    ratings = get_book_ratings(book_id)
    if not ratings:
        st.markdown('<div class="alert-info">📝 No reviews yet. Be the first!</div>', unsafe_allow_html=True)
    else:
        for r in ratings:
            stars_str = "★" * r["stars"] + "☆" * (5 - r["stars"])
            date_str = r["created_at"][:10] if r["created_at"] else ""
            review_content = r.get("review_text") or "<em>No written review.</em>"
            st.markdown(f"""
            <div class="review-card">
                <div class="review-header">
                    <span class="reviewer-name">{r['user_name']}</span>
                    <span style="color:#c9a84c;">{stars_str}</span>
                    <span class="review-date">{date_str}</span>
                </div>
                <p class="review-text">{review_content}</p>
            </div>
            """, unsafe_allow_html=True)


def show_reader():
    book_id = st.session_state.get("reading_book_id")
    if not book_id:
        st.session_state.page = "library"
        st.rerun()
        return

    book = get_book(book_id)
    if not book:
        st.markdown('<div class="alert-error">Book not found.</div>', unsafe_allow_html=True)
        return

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back"):
            st.session_state.page = "book_detail"
            st.session_state.current_book_id = book_id
            st.rerun()
    with col2:
        st.markdown(f"<div style='font-family:Playfair Display,serif; color:#c9a84c; font-size:1.3rem; font-weight:700;'>📖 {book['title']}</div>", unsafe_allow_html=True)

    file_path = book.get("file_path", "")

    if not file_path or not os.path.exists(file_path):
        st.markdown('<div class="alert-error">❌ Book file not found on server.</div>', unsafe_allow_html=True)
        return

    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        pdf_html = f"""
        <iframe
            src="data:application/pdf;base64,{b64}#toolbar=1&navpanes=1&scrollbar=1"
            width="100%"
            height="850px"
            style="border:none; border-radius:8px; background:#fff;"
            type="application/pdf">
        </iframe>
        """
        st.markdown(pdf_html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="alert-info">⚠️ Only PDF files can be read in-browser. You can download EPUB files.</div>', unsafe_allow_html=True)
        with open(file_path, "rb") as f:
            st.download_button("⬇ Download EPUB", data=f.read(),
                               file_name=f"{book['title']}.epub",
                               mime="application/epub+zip")