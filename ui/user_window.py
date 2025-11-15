import tkinter as tk
from tkinter import ttk, messagebox
from ui.base_window import BaseWindow
from models.book import Book
from models.loan import Loan

class UserWindow(BaseWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.root.title(f"User - {user.full_name}")
        self.root.geometry("900x600")

        tk.Label(self.root, text=f"Selamat Datang, {user.full_name}!", 
                 font=("Arial", 16)).pack(pady=10)

        # Tabel Buku
        columns = ("ID", "Judul", "Penulis", "Tahun", "Stok")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Form pinjam
        frame = tk.Frame(self.root)
        frame.pack(pady=10)
        tk.Label(frame, text="ID Buku:").pack(side="left", padx=5)
        self.entry_id = tk.Entry(frame, width=10)
        self.entry_id.pack(side="left", padx=5)
        tk.Button(frame, text="Ajukan Pinjam", bg="#4CAF50", fg="white",
                  command=self.pinjam).pack(side="left", padx=5)

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

        self.refresh_books()

    def refresh_books(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        books = Book.get_all()
        for b in books:
            self.tree.insert("", "end", values=(b["id"], b["title"], b["author"], b["year"], b["stock"]))

    def pinjam(self):
        try:
            book_id = int(self.entry_id.get())
            result = Loan.request(self.user.id, book_id)
            if result:
                messagebox.showinfo("Sukses", "Pengajuan berhasil! Menunggu konfirmasi admin.")
                self.entry_id.delete(0, "end")
                self.refresh_books()
            else:
                messagebox.showerror("Gagal", "Stok habis atau buku tidak ditemukan!")
        except ValueError:
            messagebox.showerror("Error", "Masukkan ID buku yang valid!")

    def logout(self):
        self.root.destroy()
        from ui.login_window import LoginWindow
        LoginWindow().run()