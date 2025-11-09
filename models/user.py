class User:
    def __init__(self, id: str, email: str, full_name: str = None, is_admin: bool = False):
        """
        Representasi objek pengguna (user atau admin).
        """
        self.id = id
        self.email = email
        self.full_name = full_name
        self.is_admin = is_admin

    def __repr__(self):
        role = "Admin" if self.is_admin else "User"
        return f"<User {self.full_name or self.email} ({role})>"

    def to_dict(self):
        """
        Mengembalikan representasi dictionary dari objek User.
        """
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "is_admin": self.is_admin
        }