

# 🌐 PotSol – Pot-hole & Streetlight Complaint Management System

**PotSol** is a simple and effective web application designed to help users report potholes and faulty streetlights in their area. Built using **Streamlit**, **HTML/CSS**, **Python**, and integrated with **interactive maps**, this platform ensures real-time, location-based issue reporting for quicker municipal action.

---

## 🚀 Features

* 📍 **Location Pinpointing on Map**
  Users can select the **exact coordinates** of the issue using an interactive map for accurate complaint submission.

* 📝 **User Complaint Form**
  Simple and clean UI for users to submit complaints about:

  * Damaged roads / potholes
  * Non-working or broken street lights

* 🔐 **Secure Registration with OTP Verification**
  Users must **register using their email ID**, and complete a **one-time OTP verification** to authenticate.

* 🧾 **Admin Dashboard Panel** 
  Admin can login using their credential to view, update the status of complaint & delete the complaint.

* 🗂️ **Complaint History Log** *(Coming Soon)*
  Logged-in users will have access to their personal dashboard showing complaint history and responses.

---

## 🛠️ Tech Stack

| Component       | Technology                             |
| --------------- | -------------------------------------- |
| Frontend        | HTML, CSS                              |
| Backend         | Python (Streamlit)                     |
| Email OTP       | smtplib / email verification APIs      |
| Map Integration | Streamlit Map / Folium / OpenStreetMap |
| Hosting         | Streamlit Cloud / Local Server         |

---


## 🧠 Future Enhancements

* 📡 SMS or Email alerts once complaints are resolved
* 🔍 Filter and search complaints by area, type, and date
* 📊 Visual analytics dashboard for authorities
* 📷 Option to upload image proof of issue
* 👤 Role-based access (Admin / User)
* 📌 Auto-geolocation using user’s browser/device

---

## 📦 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/rohit6996/potsol.git
   cd potsol
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   streamlit run app.py
   ```

---

## 🧑‍💻 Author

**Rohit Bhandarkar**
📧 [rohitbhandarkar@email.com](mailto:rohitbhandarkar2205@email.com)
🔗 [LinkedIn](https://www.linkedin.com/in/rohit-bhandarkar-486158265/) • [GitHub](https://github.com/rohit6996)

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).
