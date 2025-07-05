import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import os
import uuid
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="Admin Portal")


IMAGE_FOLDER = "images"

# Create a SQLite database and a table for user information
conn = sqlite3.connect('users1.db')
cursor = conn.cursor()

conn.commit()


def login(username, password):
    if username=='admin' and password=='admin123':
        return True
    return False

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Pot-Sol Website',
                           ['Login',
                            'Edit Complaint Status',
                            'View Users',
                            'Logout'],
                           icons=['person', 'view-list', 'people', 'box-arrow-right'],
                           default_index=0)

if selected == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("Logged in as " + username)
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password")
            st.session_state.logged_in = False


if selected == "Edit Complaint Status":
    st.title("Edit Complaint Status")

    if st.session_state.get("logged_in", False):
        def send_status_update_email(raising_person_email, username, complaint_title, new_status):
            # Create the email content
            email_content = f"""
            <div style="background-color:#111827; padding: 20px; border-radius: 15px; width: 100%; max-width: 400px; margin: auto; color: #ffffff; font-family: Arial, sans-serif; text-align: center;">
                <h3 style="color: #ffffff;">Hi {username},</h3>
                <p style="color: #ffffff;">This is to inform you that the status of your complaint <strong>{complaint_title}</strong> has been updated to:</p>
                <div style="background-color: #2d3748; padding: 15px; border-radius: 8px; font-size: 24px; letter-spacing: 2px; margin-bottom: 20px; color: #ffffff;">
                    {new_status}
                </div>
                <p style="font-size: 14px; color: #ffffff;">
                    We will notify you once there is a further update. Thank you for your patience!
                </p>
                <div style="margin-top: 40px;">
                    <p style="font-size: 12px; color: #ffffff;">© Pot-Sol Management, All Rights Reserved</p>
                </div>
            </div>
            """

            # Set up the email details
            email_msg = EmailMessage()
            email_msg.set_content(email_content, subtype='html')
            email_msg['Subject'] = "Complaint Status Update"
            email_msg['From'] = "no.reply.pot.sol@gmail.com"
            email_msg['To'] = raising_person_email

            # Send the email using SMTP
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("no.reply.pot.sol@gmail.com", "rfkh opci nhgs hyop")  # Replace with your credentials
                    smtp.send_message(email_msg)
                return True
            except Exception as e:
                st.error(f"Failed to send status update email. Error: {e}")
                return False

        cursor.execute('''SELECT complaint_type, complaint_title, complaint_description, 
                          complaint_area, complaint_co, priority, status, id, image_name, raising_person_name, 
                          raising_person_mobile, raising_person_email FROM Complaints''')
        complaints = cursor.fetchall()

        for complaint in complaints:
            st.image(os.path.join(IMAGE_FOLDER, complaint[8]), caption=f"Image ID: {complaint[7]}", use_column_width=True)
            st.write(f"**Title:** {complaint[1]}")
            st.write(f"**Description:** {complaint[2]}")
            
            if complaint[4] and complaint[3]:  # Display both coordinates and address if available
                st.write(f"**Coordinates:** {complaint[4]}")
                st.write(f"**Address:** {complaint[3]}")
                
            elif complaint[4]:  # Display only coordinates if available
                st.write(f"**Coordinates:** {complaint[4]}")
                
            elif complaint[3]:  # Display only address if coordinates not available
                st.write(f"**Address:** {complaint[3]}")
                

            st.write(f"**Type:** {complaint[0]} | **Priority:** {complaint[5]} | **Status:** {complaint[6]}")
            st.write(f"**Citizen Name:** {complaint[9]} | **Mobile No:** {complaint[10]}")
            
            # Button to edit status
            new_status = st.selectbox(f"Edit Status for Complaint {complaint[7]}",
                                      ["Submitted","In-Queue", "In-Review", "Physical Verification", "Completed", "Rejected"], key=f"edit_status_{complaint[7]}")
            
            if st.button(f"Update Status for Complaint {complaint[7]}", key=f"update_status_{complaint[7]}"):
                # Update status in the database
                cursor.execute("UPDATE Complaints SET status=? WHERE id=?", (new_status, complaint[7]))
                conn.commit()
                st.success(f"Status for Complaint {complaint[7]} updated successfully.")
                send_status_update_email(complaint[11], complaint[9], complaint[1], new_status) # Send email
                st.success(f"Email sent successfully to {complaint[11]}")


            st.write("---")



    else:
        st.warning("Please log in to access this page.")
        print("I'm warning")
        
        
if selected == "View Users":
    st.title("Registered Users")
    st.write("---")

    if st.session_state.get("logged_in", False):
        cursor.execute('''SELECT username, registration_mail FROM users''')  # Modify based on your actual table structure
        users = cursor.fetchall()

        for idx, user in enumerate(users, start=1):
            st.write(f"**{idx}. Username:** {user[0]}")
            st.write(f"**Registation Email:** {user[1]}")
            st.write("---")

    else:
        st.warning("Please log in to view the users.")


if selected == "Logout":
    confirmation = st.warning("Are you sure you want to log out?")
    if confirmation.button("Do you want to log-out"):
        st.session_state.logged_in = False
        st.success("You have been logged out.")

# Close the database connection when the Streamlit app is done
conn.close()


