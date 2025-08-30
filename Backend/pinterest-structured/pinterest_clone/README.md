# 📌 Pinterest Clone (Flask Mini Project)

A simple Pinterest-like web application built with **Flask** and **SQLite**.  
Users can register, log in, upload pins (images), view other users’ pins, and save/unsave pins to their profile.  

---

## 🚀 Features
- User authentication (register, login, logout)
- Profile management (name, bio, profile picture)
- Upload pins with title, description, and image
- Save/unsave pins (like Pinterest boards)
- View all users and their pins
- Flash messages for user feedback
- Basic file upload handling (images only)

---

## 🛠 Tech Stack
- **Backend:** Flask, SQLAlchemy
- **Database:** SQLite
- **Frontend:** Jinja2 templates, HTML, CSS
- **Other:** Werkzeug (password hashing), Session management

---

## 📂 Project Structure
```

pinterest\_clone/
│
├── app/
│   ├── **init**.py          # App factory & config
│   ├── controllers/         # Route controllers (user, pin)
│   ├── models/              # Database models
│   ├── db/                  # DB configs
│   ├── utils/               # Utility functions
│   ├── templates/           # Jinja2 templates (HTML)
│   └── static/              # Static files (CSS, JS, uploads)
│
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
└── README.md                # Project info

````

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/pinterest-clone.git
   cd pinterest-clone


2. **Create virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project**

   ```bash
   python main.py
   ```

5. Open your browser → [http://localhost:5000](http://localhost:5000)

---

## 📸 Screenshots (Optional)

*Add some screenshots of your UI here*

---

## ✅ Future Improvements

* Add comments on pins
* Create boards (collections of pins)
* Add likes & notifications
* Deploy on Heroku/VPS

---

## 👨‍💻 Author

Developed by **Your Name**
📧 Contact: [your.email@example.com](mailto:your.email@example.com)

```