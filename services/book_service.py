# services/book_service.py
from services.db_client import ClientDB as db
from models.book import Book
from typing import Optional, List
from datetime import datetime

class BookService:
    """Service untuk handle semua operasi terkait Book"""
    
    @staticmethod
    def create_book(title: str, author: str, isbn: str, 
                   total_count: int,) -> Optional[Book]:
        """Tambah buku baru (untuk admin)"""
        try:
            # Validasi input
            if not title or not author or not isbn:
                print("Error: Title, author, ISBN, dan category harus diisi")
                return None
            
            if total_count < 0:
                print("Error: Stock tidak boleh negatif")
                return None
            
            # Cek ISBN sudah ada atau belum
            existing = db.table('books').select('*').eq('isbn', isbn).execute()
            if existing.data:
                print(f"Error: Buku dengan ISBN '{isbn}' sudah ada")
                return None
            
            # Insert ke database
            response = db.table('books').insert({
                'title': title,
                'author': author,
                'isbn': isbn,
                'total_count': total_count,
                'available_count': total_count,
                "created_at": datetime.utcnow().isoformat()
            }).execute()
            
            if response.data:
                data = response.data[0]
                print(f"✅ Buku '{title}' berhasil ditambahkan")
                return Book(
                    id=data['id'],
                    title=data['title'],
                    author=data['author'],
                    isbn=data['isbn'],
                    total_count=data['total_count'],
                    available_count=data['available_count'],
                    created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                )
            return None
            
        except Exception as e:
            print(f"❌ Error saat create book: {e}")
            return None
    
    @staticmethod
    def get_all_books() -> List[Book]:
        """Get semua buku"""
        try:
            response = db.table('books').select('*').order('title').execute()
            
            books = []
            for data in response.data:
                books.append(Book(
                    id=data['id'],
                    title=data['title'],
                    author=data['author'],
                    isbn=data['isbn'],
                    total_count=data['total_count'],
                    available_count=data['available_count'],
                    created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                ))
            
            print(f"✅ Berhasil load {len(books)} buku")
            return books
            
        except Exception as e:
            print(f"❌ Error saat get books: {e}")
            return []
    
    @staticmethod
    def get_available_books() -> List[Book]:
        """Get buku yang tersedia (stock > 0)"""
        try:
            response = db.table('books').select('*').gt('available_count', 0).order('title').execute()
            
            books = []
            for data in response.data:
                books.append(Book(
                    id=data['id'],
                    title=data['title'],
                    author=data['author'],
                    total_count=data['total_count'],
                    available_count=data['available_count'],
                    created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                ))
            
            print(f"✅ Berhasil load {len(books)} buku tersedia")
            return books
            
        except Exception as e:
            print(f"❌ Error saat get available books: {e}")
            return []
    
    @staticmethod
    def get_book_by_id(book_id: str) -> Optional[Book]:
        """Get buku berdasarkan ID"""
        try:
            response = db.table('books').select('*').eq('id', book_id).execute()
            
            if response.data:
                data = response.data[0]
                return Book(
                    id=data['id'],
                    title=data['title'],
                    author=data['author'],
                    isbn=data['isbn'],
                    total_count=data['total_count'],
                    available_count=data['available_count'],
                    created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                )
            return None
            
        except Exception as e:
            print(f"❌ Error saat get book: {e}")
            return None
    
    @staticmethod
    def search_books(keyword: str) -> List[Book]:
        """Search buku berdasarkan keyword (title atau author)"""
        try:
            # Search by title
            response_title = db.table('books').select('*').ilike('title', f'%{keyword}%').execute()
            
            # Search by author
            response_author = db.table('books').select('*').ilike('author', f'%{keyword}%').execute()
            
            # Combine results (hapus duplikat)
            book_ids = set()
            books = []
            
            for data in response_title.data + response_author.data:
                if data['id'] not in book_ids:
                    book_ids.add(data['id'])
                    books.append(Book(
                        id=data['id'],
                        title=data['title'],
                        author=data['author'],
                        isbn=data['isbn'],
                        total_count=data['total_count'],
                        available_count=data['available_count'],
                        created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                    ))
            
            print(f"✅ Ditemukan {len(books)} buku dengan keyword '{keyword}'")
            return books
            
        except Exception as e:
            print(f"❌ Error saat search books: {e}")
            return []
    
    @staticmethod
    def update_book(book_id: str, title: str = None, author: str = None, 
                   isbn: str = None, total_count: int = None, available_count: int = None) -> bool:
        """Update data buku (untuk admin)"""
        try:
            update_data = {}
            
            if title:
                update_data['title'] = title
            if author:
                update_data['author'] = author
            if isbn:
                update_data['isbn'] = isbn
            if total_count is not None:
                update_data['total_count'] = total_count
            if available_count is not None:
                update_data['available_count'] = available_count
            
            if not update_data:
                print("Error: Tidak ada data yang diupdate")
                return False
            
            response = db.table('books').update(update_data).eq('id', book_id).execute()
            
            if response.data:
                print(f"✅ Buku berhasil diupdate")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error saat update book: {e}")
            return False
    
    @staticmethod
    def delete_book(book_id: str) -> bool:
        """Hapus buku (untuk admin)"""
        try:
            response = db.table('books').delete().eq('id', book_id).execute()
            
            if response.data:
                print(f"✅ Buku berhasil dihapus")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error saat delete book: {e}")
            return False
    
    @staticmethod
    def update_stock(book_id: str, change: int) -> bool:
        """
        Update stock buku (increment/decrement)
        change: positif = tambah, negatif = kurang
        """
        try:
            # Get current book
            book = BookService.get_book_by_id(book_id)
            if not book:
                print("Error: Buku tidak ditemukan")
                return False
            
            new_stock = book.stock + change
            
            if new_stock < 0:
                print("Error: Stock tidak boleh negatif")
                return False
            
            response = db.table('books').update({
                'total_count': new_stock
            }).eq('id', book_id).execute()
            
            if response.data:
                print(f"✅ Stock diupdate: {book.total_count} → {new_stock}")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error saat update stock: {e}")
            return False
    
    @staticmethod
    def get_books_by_category(category: str) -> List[Book]:
        """Get buku berdasarkan kategori"""
        try:
            response = db.table('books').select('*').eq('category', category).order('title', desc=False).execute()
            
            books = []
            for data in response.data:
                books.append(Book(
                    id=data['id'],
                    title=data['title'],
                    author=data['author'],
                    isbn=data['isbn'],
                    category=data['category'],
                    total_count=data['total_count'],
                    available_count=data['available_count'],
                    description=data.get('description'),
                    created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                ))
            
            print(f"✅ Ditemukan {len(books)} buku dalam kategori '{category}'")
            return books
            
        except Exception as e:
            print(f"❌ Error saat get books by category: {e}")
            return []