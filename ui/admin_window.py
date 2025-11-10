import tkinter as tk
from tkinter import ttk, messagebox
from ui.base_window import BaseWindow
from models.book import Book
from models.loan import Loan

class AdminWindow(BaseWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.root.title("Admin Dashboard")
        self.root.geometry("1000x700")

        tk.Label(self.root, text="ADMIN DASHBOARD", font=("Times New Roman", 18, "bold")).pack(pady=10)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.tab_buku(notebook)
        self.tab_pinjam(notebook)
        self.tab_terlambat(notebook)

        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

    def tab_buku(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Kelola Buku")

        # Form tambah
        form = tk.Frame(frame)
        form.pack(pady=10)
        tk.Label(form, text="Judul:").grid(row=0, column=0)
        self.e_judul = tk.Entry(form, width=30)
        self.e_judul.grid(row=0, column=1, padx=5)

        tk.Label(form, text="Penulis:").grid(row=1, column=0)
        self.e_penulis = tk.Entry(form, width=30)
        self.e_penulis.grid(row=1, column=1, padx=5)

        tk.Label(form, text="Tahun:").grid(row=2, column=0)
        self.e_tahun = tk.Entry(form, width=10)
        self.e_tahun.grid(row=2, column=1, padx=5, sticky="w")

        tk.Label(form, text="Stok:").grid(row=3, column=0)
        self.e_stok = tk.Entry(form, width=10)
        self.e_stok.grid(row=3, column=1, padx=5, sticky="w")

        tk.Button(form, text="Tambah Buku", bg="#2196F3", fg="white",
                  command=self.tambah_buku).grid(row=4, column=1, pady=10, sticky="e")

        # Tabel buku
        cols = ("ID", "Judul", "Penulis", "Tahun", "Stok")
        self.tree_buku = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            self.tree_buku.heading(c, text=c)
            self.tree_buku.column(c, width=150)
        self.tree_buku.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_buku.bind("<Double-1>", self.edit_buku)

        self.refresh_buku()

    def tambah_buku(self):
        try:
            Book.add(self.e_judul.get(), self.e_penulis.get(), int(self.e_tahun.get()), int(self.e_stok.get()))
            messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")
            self.clear_form_buku()
            self.refresh_buku()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_buku(self):
        for i in self.tree_buku.get_children():
            self.tree_buku.delete(i)
        for b in Book.get_all():
            self.tree_buku.insert("", "end", values=(b["id"], b["title"], b["author"], b["year"], b["stock"]))

    def clear_form_buku(self):
        self.e_judul.delete(0, "end")
        self.e_penulis.delete(0, "end")
        self.e_tahun.delete(0, "end")
        self.e_stok.delete(0, "end")

    def edit_buku(self, event):
        item = self.tree_buku.selection()[0]
        book_id = self.tree_buku.item(item, "values")[0]
        # Bisa ditambah fitur edit & hapus di sini kalau mau

    def tab_pinjam(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Konfirmasi Peminjaman")

        cols = ("ID Loan", "User", "Buku", "Status", "Tenggat")
        self.tree_pinjam = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            self.tree_pinjam.heading(c, text=c)
            self.tree_pinjam.column(c, width=160)
        self.tree_pinjam.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_pinjam.bind("<Double-1>", self.konfirmasi_pinjam)

        self.refresh_pinjam()

    def refresh_pinjam(self):
        for i in self.tree_pinjam.get_children():
            self.tree_pinjam.delete(i)
        loans = Loan.get_all_with_details()
        for l in loans:
            buku = f"{l['books']['title']} - {l['books']['author']}"
            self.tree_pinjam.insert("", "end", values=(l["id"], l["users"]["username"], buku, l["status"], l["due_date"]))

    def konfirmasi_pinjam(self, event):
        item = self.tree_pinjam.selection()[0]
        loan_id = self.tree_pinjam.item(item, "values")[0]
        status = self.tree_pinjam.item(item, "values")[3]
        if status == "pending":
            Loan.confirm(loan_id)
            messagebox.showinfo("Sukses", "Peminjaman dikonfirmasi!")
            self.refresh_pinjam()

    def tab_terlambat(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Terlambat")

        cols = ("User", "Buku", "Tenggat")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=200)
        tree.pack(fill="both", expand=True, padx=20, pady=10)

        for l in Loan.get_overdue():
            tree.insert("", "end", values=(l["users"]["username"], l["books"]["title"], l["due_date"]))

    def logout(self):
        self.root.destroy()
        from ui.login_window import LoginWindow
        LoginWindow().run()