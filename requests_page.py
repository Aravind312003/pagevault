import streamlit as st
from database import submit_request, get_user_requests

def show_request_page():
    user = st.session_state.user

    st.markdown('<div class="section-header">📬 Request a Book</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#8b9bb4; font-size:1rem; margin-bottom:2rem; line-height:1.7;'>
        Can't find a book you're looking for? Submit a request and the admin will consider adding it to the library.
    </div>
    """, unsafe_allow_html=True)

    with st.form("book_request_form"):
        book_title = st.text_input("Book Title *", placeholder="e.g. A Court of Thorns and Roses")
        author = st.text_input("Author", placeholder="e.g. Sarah J. Maas")
        reason = st.text_area("Why do you want this book?", placeholder="Tell us why you'd love to have this book in the library...", height=120)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Submit Request →", use_container_width=True)

        if submitted:
            if not book_title.strip():
                st.markdown('<div class="alert-error">⚠️ Book title is required.</div>', unsafe_allow_html=True)
            else:
                submit_request(user["id"], book_title.strip(), author.strip(), reason.strip())
                st.markdown('<div class="alert-success">✅ Request submitted! The admin will review it soon.</div>', unsafe_allow_html=True)
                st.rerun()

    # Show past requests
    past = get_user_requests(user["id"])
    if past:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">📋 Your Past Requests</div>', unsafe_allow_html=True)
        for req in past:
            status_cls = "status-fulfilled" if req["status"] == "fulfilled" else "status-pending"
            st.markdown(f"""
            <div class="review-card">
                <div class="review-header">
                    <span class="reviewer-name">📚 {req['book_title']}</span>
                    <span class="{status_cls}">{req['status'].upper()}</span>
                </div>
                <div style="color:#8b9bb4; font-size:0.85rem; margin-bottom:4px;">
                    {f'by {req["author"]}  ·  ' if req.get('author') else ''}{str(req.get('created_at',''))[:10]}
                </div>
                {f'<p class="review-text">{req["reason"]}</p>' if req.get('reason') else ''}
            </div>
            """, unsafe_allow_html=True)