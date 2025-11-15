import tkinter as tk
from tkinter import messagebox
from ui.base_window import BaseWindow
from ui.register_window import RegisterWindow
from services.user_service import UserService

class LoginWindow(BaseWindow):
    def __init__(self, user_svc, on_login, title, size):
        super().__init__()
        self.user_svc = user_svc
        self.on_login = on_login
        
        self.root.title("Login - Sistem Perpustakaan")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Judul
        tk.Label(self.root, text="SISTEM PERPUSTAKAAN", font=("Times New Roman", 16, "bold")).pack(pady=20)

        # email
        tk.Label(self.root, text="Email").pack(pady=5)
        self.entry_email = tk.Entry(self.root, width=30, font=("Times New Roman", 11))
        self.entry_email.pack(pady=5)
        self.entry_email.focus()
        # Password
        tk.Label(self.root, text="Password").pack(pady=5)
        self.entry_pass = tk.Entry(self.root, width=30, font=("Times New Roman", 11), show="*")
        self.entry_pass.pack(pady=5)

        # Tombol
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="LOGIN", width=12, bg="#4CAF50", fg="white",
                  command=self.login).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="DAFTAR", width=12, bg="#2196F3", fg="white",
                  command=self.open_register).grid(row=0, column=1, padx=10)

        # Bind Enter
        self.root.bind("<Return>", lambda e: self.login())

    def login(self):
        email = self.entry_email.get().strip()
        password = self.entry_pass.get()

        if not email or not password:
            messagebox.showerror("Error", "Email dan password harus diisi!")
            return

        user = UserService.login(email, password)
        if user:
            self.root.destroy()  # tutup login
            if user.is_admin:
                from ui.admin_window import AdminWindow
                AdminWindow(user).run()
            else:
                from ui.user_window import UserWindow
                UserWindow(user).run()
        else:
            messagebox.showerror("Gagal", "Email atau password salah!")

    def open_register(self):
        RegisterWindow(self.root)  # buka sebagai Toplevel