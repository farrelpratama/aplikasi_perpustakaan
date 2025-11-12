import tkinter as tk
from tkinter import messagebox
from services.user_service import UserService as User

class RegisterWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Registrasi Akun Baru")
        self.top.geometry("380x400")
        self.top.transient(parent)
        self.top.grab_set()  # fokus ke window ini

        tk.Label(self.top, text="BUAT AKUN BARU", font=("Times New Roman", 16, "bold")).pack(pady=20)

        tk.Label(self.top, text="Username").pack(pady=5)
        self.e_user = tk.Entry(self.top, width=30, font=("Times New Roman", 11))
        self.e_user.pack(pady=5)

        tk.Label(self.top, text="Password").pack(pady=5)
        self.e_pass = tk.Entry(self.top, width=30, font=("Times New Roman", 11), show="*")
        self.e_pass.pack(pady=5)

        tk.Label(self.top, text="Ulangi Password").pack(pady=5)
        self.e_pass2 = tk.Entry(self.top, width=30, font=("Times New Roman", 11), show="*")
        self.e_pass2.pack(pady=5)

        tk.Button(self.top, text="DAFTAR", width=15, bg="#FF9800", fg="white",
                  command=self.register).pack(pady=20)

    def register(self):
        username = self.e_user.get().strip()
        pass1 = self.e_pass.get()
        pass2 = self.e_pass2.get()

        if not all([username, pass1, pass2]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return
        if pass1 != pass2:
            messagebox.showerror("Error", "Password tidak sama!")
            return
        if len(pass1) < 6:
            messagebox.showerror("Error", "Password minimal 6 karakter!")
            return

        user = User.register(username, pass1)
        if user:
            messagebox.showinfo("Sukses", f"Akun {username} berhasil dibuat!\nSilakan login.")
            self.top.destroy()
        else:
            messagebox.showerror("Gagal", "Username sudah digunakan!")