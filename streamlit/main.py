import streamlit as st
def main():
    # Initialize session state
    session_state = st.session_state
    if "login_screen" not in session_state:
        session_state.login_screen = True

    if "auth_user_token" not in session_state:
        session_state.auth_user_token = None
    
    if session_state.auth_user_token is None:    
        if session_state.login_screen:
            # Login Section
            st.subheader("Login")
            username = st.text_input("Username:", key="login_username")
            password = st.text_input("Password:", type="password", key="login_password")
            if st.button("Login"):
                if username.strip() == "" or password.strip() == "":
                    st.warning("Please enter a username and password.")
                else:
                    st.success(f"Welcome back, {username}!")
                    session_state.auth_user_token = "Hello world"
                    session_state.username = username
                    st.rerun()
        else:
            # Sign Up Section
            st.subheader("Sign Up")
            new_username = st.text_input("Username:", key="signup_username")
            new_email = st.text_input("Email:", key="signup_email")
            new_password = st.text_input("Password:", type="password", key="signup_password")
            if st.button("Sign Up"):
                if new_username.strip() == "" or new_email.strip() == "" or new_password.strip() == "":
                    st.warning("Please enter a username, email, and password.")
                else:
                    st.success("Account created successfully. Please log in.")
                    session_state.login_screen = not session_state.login_screen
                    st.rerun()

        if st.button("Already a user? Signup now" if session_state.login_screen else "Already a user? Login now"):
            session_state.login_screen = not session_state.login_screen
            st.rerun()
            
    else: 
        head_col_1,head_col_2 = st.columns([1,0.14])
        with head_col_1:
            st.title("Todo List")
        with head_col_2:
            if st.button("Logout"):
                session_state.login_page=True
                session_state.auth_user_token = None
                st.rerun()
        if "tasks" not in session_state:
            session_state.tasks = [
                {"id": 1, "title": "Task 1", "description": "Description for Task 1"},
                {"id": 2, "title": "Task 2", "description": "Description for Task 2"},
                {"id": 3, "title": "Task 3", "description": "Description for Task 3"},
            ]
        # Display existing tasks
        st.subheader("Existing Tasks")
        
        session_tasks = session_state.tasks
        if session_tasks:
            for task in session_tasks:
                col1, col2, col3 = st.columns([1, 0.12, 0.15])
                with col1: 
                    
                    st.write(f"**{task['title']}**: {task['description']} (ID: {task['id']})")
                with col2:
                    if st.button("Edit",key=f"edit_task_{task['id']}"):
                        # edit_task(task)
                        print("edit")
                with col3:
                    if st.button("Delete",key=f"delete_task_{task['id']}"):
                        # delete_task(task['id'])
                        print("delete")
        else:
            st.write("No tasks available.")

        # Add new task
        st.subheader("Add New Task")
        new_title = st.text_input("Title:")
        new_description = st.text_area("Description:")
        if st.button("Add Task"):
            if new_title.strip() == "" or new_description.strip() == "":
                st.warning("Please enter a title and description for the task.")
            else:
                new_id = len(session_tasks) + 1
                new_task = {"id": new_id, "title": new_title, "description": new_description}
                session_tasks.append(new_task)
                st.success("Task added successfully.")   
                st.rerun()        


if __name__ == "__main__":
    # Sample data - list of dictionaries containing tasks
    
    main()