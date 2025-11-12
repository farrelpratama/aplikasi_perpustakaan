class Book:
    def __init__(self, book_id: str, title: str, author: str, isbn: str, total_count: int, available_count: int, created_at: str):
        self.id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_count = total_count
        self.available = available_count
        self.created_at = created_at

    def __repr__(self):
        status = "Available" if self.available else "Not Available"
        return f"<Book {self.title} by {self.author} ({status})>"

    def to_dict(self):
        """
        Mengembalikan representasi dictionary dari objek Book.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "total_count": self.total_count,
            "available_count": self.available_count,
            "created_at": self.created_at
        }
