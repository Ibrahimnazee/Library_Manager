import streamlit as st
import json
import os

# File to store book data
data_file = 'library.json'

# Load library data
def load_library():
    if os.path.exists(data_file) and os.path.getsize(data_file) > 0:
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

# Save library data
def save_library():
    with open(data_file, 'w') as file:
        json.dump(st.session_state.library, file, indent=4)

# Initialize session state
if "library" not in st.session_state:
    st.session_state.library = load_library()

    # 🎨 Custom Styling
st.markdown("""
    <style>
        .stApp { background-color: #9fd1b9; color: #141414}
        .title { text-align: center; color: #58A6FF; font-size: 2.5em; font-weight: bold; }
        .subtitle { text-align: center; font-size: 1.2em; color: #f51827; }
        .footer { text-align: center; font-size: 1em; color: #141414; margin-top: 30px; }
        .stProgress > div > div > div { background-color:#f51827 !important; }
    </style>
""", unsafe_allow_html=True)

# 🎉 App Title
st.markdown("<h1 style='text-align: center; color: #58A6FF;'>📚 Library Manager</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Easily manage your personal book collection!</p>", unsafe_allow_html=True)

# 🆕 **Add New Book**
st.subheader("➕ Add a New Book")

with st.form("add_book_form"):
    title = st.text_input("📖 Book Title").strip()
    author = st.text_input("✍️ Author").strip()
    year = st.number_input("📅 Year of Publication", min_value=1500, max_value=2025, step=1)
    genre = st.selectbox("📂 Genre", ["Fiction", "Non-Fiction", "Mystery", "Fantasy", "Biography", "Science", "Other"])
    read = st.checkbox("✅ Mark as Read")

    submitted = st.form_submit_button("📌 Add Book")

    if submitted:
        if title and author and year:
            new_book = {"title": title, "author": author, "year": int(year), "genre": genre, "read": read}
            st.session_state.library.append(new_book)
            save_library()
            st.success(f'✅ Book "{title}" added successfully!')
            st.rerun()  # 🔄 Refresh UI to show new book
        else:
            st.error("❌ Please fill in all fields before adding a book.")

# 📋 **Display All Books**
st.subheader("📋 Your Book Collection")
if st.session_state.library:
    for book in st.session_state.library:
        status = "✅ Read" if book["read"] else "❌ Unread"
        st.markdown(f"**📖 {book['title']}** by *{book['author']}* ({book['year']}) - *{book['genre']}* - {status}")
else:
    st.info("📭 No books in your collection yet.")

# 🔍 **Search Books**
st.subheader("🔎 Search Books")
search_term = st.text_input("Search by title or author")

if search_term:
    results = [book for book in st.session_state.library if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]
    if results:
        for book in results:
            st.markdown(f"**📖 {book['title']}** by *{book['author']}* ({book['year']}) - *{book['genre']}*")
    else:
        st.warning("No matching books found.")

# 🗑️ **Remove Book**
st.subheader("🗑️ Remove a Book")
remove_title = st.text_input("Enter the title to remove")

if st.button("❌ Remove Book"):
    initial_length = len(st.session_state.library)
    st.session_state.library = [book for book in st.session_state.library if book["title"].lower() != remove_title.lower()]
    if len(st.session_state.library) < initial_length:
        save_library()
        st.success(f'✅ Book "{remove_title}" removed successfully!')
        st.rerun()  # 🔄 Refresh UI
    else:
        st.error(f'❌ Book "{remove_title}" not found.')

# 📊 **Library Statistics**
st.subheader("📊 Library Statistics")
total_books = len(st.session_state.library)
read_books = len([book for book in st.session_state.library if book["read"]])
percentage_read = (read_books / total_books * 100) if total_books > 0 else 0

st.markdown(f"📚 **Total Books:** {total_books}")
st.markdown(f"📖 **Books Read:** {read_books} ({percentage_read:.2f}%)")
st.progress(percentage_read / 100)

# 📌 **Footer**
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🚀 Made by <strong>Ibrahim Nazeer 🚀</strong></p>", unsafe_allow_html=True)
