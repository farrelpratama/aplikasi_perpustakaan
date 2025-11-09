class Book:
    def __init__(self, book_id: str, title: str, author: str, available: bool):
        self.id = book_id
        self.title = title
        self.author = author
        self.available = available

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
            "available": self.available
        }
