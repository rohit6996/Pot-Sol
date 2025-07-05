import re
import streamlit as st
from streamlit_option_menu import option_menu
import sqlite3
import os
import uuid
from PIL import Image
import requests
import pyperclip
import random
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="User Portal")


# Create a folder to store images if it doesn't exist
IMAGE_FOLDER = "images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

# Create a SQLite database and a table for user information
conn = sqlite3.connect('users1.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        registration_mail TEXT
    )
''')

# Create Complaints table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS Complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT,
    complaint_type TEXT,
    complaint_title TEXT,
    complaint_description TEXT,
    complaint_area TEXT,
    priority TEXT,
    raising_person_name TEXT,
    raising_person_mobile TEXT,
    raising_person_email TEXT,
    status TEXT,
    complaint_co TEXT
    
)
''')

conn.commit()

def is_user_exists(username, password):
    conn = sqlite3.connect('users1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    return cursor.fetchone() is not None

def is_username_exists(username):
    conn = sqlite3.connect('users1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cursor.fetchone() is not None

def create_user(username, password, registration_mail):
    conn = sqlite3.connect('users1.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, registration_mail) VALUES (?, ?, ?)', (username, password, registration_mail))
    conn.commit()

def login(username, password):
    conn = sqlite3.connect('users1.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        return True
    return False

# html_code = """
# <!DOCTYPE html>
# <html lang="en">

# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Manually Select Location</title>
#     <style>
#         body {
#             margin: 0;
#             padding: 0;
#         }

#         #map-container {
#             width: 100%;
#             height: 75vh;
#             /* Reduced the height of the map */
#             margin: 0 auto;
#             border: 1px solid #ccc;
#             border-radius: 5px;
#             box-sizing: border-box;
#             overflow: hidden;
#         }

#         #coordinates-display {
#             color: white;
#             /* Change this to any color you want */
#         }

#         #address-display {
#             color: white;
#             /* Change this to any color you want */
#         }


#         #map {
#             height: calc(100% - 2px);
#             width: calc(100% - 2px);
#             margin: 1px;
#         }

#         #selected-coordinates {
#             text-align: center;
#             margin-top: 10px;
#             font-weight: bold;
#         }

#         #copy-button {
#             margin-top: 10px;
#             cursor: pointer;
#             background-color: #4caf50;
#             color: white;
#             border: none;
#             border-radius: 5px;
#             padding: 8px 16px;
#             text-align: center;
#             text-decoration: none;
#             display: inline-block;
#             font-size: 15px;
#         }

#         /* Position the button over the map */
#         #get-location-btn {
#             position: absolute;
#             top: 10px;
#             left: 10px;
#             z-index: 5;
#             background-color: #007bff;
#             color: white;
#             padding: 10px 20px;
#             border: none;
#             border-radius: 5px;
#             cursor: pointer;
#             font-size: 14px;
#         }

#         #get-location-btn:hover {
#             background-color: #0056b3;
#         }
#     </style>
# </head>

# <body>

#     <!-- Get My Location Button -->
#     <button id="get-location-btn" onclick="getMyLocation()">Get My Location</button>

#     <div id="map-container">
#         <div id="map"></div>
#     </div>

#     <div id="selected-coordinates">
#         <span id="coordinates-display"></span><br>
#         <span id="address-display"></span><br>
#         <button id="copy-button" onclick="copyToClipboard()">Copy to Clipboard</button>
#     </div>

#     <script>
#         let map, marker;

#         function initMap() {
#             // Initialize the map with a default location
#             map = new google.maps.Map(document.getElementById('map'), {
#                 center: { lat: 21.126089, lng: 79.003391 },
#                 zoom: 12
#             });

#             // Initialize marker
#             marker = new google.maps.Marker({
#                 position: map.getCenter(),
#                 map: map,
#                 draggable: true,
#                 title: 'Drag me!'
#             });

#             // Add a click event listener to the map
#             google.maps.event.addListener(map, 'click', function (event) {
#                 marker.setPosition(event.latLng);
#                 const selectedLocation = {
#                     lat: event.latLng.lat(),
#                     lng: event.latLng.lng()
#                 };

#                 // Display the coordinates on the page
#                 document.getElementById('coordinates-display').innerHTML =
#                     'Selected Coordinates: ' + selectedLocation.lat + ', ' + selectedLocation.lng;

#                 // Call the Geocoding API to get the address
#                 getAddress(selectedLocation.lat, selectedLocation.lng);
#             });
#         }

#         // Function to get user's current location
#         function getMyLocation() {
#             if (navigator.geolocation) {
#                 navigator.geolocation.getCurrentPosition(
#                     function (position) {
#                         const userLocation = {
#                             lat: position.coords.latitude,
#                             lng: position.coords.longitude
#                         };

#                         // Center the map on user's location
#                         map.setCenter(userLocation);
#                         map.setZoom(15);
#                         marker.setPosition(userLocation);

#                         // Display the user's coordinates and get the address
#                         document.getElementById('coordinates-display').innerHTML =
#                             'Selected Coordinates: ' + userLocation.lat + ', ' + userLocation.lng;
#                         getAddress(userLocation.lat, userLocation.lng);
#                     },
#                     function () {
#                         alert('Geolocation permission denied. Unable to get location.');
#                     }
#                 );
#             } else {
#                 alert('Geolocation is not supported by this browser.');
#             }
#         }

#         // Function to copy coordinates to clipboard
#         function copyToClipboard() {
#             const selectedLocation = {
#                 lat: marker.getPosition().lat(),
#                 lng: marker.getPosition().lng()
#             };
#             const coordinatesText = selectedLocation.lat + ', ' + selectedLocation.lng;
#             navigator.clipboard.writeText(coordinatesText)
#                 .then(function () {
#                     alert('Coordinates copied to clipboard: ' + coordinatesText);
#                 })
#                 .catch(function (err) {
#                     console.error('Unable to copy to clipboard', err);
#                 });
#         }

#         // Function to get address from coordinates using Google Geocoding API
#         function getAddress(lat, lng) {
#             const geocoder = new google.maps.Geocoder();
#             const latLng = { lat: parseFloat(lat), lng: parseFloat(lng) };

#             geocoder.geocode({ location: latLng }, function (results, status) {
#                 if (status === 'OK') {
#                     if (results[0]) {
#                         const address = results[0].formatted_address;
#                         document.getElementById('address-display').innerHTML = 'Address: ' + address;
#                     } else {
#                         document.getElementById('address-display').innerHTML = 'No address found';
#                     }
#                 } else {
#                     console.error('Geocoder failed due to: ' + status);
#                 }
#             });
#         }
#     </script>

#     <!-- Google Maps with API key -->
#     <script async defer
#         src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY_HERE_&callback=initMap">
#         </script>

# </body>

# </html>

# """


# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Pot-Sol Website',
                           ['Register',
                            'Login',
                            'Raise Complaint',
                            'View Complaint Status',
                            'Logout'],
                           icons=['file-earmark-person', 'person', 'hand-index', 'view-list', 'box-arrow-right'],
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





# Updated registration section with OTP verification
if selected == "Register":
    st.header("Register")
    
    # Username validation function
    def validate_username(username):
        # Regex pattern: At least 4 letters and 3 numbers
        if re.fullmatch(r'^(?=.*[A-Za-z]{4,})(?=.*\d{3,})[A-Za-z\d]{7,}$', username):
            return True
        else:
            return False

    # Password validation function
    def validate_password(password):
        # Regex pattern for standard password: At least 1 uppercase, 1 lowercase, 1 digit, 1 special character, and 8 characters long
        if re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            return True
        else:
            return False
        
    # Function to generate a 6-digit OTP
    def generate_otp():
        return random.randint(100000, 999999)

    # Function to send the OTP via email
    def send_otp_email(receiver_email, otp):
        # Create the email content
        email_content = f"""
        <div style="background-color:#111827; padding: 20px; border-radius: 15px; width: 100%; max-width: 400px; margin: auto; color: #ffffff; font-family: Arial, sans-serif; text-align: center;">
        <h3 style="color: #ffffff;">Hi Citizen,</h3>
        <p style="color: #ffffff;">Here is your unique login code to access your Pot-Sol account:</p>
        <div style="background-color: #2d3748; padding: 15px; border-radius: 8px; font-size: 24px; letter-spacing: 2px; margin-bottom: 20px; color: #ffffff;">
            {otp}
        </div>
        <p style="font-size: 14px; color: #ffffff;">
            We have implemented these measures as an extra layer of security, which is extremely important to us.
        </p>
        <div style="margin-top: 40px;">
            <p style="font-size: 12px; color: #ffffff;">© Pot-Sol Management, All Rights Reserved</p>
        </div>
    </div>
            """

        # Set up the email details
        email_msg = EmailMessage()
        email_msg.set_content(email_content, subtype='html')
        email_msg['Subject'] = "Your Pot-Sol OTP Verification Code"
        email_msg['From'] = "no.reply.pot.sol@gmail.com"
        email_msg['To'] = receiver_email

        # Set up the SMTP server (use your email credentials)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("no.reply.pot.sol@gmail.com", "rfkh opci nhgs hyop")  # Replace with your credentials
                smtp.send_message(email_msg)
            return True
        except Exception as e:
            st.error(f"Failed to send OTP email. Error: {e}")
            return False

    # Function to verify the OTP entered by the user
    def verify_otp(generated_otp, user_input_otp):
        return generated_otp == user_input_otp
        

    # Reset session state variables at the start of each registration
    # if 'otp_generated' not in st.session_state or st.button("Reset Registration"):
    if 'otp_generated' not in st.session_state:

        st.session_state.otp_generated = False
        st.session_state.generated_otp = None
        st.session_state.otp_verified = False

    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    def is_username_exists(username):
        conn = sqlite3.connect('users1.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone() is not None
    
    if st.button("Validate Username and Password"):
        # Step 1: Check if the username format is valid
        if validate_username(new_username):
            # Step 2: Check if the username is already registered
            if is_username_exists(new_username):
                st.error("Username already exists. Please choose a different username.")
            else:
                st.success("Username is valid and available.")
        else:
            st.error("Invalid Username. It must contain at least 4 letters and 3 numbers.")

        if validate_password(new_password):
            st.success("Password is valid.")
        else:
            st.error("Invalid Password. It must be at least 8 characters long, contain at least 1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character.")
    
    registraion_email = st.text_input("Email for OTP verification")
    

    # Check if passwords match
    if new_password == confirm_password:
        
        # OTP generation and sending process
        if st.button("Generate OTP"):
            if registraion_email and not is_username_exists(new_username):  # Check if email is provided and username is unique
                otp = generate_otp()
                st.session_state.generated_otp = otp
                st.session_state.otp_generated = True
                if send_otp_email(registraion_email, otp):
                    st.success("If the email is valid, OTP has been sent successfully! Please check your email.")
            else:
                st.error('Username already exists or email is missing. Please choose a different username and provide an email.')
    
        # OTP input and verification only if OTP was generated
        if st.session_state.otp_generated:
            user_input_otp = st.text_input("Enter OTP", type="password", key="otp_input")
            
            # Verify OTP button
            if st.button("Verify OTP"):
                if verify_otp(st.session_state.generated_otp, int(user_input_otp)):
                    st.success("OTP verified successfully!")
                    st.session_state.otp_verified = True
                else:
                    st.error("Invalid OTP. Please try again.")
                    
                    
        def send_welcome_email(receiver_email, username):
            # Create the email content
            email_content = f"""
            <div
            style="background-color:#1b2733; padding: 20px; border-radius: 15px; width: 100%; max-width: 400px; margin: auto; color: #ffffff; font-family: Arial, sans-serif; text-align: center; line-height: 1.6;">
            <h3 style="color: #20f903; font-weight: bold;">Welcome, {username}!</h3>
            <p style="color: #fefefe; line-height: 1.8;">We are thrilled to have you on board with Pot-Sol!</p>
            <p style="color: #ffffff; line-height: 1.8;">Your account has been successfully created and you can now explore all
                the features we
                offer to make managing potholes and streetlight issues easier in your area.</p>
            <p style="font-size: 14px; color: #ffffff; line-height: 1.8;">
                If you have any questions or need assistance, feel free to reach out to our support team. We are always here to
                help!
            </p>
            <div style="margin-top: 40px;">
                <p style="font-size: 12px; color: #ffffff;">© Pot-Sol Management, All Rights Reserved</p>
            </div>
            </div>
            """

            # Set up the email details
            email_msg = EmailMessage()
            email_msg.set_content(email_content, subtype='html')
            email_msg['Subject'] = "Welcome to Pot-Sol!"
            email_msg['From'] = "no.reply.pot.sol@gmail.com"
            email_msg['To'] = receiver_email

            # Set up the SMTP server (use your email credentials)
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("no.reply.pot.sol@gmail.com", "rfkh opci nhgs hyop")  # Replace with your email credentials
                    smtp.send_message(email_msg)
                return True
            except Exception as e:
                st.error(f"Failed to send welcome email. Error: {e}")
                return False
        
        # Final registration only if OTP is verified
        if st.session_state.otp_verified:
            if st.button("Register"):
                if new_username and new_password and registraion_email:
                    create_user(new_username, new_password, registraion_email)
                    st.success("Registration successful. You can now log in.")
                    send_welcome_email(registraion_email, new_username)
        else:
            st.info("Please verify the Email before proceeding with registration.")
    
    else:
        st.error("Passwords do not match")



if selected == "Raise Complaint":
    st.title("Raise a new Complaint")

    if st.session_state.get("logged_in", False):

        complaint_type = st.radio("Complaint Type", ["Pothole" , "Light Complaint" , "Other"], horizontal=True)
        complaint_title = st.text_input("Complaint Title")
        complaint_description = st.text_area("Complaint Description")
        priority = st.selectbox("Priority", ["High", "Low", "Mid"])
        raising_person_name = st.text_input("Your Name")
        
        raising_person_mobile = st.text_input("Your Mobile Number")
        if raising_person_mobile and not raising_person_mobile.isdigit():
            st.error("Please enter a valid phone number (numeric characters only).")
            raising_person_mobile = ""  # Clear the input if it's not valid
            
        raising_person_email = st.text_input("Your Email")
        email_pattern = r'^\S+@\S+\.\S+$'
        if raising_person_email:
            if not re.match(email_pattern, raising_person_email):
                st.error("Please enter a valid email address.")
        
        complaint_area = st.text_input("Complaint Area/Address")
        st.markdown(
            "<div style='text-align:center; margin: 10px 0;'><strong>OR</strong></div>", 
            unsafe_allow_html=True
        )
        
        with open('map.html', 'r') as file:
            map_html = file.read()

        st.components.v1.html(map_html, height=800)
        
                
        complaint_co = st.text_input("Enter the Coordinates")
            
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        st.write(f"**Note:** Please fill all fields")

        if st.button("Submit Complaint"):

            try:
                #print(complaint_type, complaint_title, complaint_description, complaint_area, priority, raising_person_name, raising_person_email, raising_person_mobile, uploaded_file)

                if (uploaded_file is not None and complaint_type !='' and complaint_title !='' and complaint_description !='' and (complaint_area != "" or complaint_co != "") and priority !='' and raising_person_name !='' ):
                    # Generate a random unique ID for the image filename
                    unique_id = str(uuid.uuid4().hex)[:8]
                    image_name = f"{unique_id}.png"  # Save all images as PNG for simplicity

                    # Save image to the folder
                    image_path = os.path.join(IMAGE_FOLDER, image_name)
                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getvalue())

                    cursor.execute('''
                        INSERT INTO Complaints (image_name, complaint_type, complaint_title, complaint_description, 
                                                complaint_area, complaint_co, priority, raising_person_name, 
                                                raising_person_mobile, raising_person_email, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (image_name, complaint_type, complaint_title, complaint_description, complaint_area, complaint_co,
                          priority, raising_person_name, raising_person_mobile, raising_person_email, 'Submitted'))

                    # cursor.execute('''
                    #         INSERT INTO Complaints (complaint_type, complaint_title, complaint_description,
                    #                                 complaint_area, priority, raising_person_name,
                    #                                 raising_person_mobile, raising_person_email, image_name)
                    #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    #     ''', (complaint_type, complaint_title, complaint_description, complaint_area,
                    #           priority, raising_person_name, raising_person_mobile, raising_person_email, image_name))
                    conn.commit()
                    st.success("Complaint submitted successfully.")
                    
                else:
                    st.warning("Please fill in all the required fields before submitting the complaint.")

            except Exception as e:
                st.error(f"Error: {e}")
                print(e)

    else:
        st.warning("Please log in to access this page.")

if selected == "View Complaint Status":
    st.title("View Complaint Status")

    if st.session_state.get("logged_in", False):

        cursor.execute('''SELECT complaint_type, complaint_title, complaint_description, 
                          complaint_area, complaint_co, priority, status, id, image_name FROM Complaints''')
        complaints = cursor.fetchall()

        for complaint in complaints:
            st.image(os.path.join(IMAGE_FOLDER, complaint[8]), caption=f"Image ID: {complaint[7]}", use_column_width=True)
            st.write(f"**Title:** {complaint[1]}")
            st.write(f"**Description:** {complaint[2]}")
            st.write(f"**Address:** {complaint[3]}")
            st.write(f"**Coordinates:** {complaint[4]}")
            st.write(f"**Type:** {complaint[0]} | **Priority:** {complaint[5]} | **Status:** {complaint[6]}")
            
            
            status = complaint[6]

            def update_progress(status):
                if status == "Submitted":
                    return 5
                elif status == "In-Queue":
                    return 25
                elif status == "In-Review":
                    return 50
                elif status == "Physical Verification":
                    return 75
                elif status == "Completed" or status == "Rejected":
                    return 100
                else:
                    return 0
            
            progress_value = update_progress(status)

            # Dynamically assign labels based on progress_value
            submitted_label = "📄  Submitted" if progress_value >= 5 else ""
            in_queue_label = "⏳  In-Queue" if progress_value >= 25 else ""
            in_review_label = "🔍  In-Review" if progress_value >= 50 else ""
            physical_verification_label = "🏗️  Physical Verification" if progress_value >= 75 else ""
            completion_label = "❌  Rejected" if status == "Rejected" else "✅  Completed" if status == "Completed" else ""

            # Build progress bar HTML
            progress_bar_html = f"""
            <div style="position: relative; height: 30px; width: 100%; background-color: #e0e0e0; border-radius: 10px;">
                <!-- Progress bar background -->
                <div style="height: 100%; width: {progress_value}%; background-color: {'red' if status == 'Rejected' else '#4CAF50'}; border-radius: 10px;"></div>
            </div>

            <!-- Labels below the progress bar -->
            <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 5px;">
                <span>{submitted_label}</span>
                <span>{in_queue_label}</span>
                <span>{in_review_label}</span>
                <span>{physical_verification_label}</span>
                <span>{completion_label}</span>
            </div>
            """

            # Render the progress bar
            st.markdown(progress_bar_html, unsafe_allow_html=True)


            # Icons for status
            icons_html = '<div style="text-align: left;">'
            
            st.write("---")

    else:
        st.warning("Please log in to access this page.")
        print("I'm warning")


if selected == "Logout":
    confirmation = st.warning("Are you sure you want to log out?")
    if confirmation.button("Do you want to log-out"):
        st.session_state.logged_in = False
        st.success("You have been logged out.")

# Close the database connection when the Streamlit app is done
conn.close()


