import sqlite3
from tkinter import *
from tkinter import ttk, simpledialog
import requests

conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

class WeatherApp:
    def __init__(self, master):
        self.master = master
        self.logged_in_username = None

        self.create_database()

        self.title_frame = Frame(self.master, bg="#3498db", height=50)
        self.title_frame.pack(fill="x")

        self.name_label = Label(self.title_frame, text="Bharat Atmos", font=("Helvetica", 30, "bold"), fg="white", bg="#3498db")
        self.name_label.pack(side="left", padx=20)

        self.city_name_var = StringVar(value="Delhi")
        self.list_name = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
                          "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
                          "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim",
                          "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
                          "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli", "Daman and Diu", "Lakshadweep",
                          "National Capital Territory of Delhi", "Puducherry"]

        self.com = ttk.Combobox(self.master, values=self.list_name, font=("Helvetica", 18), textvariable=self.city_name_var, state="disabled")
        self.com.place(x=25, y=80, height=40, width=650)

        self.register_button = Button(self.master, text="Register", font=("Helvetica", 12, "bold"), command=self.register, bg="#3498db", fg="white")
        self.register_button.place(y=140, height=40, width=100, x=100)

        self.login_button = Button(self.master, text="Login", font=("Helvetica", 12, "bold"), command=self.login, bg="#3498db", fg="white")
        self.login_button.place(y=140, height=40, width=100, x=250)

        self.show_button = Button(self.master, text="SHOW", font=("Helvetica", 12, "bold"), command=self.data_get, bg="#2ecc71", fg="white", state="disabled")
        self.show_button.place(y=140, height=40, width=100, x=400)

        self.bookmark_button = Button(self.master, text="Bookmark", font=("Helvetica", 12, "bold"), command=self.add_to_bookmarks, bg="#3498db", fg="white", state="disabled")
        self.bookmark_button.place(y=140, height=40, width=100, x=550)

        self.w_label = Label(self.master, text="Weather Climate", font=("Helvetica", 20, "bold"), fg="#3498db", bg="#ecf0f1")
        self.w_label.place(x=25, y=200, height=40, width=650)
        self.w1_label = Label(self.master, text="", font=("Helvetica", 20), fg="#2c3e50", bg="#ecf0f1")
        self.w1_label.place(x=25, y=250, height=50, width=650)

        self.wb_label = Label(self.master, text="Weather Description", font=("Helvetica", 17, "bold"), fg="#3498db", bg="#ecf0f1")
        self.wb_label.place(x=25, y=330, height=40, width=650)
        self.wb_label1 = Label(self.master, text="", font=("Helvetica", 17), fg="#2c3e50", bg="#ecf0f1")
        self.wb_label1.place(x=25, y=370, height=50, width=650)

        self.w_progress = ttk.Progressbar(self.master, orient="horizontal", length=650, mode="determinate")
        self.w_progress.place(x=25, y=300, height=15)

        self.wb_progress = ttk.Progressbar(self.master, orient="horizontal", length=650, mode="determinate")
        self.wb_progress.place(x=25, y=420, height=15)

        self.temp_label = Label(self.master, text="Temperature", font=("Helvetica", 20, "bold"), fg="#3498db", bg="#ecf0f1")
        self.temp_label.place(x=25, y=470, height=40, width=650)
        self.temp_label1 = Label(self.master, text="", font=("Helvetica", 15), fg="#2c3e50", bg="#ecf0f1")
        self.temp_label1.place(x=25, y=510, height=50, width=650)

        self.temp_progress = ttk.Progressbar(self.master, orient="horizontal", length=650, mode="determinate")
        self.temp_progress.place(x=25, y=560, height=15)

        self.history_label = Label(self.master, text="Recent Searches", font=("Helvetica", 10, "bold"), fg="#3498db", bg="#ecf0f1")
        self.history_label.place(x=25, y=630)

        self.history_listbox = Listbox(self.master, font=("Helvetica", 10), selectbackground="#3498db", selectforeground="white")
        self.history_listbox.place(x=25, y=660, height=60, width=650)

        self.bookmark_label = Label(self.master, text="Bookmarks", font=("Helvetica", 12, "bold"), fg="#3498db", bg="#ecf0f1")
        self.bookmark_label.place(x=650, y=630)

        self.bookmark_listbox = Listbox(self.master, font=("Helvetica", 10), selectbackground="#3498db", selectforeground="white")
        self.bookmark_listbox.place(x=650, y=660, height=60, width=150)

        self.show_username_label = Label(self.master, text="", font=("Helvetica", 12, "bold"), fg="#3498db", bg="#ecf0f1")
        self.show_username_label.place(x=25, y=770, anchor="sw")

    def create_database(self):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def register(self):
        username = simpledialog.askstring("Register", "Enter a new username:")
        password = simpledialog.askstring("Register", "Enter a password:")

        if username and password:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            print("Registration successful")
            self.logged_in_username = username
            self.show_username_label.config(text=f"Logged in as: {self.logged_in_username}")
            self.setup_weather_ui()
        else:
            print("Invalid registration details")

    def login(self):
        username = simpledialog.askstring("Login", "Enter your username:")
        password = simpledialog.askstring("Login", "Enter your password:")

        if username and password:
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                print("Login successful")
                self.logged_in_username = username
                self.show_username_label.config(text=f"Logged in as: {self.logged_in_username}")
                self.setup_weather_ui()
            else:
                print("Invalid username or password")
        else:
            print("Login failed")

    def setup_weather_ui(self):
        self.com.config(state="normal")
        self.show_button.config(state="normal")
        self.bookmark_button.config(state="normal")

    def data_get(self):
        City = self.city_name_var.get()
        data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={City}&appid=f7a4cc7db4e85381ff3710e9d3a45510").json()
        self.w1_label.config(text=data["weather"][0]["main"])
        self.wb_label1.config(text=data["weather"][0]["description"])

        self.w_progress['value'] = 100 if data["weather"][0]["main"] == "Clear" else 50
        self.wb_progress['value'] = 100 if "clear" in data["weather"][0]["description"].lower() else 50

        temp_in_celsius = data["main"]["temp"] - 273.15
        self.temp_label1.config(text=f"{temp_in_celsius:.2f} °C", font=("Helvetica", 15))
        self.temp_progress['value'] = (temp_in_celsius + 10) / 50 * 100

        self.update_background(data["weather"][0]["main"])

        self.add_to_history(City)

    def update_background(self, weather_condition):
        if weather_condition.lower() == "clear":
            self.master.config(bg="#87CEEB")
        else:
            self.master.config(bg="#808080")

    def add_to_history(self, city):
        self.history_listbox.insert(0, city)

    def add_to_bookmarks(self):
        selected_indices = self.history_listbox.curselection()
        if selected_indices:
            selected_item = self.history_listbox.get(selected_indices[0])
            self.bookmark_listbox.insert(0, selected_item)
        else:
            print("No item selected from history to bookmark")

if __name__ == "__main__":
    root = Tk()
    app = WeatherApp(root)
    root.geometry("800x800")
    root.mainloop()
    conn.close()
