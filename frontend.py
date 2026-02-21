import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="FastAPI Blog App", layout="centered")

# -----------------------------
# Session State
# -----------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None

if "name" not in st.session_state:
    st.session_state.name = None

# -----------------------------
# Helper Functions
# -----------------------------

def signup(name, username, password):
    url = f"{BASE_URL}/user/"
    data = {
        "name": name,
        "username": username,
        "Password": password
    }
    return requests.post(url, json=data)


def login(username, password):
    url = f"{BASE_URL}/login"
    data = {
        "username": username,
        "password": password
    }
    return requests.post(url, data=data)


def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def create_blog(title, body):
    url = f"{BASE_URL}/blog/"
    data = {
        "title": title,
        "body": body
    }
    return requests.post(url, json=data, headers=get_headers())


def get_blogs():
    url = f"{BASE_URL}/blog/"
    return requests.get(url, headers=get_headers())


def delete_blog(blog_id):
    url = f"{BASE_URL}/blog/{blog_id}"
    return requests.delete(url, headers=get_headers())


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Go to",
    ["Login", "Signup", "Dashboard"] if not st.session_state.token else ["Dashboard", "Logout"]
)


# -----------------------------
# Signup Page
# ----------------------------- 

if menu == "Signup":
    st.title("📝 Create Account")

    name = st.text_input("Name")
    username = st.text_input("Username")
    
    # Changed label to "Create Password"
    password = st.text_input("Create Password", type="password")
    
    # Added "Confirm Password" field
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        # Validation Logic
        if not name or not username or not password:
            st.error("Please fill in all fields.")
        elif password != confirm_password:
            st.error("Passwords don't match")
        else:
            response = signup(name, username, password)
            if response.status_code == 200 or response.status_code == 201:
                st.success("Account created successfully!")
            else:
                st.error(f"Error: {response.text}")


# -----------------------------
# Login Page
# -----------------------------

elif menu == "Login":
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        response = login(username, password)

        if response.status_code == 200:
            data = response.json()

            # Save token
            st.session_state.token = data.get("access_token")
            st.session_state.username = username

            # Get logged-in user details
            headers = {
                "Authorization": f"Bearer {st.session_state.token}"
            }

            user_response = requests.get(f"{BASE_URL}/user/me", headers=headers)

            if user_response.status_code == 200:
                user_data = user_response.json()

                # 🔥 VERY IMPORTANT
                # Use lowercase key
                st.session_state.name = user_data.get("name")

            else:
                st.error("Failed to fetch user details")

            st.success("Login successful!")
            st.rerun()

        else:
            st.error("Invalid Credentials")


# -----------------------------
# Dashboard
# -----------------------------

elif menu == "Dashboard":
    if not st.session_state.token:
        st.warning("Please login first.")
    else:
        # Retrieve the name from session state
        admin_name = st.session_state.get("name")

        # -----------------------------
        # IMPROVED GREETING LOGIC
        # ----------------------------- 
        if admin_name:
            # Displays: Welcome [Name] 👋
            st.title(f"Welcome {admin_name} 👋")
        else:
            # Fallback if name wasn't captured correctly
            st.title("Welcome 👋")

        tab1, tab2 = st.tabs(["➕ Create Blog", "📄 View Blogs"])

        # Create Blog
        with tab1:
            st.subheader("Create New Blog")
            title = st.text_input("Title")
            body = st.text_area("Body")

            if st.button("Create Blog"):
                response = create_blog(title, body)
                if response.status_code == 201 or response.status_code == 200:
                    st.success("Blog created successfully!")
                else:
                    st.error(response.text)

        # View Blogs
        with tab2:
            st.subheader("All Blogs")
            response = get_blogs()
            if response.status_code == 200:
                blogs = response.json()
                for blog in blogs:
                    st.markdown("---")
                    st.write(f"### {blog['title']}")
                    st.write(blog['body'])
                    
                    # Using a unique key for the delete button to avoid Streamlit errors
                    if st.button(f"Delete {blog['id']}", key=f"del_{blog['id']}"):
                        del_response = delete_blog(blog['id'])
                        if del_response.status_code == 204:
                            st.success("Deleted successfully!")
                            st.rerun()
                        else:
                            st.error(del_response.text)
            else:
                st.error("Failed to fetch blogs")


# -----------------------------
# Logout
# -----------------------------

elif menu == "Logout":
    for key in ["token", "name", "username"]:
        st.session_state[key] = None
    st.rerun()
