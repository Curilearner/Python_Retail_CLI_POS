import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import hashlib

# Professional color scheme inspired by Netflix
COLORS = {
    "bg": "#141414",          # Netflix dark background
    "card": "#181818",        # Card background
    "primary": "#E50914",     # Netflix red
    "secondary": "#B20710",    # Darker red
    "text": "#FFFFFF",        # White text
    "muted": "#B3B3B3",      # Muted text
    "input": "#333333",       # Input field background
    "border": "#404040",      # Border color
    "hover": "#F40612",       # Hover red
    "success": "#46D369",     # Success green
    "error": "#E87C03",       # Error orange
}

# User data file
USER_DATA_FILE = "users.json"

# ----------------- User Authentication ----------------- #

def ensure_user_file():
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w") as f:
            json.dump({}, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(username, password, name=""):
    ensure_user_file()
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)
    
    users[username] = {
        "password": hash_password(password),
        "name": name
    }
    
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

def verify_user(username, password):
    ensure_user_file()
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)
    
    if username in users:
        return users[username]["password"] == hash_password(password)
    return False

def user_exists(username):
    ensure_user_file()
    with open(USER_DATA_FILE, "r") as f:
        users = json.load(f)
    return username in users

# ----------------- Login & Signup Classes ----------------- #

class NetflixLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Billing System - Login")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.configure(bg=COLORS["bg"])
        
        self.center_window()
        self.main_frame = tk.Frame(root, bg=COLORS["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Logo and branding
        self.left_frame = tk.Frame(self.main_frame, bg=COLORS["bg"], width=450)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Logo
        self.logo_label = tk.Label(self.left_frame, text="RETAIL", 
                                  font=("Arial", 48, "bold"), 
                                  fg=COLORS["primary"], 
                                  bg=COLORS["bg"])
        self.logo_label.pack(pady=(150, 0))
        
        self.logo_label2 = tk.Label(self.left_frame, text="BILLING", 
                                   font=("Arial", 48, "bold"), 
                                   fg=COLORS["text"], 
                                   bg=COLORS["bg"])
        self.logo_label2.pack()
        
        self.tagline = tk.Label(self.left_frame, text="Professional Retail Management", 
                               font=("Arial", 14), 
                               fg=COLORS["muted"], 
                               bg=COLORS["bg"])
        self.tagline.pack(pady=(20, 0))
        
        # Right side - Login form
        self.right_frame = tk.Frame(self.main_frame, bg=COLORS["card"], width=450)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_login_card()
        self.configure_styles()
        self.root.bind("<Return>", lambda e: self.login())
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_login_card(self):
        self.canvas = tk.Canvas(self.right_frame, bg=COLORS["card"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["card"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.login_card = tk.Frame(self.scrollable_frame, bg=COLORS["card"], padx=60, pady=40)
        self.login_card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = tk.Label(self.login_card, text="Sign In", 
                                   font=("Arial", 32, "bold"), 
                                   fg=COLORS["text"], 
                                   bg=COLORS["card"])
        self.title_label.pack(anchor=tk.W, pady=(0, 30))
        
        # Email/Username
        self.email_label = tk.Label(self.login_card, text="Email or username", 
                                   font=("Arial", 12), 
                                   fg=COLORS["text"], 
                                   bg=COLORS["card"])
        self.email_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.email_entry = tk.Entry(self.login_card, 
                                   font=("Arial", 14), 
                                   bg=COLORS["input"], 
                                   fg=COLORS["text"], 
                                   insertbackground=COLORS["text"],
                                   relief=tk.FLAT,
                                   bd=0,
                                   highlightthickness=1,
                                   highlightbackground=COLORS["border"],
                                   highlightcolor=COLORS["primary"])
        self.email_entry.pack(fill=tk.X, pady=(0, 20), ipady=10)
        
        # Password
        self.password_label = tk.Label(self.login_card, text="Password", 
                                      font=("Arial", 12), 
                                      fg=COLORS["text"], 
                                      bg=COLORS["card"])
        self.password_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = tk.Entry(self.login_card, 
                                      font=("Arial", 14), 
                                      bg=COLORS["input"], 
                                      fg=COLORS["text"], 
                                      insertbackground=COLORS["text"],
                                      relief=tk.FLAT,
                                      bd=0,
                                      highlightthickness=1,
                                      highlightbackground=COLORS["border"],
                                      highlightcolor=COLORS["primary"],
                                      show="•")
        self.password_entry.pack(fill=tk.X, pady=(0, 30), ipady=10)
        
        # Login button
        self.login_button = tk.Button(self.login_card, 
                                     text="Sign In", 
                                     font=("Arial", 16, "bold"), 
                                     bg=COLORS["primary"], 
                                     fg=COLORS["text"],
                                     activebackground=COLORS["hover"],
                                     activeforeground=COLORS["text"],
                                     relief=tk.FLAT,
                                     bd=0,
                                     pady=12,
                                     command=self.login)
        self.login_button.pack(fill=tk.X, pady=(0, 20))
        
        # Remember me and help links
        self.links_frame = tk.Frame(self.login_card, bg=COLORS["card"])
        self.links_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.remember_var = tk.BooleanVar()
        self.remember_check = tk.Checkbutton(self.links_frame, 
                                            text="Remember me", 
                                            variable=self.remember_var,
                                            font=("Arial", 12),
                                            fg=COLORS["muted"],
                                            selectcolor=COLORS["card"],
                                            activebackground=COLORS["card"],
                                            activeforeground=COLORS["muted"],
                                            bg=COLORS["card"],
                                            relief=tk.FLAT,
                                            bd=0,
                                            highlightthickness=0)
        self.remember_check.pack(side=tk.LEFT)
        
        self.help_link = tk.Label(self.links_frame, 
                                 text="Need help?", 
                                 font=("Arial", 12), 
                                 fg=COLORS["muted"], 
                                 bg=COLORS["card"],
                                 cursor="hand2")
        self.help_link.pack(side=tk.RIGHT)
        
        # Signup link
        self.signup_frame = tk.Frame(self.login_card, bg=COLORS["card"])
        self.signup_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.signup_text = tk.Label(self.signup_frame, 
                                   text="New to Retail Billing? ", 
                                   font=("Arial", 14), 
                                   fg=COLORS["muted"], 
                                   bg=COLORS["card"])
        self.signup_text.pack(side=tk.LEFT)
        
        self.signup_link = tk.Label(self.signup_frame, 
                                   text="Sign up now.", 
                                   font=("Arial", 14, "bold"), 
                                   fg=COLORS["text"], 
                                   bg=COLORS["card"],
                                   cursor="hand2")
        self.signup_link.pack(side=tk.LEFT)
        self.signup_link.bind("<Button-1>", lambda e: self.show_signup())
    
    def configure_styles(self):
        def on_entry_focus_in(entry, event):
            entry.config(highlightbackground=COLORS["primary"], highlightcolor=COLORS["primary"])
        
        def on_entry_focus_out(entry, event):
            entry.config(highlightbackground=COLORS["border"], highlightcolor=COLORS["border"])
        
        self.email_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(self.email_entry, e))
        self.email_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(self.email_entry, e))
        self.password_entry.bind("<FocusIn>", lambda e: on_entry_focus_in(self.password_entry, e))
        self.password_entry.bind("<FocusOut>", lambda e: on_entry_focus_out(self.password_entry, e))
    
    def login(self):
        username = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if verify_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            root = tk.Tk()
            app = RetailBillingApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def show_signup(self):
        self.root.destroy()
        root = tk.Tk()
        app = NetflixSignupApp(root)
        root.mainloop()

class NetflixSignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Billing System - Sign Up")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.configure(bg=COLORS["bg"])
        
        self.center_window()
        self.main_frame = tk.Frame(root, bg=COLORS["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Logo and branding
        self.left_frame = tk.Frame(self.main_frame, bg=COLORS["bg"], width=450)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Logo
        self.logo_label = tk.Label(self.left_frame, text="RETAIL", 
                                  font=("Arial", 48, "bold"), 
                                  fg=COLORS["primary"], 
                                  bg=COLORS["bg"])
        self.logo_label.pack(pady=(150, 0))
        
        self.logo_label2 = tk.Label(self.left_frame, text="BILLING", 
                                   font=("Arial", 48, "bold"), 
                                   fg=COLORS["text"], 
                                   bg=COLORS["bg"])
        self.logo_label2.pack()
        
        self.tagline = tk.Label(self.left_frame, text="Professional Retail Management", 
                               font=("Arial", 14), 
                               fg=COLORS["muted"], 
                               bg=COLORS["bg"])
        self.tagline.pack(pady=(20, 0))
        
        # Right side - Signup form with scrollbar
        self.right_frame = tk.Frame(self.main_frame, bg=COLORS["card"], width=450)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_signup_card()
        self.configure_styles()
        self.root.bind("<Return>", lambda e: self.signup())
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_signup_card(self):
        self.canvas = tk.Canvas(self.right_frame, bg=COLORS["card"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["card"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.signup_card = tk.Frame(self.scrollable_frame, bg=COLORS["card"], padx=60, pady=40)
        self.signup_card.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = tk.Label(self.signup_card, text="Sign Up", 
                                   font=("Arial", 32, "bold"), 
                                   fg=COLORS["text"], 
                                   bg=COLORS["card"])
        self.title_label.pack(anchor=tk.W, pady=(0, 20))
        
        # Full Name
        self.name_label = tk.Label(self.signup_card, text="Full Name", 
                                  font=("Arial", 12), 
                                  fg=COLORS["text"], 
                                  bg=COLORS["card"])
        self.name_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.name_entry = tk.Entry(self.signup_card, 
                                  font=("Arial", 14), 
                                  bg=COLORS["input"], 
                                  fg=COLORS["text"], 
                                  insertbackground=COLORS["text"],
                                  relief=tk.FLAT,
                                  bd=0,
                                  highlightthickness=1,
                                  highlightbackground=COLORS["border"],
                                  highlightcolor=COLORS["primary"])
        self.name_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Email
        self.email_label = tk.Label(self.signup_card, text="Email", 
                                   font=("Arial", 12), 
                                   fg=COLORS["text"], 
                                   bg=COLORS["card"])
        self.email_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.email_entry = tk.Entry(self.signup_card, 
                                  font=("Arial", 14), 
                                  bg=COLORS["input"], 
                                  fg=COLORS["text"], 
                                  insertbackground=COLORS["text"],
                                  relief=tk.FLAT,
                                  bd=0,
                                  highlightthickness=1,
                                  highlightbackground=COLORS["border"],
                                  highlightcolor=COLORS["primary"])
        self.email_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Username
        self.username_label = tk.Label(self.signup_card, text="Username", 
                                     font=("Arial", 12), 
                                     fg=COLORS["text"], 
                                     bg=COLORS["card"])
        self.username_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.username_entry = tk.Entry(self.signup_card, 
                                     font=("Arial", 14), 
                                     bg=COLORS["input"], 
                                     fg=COLORS["text"], 
                                     insertbackground=COLORS["text"],
                                     relief=tk.FLAT,
                                     bd=0,
                                     highlightthickness=1,
                                     highlightbackground=COLORS["border"],
                                     highlightcolor=COLORS["primary"])
        self.username_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Password
        self.password_label = tk.Label(self.signup_card, text="Password", 
                                      font=("Arial", 12), 
                                      fg=COLORS["text"], 
                                      bg=COLORS["card"])
        self.password_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = tk.Entry(self.signup_card, 
                                      font=("Arial", 14), 
                                      bg=COLORS["input"], 
                                      fg=COLORS["text"], 
                                      insertbackground=COLORS["text"],
                                      relief=tk.FLAT,
                                      bd=0,
                                      highlightthickness=1,
                                      highlightbackground=COLORS["border"],
                                      highlightcolor=COLORS["primary"],
                                      show="•")
        self.password_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Confirm Password
        self.confirm_label = tk.Label(self.signup_card, text="Confirm Password", 
                                     font=("Arial", 12), 
                                     fg=COLORS["text"], 
                                     bg=COLORS["card"])
        self.confirm_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.confirm_entry = tk.Entry(self.signup_card, 
                                    font=("Arial", 14), 
                                    bg=COLORS["input"], 
                                    fg=COLORS["text"], 
                                    insertbackground=COLORS["text"],
                                    relief=tk.FLAT,
                                    bd=0,
                                    highlightthickness=1,
                                    highlightbackground=COLORS["border"],
                                    highlightcolor=COLORS["primary"],
                                    show="•")
        self.confirm_entry.pack(fill=tk.X, pady=(0, 25), ipady=8)
        
        # Signup button
        self.signup_button = tk.Button(self.signup_card, 
                                     text="Sign Up", 
                                     font=("Arial", 16, "bold"), 
                                     bg=COLORS["primary"], 
                                     fg=COLORS["text"],
                                     activebackground=COLORS["hover"],
                                     activeforeground=COLORS["text"],
                                     relief=tk.FLAT,
                                     bd=0,
                                     pady=12,
                                     command=self.signup)
        self.signup_button.pack(fill=tk.X, pady=(0, 20))
        
        # Login link
        self.login_frame = tk.Frame(self.signup_card, bg=COLORS["card"])
        self.login_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.login_text = tk.Label(self.login_frame, 
                                 text="Already have an account? ", 
                                 font=("Arial", 14), 
                                 fg=COLORS["muted"], 
                                 bg=COLORS["card"])
        self.login_text.pack(side=tk.LEFT)
        
        self.login_link = tk.Label(self.login_frame, 
                                 text="Sign in.", 
                                 font=("Arial", 14, "bold"), 
                                 fg=COLORS["text"], 
                                 bg=COLORS["card"],
                                 cursor="hand2")
        self.login_link.pack(side=tk.LEFT)
        self.login_link.bind("<Button-1>", lambda e: self.show_login())
    
    def configure_styles(self):
        def on_entry_focus_in(entry, event):
            entry.config(highlightbackground=COLORS["primary"], highlightcolor=COLORS["primary"])
        
        def on_entry_focus_out(entry, event):
            entry.config(highlightbackground=COLORS["border"], highlightcolor=COLORS["border"])
        
        entries = [self.name_entry, self.email_entry, self.username_entry, 
                  self.password_entry, self.confirm_entry]
        
        for entry in entries:
            entry.bind("<FocusIn>", lambda e, ent=entry: on_entry_focus_in(ent, e))
            entry.bind("<FocusOut>", lambda e, ent=entry: on_entry_focus_out(ent, e))
    
    def signup(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        
        if not name or not email or not username or not password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        if user_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return
        
        save_user(username, password, name)
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login()
    
    def show_login(self):
        self.root.destroy()
        root = tk.Tk()
        app = NetflixLoginApp(root)
        root.mainloop()

# ----------------- Main Application ----------------- #

class RetailBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Billing System")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        self.root.configure(bg=COLORS["bg"])
        
        self.products = {}
        self.sales = []
        self.load_data()
        
        self.main_frame = tk.Frame(root, bg=COLORS["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_frame = tk.Frame(self.main_frame, bg=COLORS["bg"])
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.title_label = tk.Label(self.header_frame, text="RETAIL BILLING SYSTEM", 
                                   font=("Arial", 28, "bold"), 
                                   fg=COLORS["primary"], 
                                   bg=COLORS["bg"])
        self.title_label.pack(side=tk.LEFT)
        
        self.date_label = tk.Label(self.header_frame, text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                                  font=("Arial", 14), 
                                  fg=COLORS["muted"], 
                                  bg=COLORS["bg"])
        self.date_label.pack(side=tk.RIGHT)
        
        # Navigation buttons
        self.nav_frame = tk.Frame(self.main_frame, bg=COLORS["bg"])
        self.nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.sales_btn = tk.Button(self.nav_frame, text="POS & Sales", 
                                  font=("Arial", 14, "bold"), 
                                  bg=COLORS["primary"], 
                                  fg=COLORS["text"],
                                  activebackground=COLORS["hover"],
                                  activeforeground=COLORS["text"],
                                  relief=tk.FLAT,
                                  bd=0,
                                  pady=12,
                                  width=15,
                                  command=self.open_sales)
        self.sales_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.inventory_btn = tk.Button(self.nav_frame, text="Inventory Management", 
                                      font=("Arial", 14, "bold"), 
                                      bg=COLORS["card"], 
                                      fg=COLORS["text"],
                                      activebackground=COLORS["hover"],
                                      activeforeground=COLORS["text"],
                                      relief=tk.FLAT,
                                      bd=0,
                                      pady=12,
                                      width=20,
                                      command=self.open_inventory)
        self.inventory_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Dashboard cards
        self.dashboard_frame = tk.Frame(self.main_frame, bg=COLORS["bg"])
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sales Summary Card
        self.sales_card = tk.Frame(self.dashboard_frame, bg=COLORS["card"], padx=20, pady=20)
        self.sales_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(self.sales_card, text="Today's Sales", font=("Arial", 18, "bold"), 
                fg=COLORS["text"], bg=COLORS["card"]).pack(anchor=tk.W)
        
        self.sales_amount = tk.Label(self.sales_card, text="₹0.00", font=("Arial", 32, "bold"), 
                                   fg=COLORS["success"], bg=COLORS["card"])
        self.sales_amount.pack(anchor=tk.W, pady=(10, 5))
        
        tk.Label(self.sales_card, text="0 Transactions", font=("Arial", 14), 
                fg=COLORS["muted"], bg=COLORS["card"]).pack(anchor=tk.W)
        
        # Inventory Summary Card
        self.inventory_card = tk.Frame(self.dashboard_frame, bg=COLORS["card"], padx=20, pady=20)
        self.inventory_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(self.inventory_card, text="Inventory Status", font=("Arial", 18, "bold"), 
                fg=COLORS["text"], bg=COLORS["card"]).pack(anchor=tk.W)
        
        self.product_count = tk.Label(self.inventory_card, text="0 Products", font=("Arial", 24, "bold"), 
                                    fg=COLORS["primary"], bg=COLORS["card"])
        self.product_count.pack(anchor=tk.W, pady=(10, 5))
        
        tk.Label(self.inventory_card, text="0 Low Stock Items", font=("Arial", 14), 
                fg=COLORS["muted"], bg=COLORS["card"]).pack(anchor=tk.W)
        
        self.update_dashboard()
        self.update_time()
    
    def update_time(self):
        self.date_label.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    def update_dashboard(self):
        today = datetime.now().date()
        today_sales = [sale for sale in self.sales if sale['date'].date() == today]
        total_sales = sum(sale['total'] for sale in today_sales)
        
        self.sales_amount.config(text=f"₹{total_sales:.2f}")
        self.product_count.config(text=f"{len(self.products)} Products")
    
    def open_sales(self):
        SalesWindow(self)
    
    def open_inventory(self):
        InventoryWindow(self)
    
    def load_data(self):
        try:
            if os.path.exists("products.json"):
                with open("products.json", "r") as f:
                    data = json.load(f)
                    self.products = {int(k): v for k, v in data.items()}
        except:
            self.products = {}
        
        try:
            if os.path.exists("sales.json"):
                with open("sales.json", "r") as f:
                    sales_data = json.load(f)
                    self.sales = []
                    for sale in sales_data:
                        sale['date'] = datetime.fromisoformat(sale['date'])
                        self.sales.append(sale)
        except:
            self.sales = []
    
    def save_data(self):
        with open("products.json", "w") as f:
            json.dump(self.products, f, indent=2)
        
        sales_data = []
        for sale in self.sales:
            sale_copy = sale.copy()
            sale_copy['date'] = sale['date'].isoformat()
            sales_data.append(sale_copy)
        
        with open("sales.json", "w") as f:
            json.dump(sales_data, f, indent=2)

class SalesWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Point of Sale")
        self.window.geometry("1000x700")
        self.window.configure(bg=COLORS["bg"])
        self.window.resizable(True, True)
        
        self.cart = []
        self.current_sale_id = len(parent.sales) + 1
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.window, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Product selection
        left_frame = tk.Frame(main_frame, bg=COLORS["bg"], width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Product search
        search_frame = tk.Frame(left_frame, bg=COLORS["bg"])
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search Products:", font=("Arial", 12, "bold"), 
                fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor=tk.W)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                                    font=("Arial", 14), bg=COLORS["input"], fg=COLORS["text"],
                                    relief=tk.FLAT, bd=0)
        self.search_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        self.search_entry.bind("<KeyRelease>", self.search_products)
        
        # Products list with scrollbar
        products_container = tk.Frame(left_frame, bg=COLORS["bg"])
        products_container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(products_container, text="Available Products:", font=("Arial", 12, "bold"), 
                fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor=tk.W)
        
        # Create treeview for products
        self.products_tree = ttk.Treeview(products_container, columns=("Name", "Price", "Stock"), 
                                         show="headings", height=15)
        self.products_tree.heading("Name", text="Product Name")
        self.products_tree.heading("Price", text="Price (₹)")
        self.products_tree.heading("Stock", text="In Stock")
        
        self.products_tree.column("Name", width=200)
        self.products_tree.column("Price", width=100)
        self.products_tree.column("Stock", width=80)
        
        self.products_tree.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        self.products_tree.bind("<Double-1>", self.add_to_cart)
        
        # Right side - Cart
        right_frame = tk.Frame(main_frame, bg=COLORS["bg"], width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Cart header
        cart_header = tk.Frame(right_frame, bg=COLORS["card"], pady=10)
        cart_header.pack(fill=tk.X)
        
        tk.Label(cart_header, text="Shopping Cart", font=("Arial", 18, "bold"), 
                fg=COLORS["text"], bg=COLORS["card"]).pack()
        
        # Cart items with scrollbar
        cart_container = tk.Frame(right_frame, bg=COLORS["bg"])
        cart_container.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.cart_tree = ttk.Treeview(cart_container, 
                                     columns=("Product", "Qty", "Price", "Total"), 
                                     show="headings", height=12)
        self.cart_tree.heading("Product", text="Product")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Total", text="Total")
        
        self.cart_tree.column("Product", width=150)
        self.cart_tree.column("Qty", width=60)
        self.cart_tree.column("Price", width=80)
        self.cart_tree.column("Total", width=80)
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        # Cart summary
        summary_frame = tk.Frame(right_frame, bg=COLORS["card"], pady=10)
        summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.total_label = tk.Label(summary_frame, text="Total: ₹0.00", 
                                   font=("Arial", 16, "bold"), 
                                   fg=COLORS["text"], bg=COLORS["card"])
        self.total_label.pack()
        
        # Cart actions
        actions_frame = tk.Frame(right_frame, bg=COLORS["bg"])
        actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.remove_btn = tk.Button(actions_frame, text="Remove Item", 
                                   font=("Arial", 12), 
                                   bg=COLORS["error"], 
                                   fg=COLORS["text"],
                                   relief=tk.FLAT,
                                   command=self.remove_from_cart)
        self.remove_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_btn = tk.Button(actions_frame, text="Clear Cart", 
                                  font=("Arial", 12), 
                                  bg=COLORS["secondary"], 
                                  fg=COLORS["text"],
                                  relief=tk.FLAT,
                                  command=self.clear_cart)
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Checkout button
        self.checkout_btn = tk.Button(right_frame, text="Process Payment", 
                                     font=("Arial", 14, "bold"), 
                                     bg=COLORS["success"], 
                                     fg=COLORS["text"],
                                     relief=tk.FLAT,
                                     bd=0,
                                     pady=12,
                                     command=self.process_payment)
        self.checkout_btn.pack(fill=tk.X, pady=(10, 0))
    
    def load_products(self):
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Add products to treeview
        for product_id, product in self.parent.products.items():
            self.products_tree.insert("", "end", values=(
                product["name"], 
                f"₹{product['price']:.2f}", 
                product["quantity"]
            ), tags=(str(product_id),))
    
    def search_products(self, event=None):
        query = self.search_var.get().lower()
        
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        for product_id, product in self.parent.products.items():
            if query in product["name"].lower():
                self.products_tree.insert("", "end", values=(
                    product["name"], 
                    f"₹{product['price']:.2f}", 
                    product["quantity"]
                ), tags=(str(product_id),))
    
    def add_to_cart(self, event):
        selected = self.products_tree.selection()
        if not selected:
            return
        
        item = self.products_tree.item(selected[0])
        product_id = int(item["tags"][0])
        product = self.parent.products[product_id]
        
        # Check if product already in cart
        for i, cart_item in enumerate(self.cart):
            if cart_item["id"] == product_id:
                if cart_item["quantity"] < product["quantity"]:
                    self.cart[i]["quantity"] += 1
                    self.cart[i]["total"] = self.cart[i]["quantity"] * self.cart[i]["price"]
                else:
                    messagebox.showwarning("Warning", "Not enough stock available!")
                self.update_cart_display()
                return
        
        # Add new item to cart
        if product["quantity"] > 0:
            self.cart.append({
                "id": product_id,
                "name": product["name"],
                "price": product["price"],
                "quantity": 1,
                "total": product["price"]
            })
            self.update_cart_display()
        else:
            messagebox.showwarning("Warning", "Product out of stock!")
    
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            return
        
        item_index = self.cart_tree.index(selected[0])
        self.cart.pop(item_index)
        self.update_cart_display()
    
    def clear_cart(self):
        self.cart = []
        self.update_cart_display()
    
    def update_cart_display(self):
        # Clear cart display
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add cart items
        total_amount = 0
        for item in self.cart:
            self.cart_tree.insert("", "end", values=(
                item["name"],
                item["quantity"],
                f"₹{item['price']:.2f}",
                f"₹{item['total']:.2f}"
            ))
            total_amount += item["total"]
        
        self.total_label.config(text=f"Total: ₹{total_amount:.2f}")
    
    def process_payment(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty!")
            return
        
        total_amount = sum(item["total"] for item in self.cart)
        
        # Create sale record
        sale = {
            "id": self.current_sale_id,
            "date": datetime.now(),
            "items": self.cart.copy(),
            "total": total_amount
        }
        
        # Update inventory
        for item in self.cart:
            product_id = item["id"]
            if product_id in self.parent.products:
                self.parent.products[product_id]["quantity"] -= item["quantity"]
        
        # Add to sales history
        self.parent.sales.append(sale)
        self.current_sale_id += 1
        
        # Save data
        self.parent.save_data()
        
        messagebox.showinfo("Success", f"Payment processed successfully!\nTotal: ₹{total_amount:.2f}")
        
        # Clear cart and update displays
        self.clear_cart()
        self.load_products()
        self.parent.update_dashboard()

class InventoryWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent.root)
        self.window.title("Inventory Management")
        self.window.geometry("1000x600")
        self.window.configure(bg=COLORS["bg"])
        self.window.resizable(True, True)
        
        self.create_widgets()
        self.load_inventory()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.window, bg=COLORS["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="Inventory Management", 
                font=("Arial", 24, "bold"), fg=COLORS["text"], bg=COLORS["bg"]).pack(side=tk.LEFT)
        
        # Add product button
        self.add_btn = tk.Button(header_frame, text="Add Product", 
                                font=("Arial", 12, "bold"), 
                                bg=COLORS["success"], 
                                fg=COLORS["text"],
                                relief=tk.FLAT,
                                bd=0,
                                pady=8,
                                padx=20,
                                command=self.add_product)
        self.add_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Edit product button
        self.edit_btn = tk.Button(header_frame, text="Edit Product", 
                                 font=("Arial", 12, "bold"), 
                                 bg=COLORS["primary"], 
                                 fg=COLORS["text"],
                                 relief=tk.FLAT,
                                 bd=0,
                                 pady=8,
                                 padx=20,
                                 command=self.edit_product)
        self.edit_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Delete product button
        self.delete_btn = tk.Button(header_frame, text="Delete Product", 
                                   font=("Arial", 12, "bold"), 
                                   bg=COLORS["error"], 
                                   fg=COLORS["text"],
                                   relief=tk.FLAT,
                                   bd=0,
                                   pady=8,
                                   padx=20,
                                   command=self.delete_product)
        self.delete_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Inventory table
        table_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbar
        self.tree = ttk.Treeview(table_frame, 
                                columns=("ID", "Name", "Price", "Quantity", "Category"),
                                show="headings", height=20)
        
        # Define headings
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Product Name")
        self.tree.heading("Price", text="Price (₹)")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Category", text="Category")
        
        # Define columns
        self.tree.column("ID", width=80)
        self.tree.column("Name", width=250)
        self.tree.column("Price", width=120)
        self.tree.column("Quantity", width=100)
        self.tree.column("Category", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def load_inventory(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add products to treeview
        for product_id, product in self.parent.products.items():
            self.tree.insert("", "end", values=(
                product_id,
                product["name"],
                f"₹{product['price']:.2f}",
                product["quantity"],
                product.get("category", "Uncategorized")
            ))
    
    def add_product(self):
        dialog = AddProductDialog(self.window)
        self.window.wait_window(dialog.dialog)
        
        if dialog.result:
            product_id = max(self.parent.products.keys(), default=0) + 1
            self.parent.products[product_id] = dialog.result
            self.parent.save_data()
            self.load_inventory()
            self.parent.update_dashboard()
    
    def edit_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return
        
        item = self.tree.item(selected[0])
        product_id = item["values"][0]
        product = self.parent.products[product_id]
        
        dialog = AddProductDialog(self.window, product)
        self.window.wait_window(dialog.dialog)
        
        if dialog.result:
            self.parent.products[product_id] = dialog.result
            self.parent.save_data()
            self.load_inventory()
    
    def delete_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        item = self.tree.item(selected[0])
        product_name = item["values"][1]
        product_id = item["values"][0]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            del self.parent.products[product_id]
            self.parent.save_data()
            self.load_inventory()
            self.parent.update_dashboard()

class AddProductDialog:
    def __init__(self, parent, product=None):
        self.parent = parent
        self.product = product
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Product" if not product else "Edit Product")
        self.dialog.geometry("400x400")
        self.dialog.configure(bg=COLORS["bg"])
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.center_dialog()
        self.create_widgets()
    
    def center_dialog(self):
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        main_frame = tk.Frame(self.dialog, bg=COLORS["bg"], padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(main_frame, text="Add Product" if not self.product else "Edit Product", 
                        font=("Arial", 20, "bold"), fg=COLORS["text"], bg=COLORS["bg"])
        title.pack(pady=(0, 20))
        
        # Product Name
        tk.Label(main_frame, text="Product Name:", font=("Arial", 12), 
                fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar(value=self.product["name"] if self.product else "")
        self.name_entry = tk.Entry(main_frame, textvariable=self.name_var, font=("Arial", 14), 
                                  bg=COLORS["input"], fg=COLORS["text"], relief=tk.FLAT)
        self.name_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Price
        tk.Label(main_frame, text="Price (₹):", font=("Arial", 12), 
                fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor=tk.W, pady=(0, 5))
        self.price_var = tk.StringVar(value=str(self.product["price"]) if self.product else "0.00")
        self.price_entry = tk.Entry(main_frame, textvariable=self.price_var, font=("Arial", 14), 
                                   bg=COLORS["input"], fg=COLORS["text"], relief=tk.FLAT)
        self.price_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Quantity
        tk.Label(main_frame, text="Quantity:", font=("Arial", 12), 
                fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor=tk.W, pady=(0, 5))
        self.quantity_var = tk.StringVar(value=str(self.product["quantity"]) if self.product else "0")
        self.quantity_entry = tk.Entry(main_frame, textvariable=self.quantity_var, font=("Arial", 14), 
                                      bg=COLORS["input"], fg=COLORS["text"], relief=tk.FLAT)
        self.quantity_entry.pack(fill=tk.X, pady=(0, 15), ipady=8)
        
        # Category
        tk.Label(main_frame, text="Category:", font=("Arial", 12), 
                fg=COLORS["text"], bg=COLORS["bg"]).pack(anchor=tk.W, pady=(0, 5))
        self.category_var = tk.StringVar(value=self.product.get("category", "") if self.product else "")
        self.category_entry = tk.Entry(main_frame, textvariable=self.category_var, font=("Arial", 14), 
                                      bg=COLORS["input"], fg=COLORS["text"], relief=tk.FLAT)
        self.category_entry.pack(fill=tk.X, pady=(0, 25), ipady=8)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg=COLORS["bg"])
        button_frame.pack(fill=tk.X)
        
        self.save_btn = tk.Button(button_frame, text="Save", 
                                 font=("Arial", 14, "bold"), 
                                 bg=COLORS["success"], 
                                 fg=COLORS["text"],
                                 relief=tk.FLAT,
                                 bd=0,
                                 pady=10,
                                 command=self.save)
        self.save_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        self.cancel_btn = tk.Button(button_frame, text="Cancel", 
                                   font=("Arial", 14), 
                                   bg=COLORS["secondary"], 
                                   fg=COLORS["text"],
                                   relief=tk.FLAT,
                                   bd=0,
                                   pady=10,
                                   command=self.cancel)
        self.cancel_btn.pack(side=tk.RIGHT)
    
    def save(self):
        try:
            name = self.name_var.get().strip()
            price = float(self.price_var.get())
            quantity = int(self.quantity_var.get())
            category = self.category_var.get().strip()
            
            if not name:
                messagebox.showerror("Error", "Product name is required")
                return
            
            if price < 0:
                messagebox.showerror("Error", "Price cannot be negative")
                return
            
            if quantity < 0:
                messagebox.showerror("Error", "Quantity cannot be negative")
                return
            
            self.result = {
                "name": name,
                "price": price,
                "quantity": quantity,
                "category": category
            }
            
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for price and quantity")
    
    def cancel(self):
        self.dialog.destroy()

# ----------------- Main Entry Point ----------------- #

if __name__ == "__main__":
    root = tk.Tk()
    app = NetflixLoginApp(root)
    root.mainloop()