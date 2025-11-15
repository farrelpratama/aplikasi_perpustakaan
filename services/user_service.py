# services/user_service.py
from services.db_client import db
from models.user import User
from typing import Optional, List
import bcrypt
from datetime import datetime

class UserService:
    """Service untuk handle semua operasi terkait User"""

    @staticmethod
    def register(full_name: str, email: str, password: str, role: str = 'user') -> Optional[User]:
        """Register user baru"""
    
        try:
            # Validasi input
            if not full_name or not email or not password:
                print("Error: Semua field harus diisi")
                return None
    
            # Cek username sudah ada atau belum
            existing = db.table('users').select('*').eq('full_name', full_name).execute()
            if existing.data:
                print(f"Error: Username '{full_name}' sudah digunakan")
                return None
            
            # Cek email sudah ada atau belum
            existing_email = db.table('users').select('*').eq('email', email).execute()
            if existing_email.data:
                print(f"Error: Email '{email}' sudah digunakan")
                return None
            
            # Hash password
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            # Insert ke database
            response = db.table('users').insert({
                'full_name': full_name,
                'email': email,
                'password_hash': password_hash,
                'role': role
            }).execute()
            
            if response.data:
                data = response.data[0]
                print(f"✅ User '{full_name}' berhasil didaftarkan")
                return User(
                    id=data['id'],
                    full_name=data['full_name'],
                    email=data['email'],
                    is_admin=(data.get('role') == 'admin'),
                    created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                )
            return None
            
        except Exception as e:
            print(f"❌ Error saat register: {e}")
            return None
    
    @staticmethod
    def login(email: str, password: str) -> Optional[User]:
        """Login user"""
        try:
            # Validasi input
            if not email or not password:
                print("Error: Email dan password harus diisi")
                return None
            
            # Get user dari database
            response = db.table('users').select('*').eq('email', email).execute()
            
            if not response.data:
                print(f"Error: Email '{email}' tidak ditemukan")
                return None
            
            user_data = response.data[0]
            
            # Verify password
            if bcrypt.checkpw(password.encode('utf-8'), user_data['password_hash'].encode('utf-8')):
                print(f"✅ Login berhasil: {user_data['full_name']}")
                return User(
                    id=user_data['id'],
                    full_name=user_data['full_name'],
                    email=user_data['email'],
                    is_admin=(user_data.get('role') == 'admin'),
                    created_at=datetime.fromisoformat(user_data['created_at'].replace('Z', '+00:00'))
                )
            else:
                print("Error: Password salah")
                return None
            
        except Exception as e:
            print(f"❌ Error saat login: {e}")
            return None
    
    @staticmethod
    def get_all_users() -> List[User]:
        """Get semua user (untuk admin)"""
        try:
            response = db.table('users').select('*').order('created_at', desc=False).execute()
            
            users = []
            for data in response.data:
                users.append(User(
                    id=data['id'],
                    full_name=data['full_name'],
                    email=data['email'],
                    is_admin=(data.get('role') == 'admin'),
                    created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                ))
            
            print(f"✅ Berhasil load {len(users)} users")
            return users
            
        except Exception as e:
            print(f"❌ Error saat get users: {e}")
            return []
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """Get user berdasarkan ID"""
        try:
            response = db.table('users').select('*').eq('id', user_id).execute()
            
            if response.data:
                data = response.data[0]
                return User(
                    id=data['id'],
                    full_name=data['full_name'],
                    email=data['email'],
                    is_admin=(data.get('role') == 'admin'),
                    created_at=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
                )
            return None
            
        except Exception as e:
            print(f"❌ Error saat get user: {e}")
            return None
    
    @staticmethod
    def update_user(user_id: str, full_name: str = None, email: str = None, 
                   password: str = None, role: str = None) -> bool:
        """Update data user"""
        try:
            update_data = {}
            
            if full_name :
                update_data['full_name'] = full_name
            if email:
                update_data['email'] = email
            if password:
                password_hash = bcrypt.hashpw(
                    password.encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                update_data['password_hash'] = password_hash
            if role:
                update_data['role'] = role
            
            if not update_data:
                print("Error: Tidak ada data yang diupdate")
                return False
            
            response = db.table('users').update(update_data).eq('id', user_id).execute()
            
            if response.data:
                print(f"✅ User berhasil diupdate")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error saat update: {e}")
            return False
    
    @staticmethod
    def delete_user(user_id: str) -> bool:
        """Hapus user"""
        try:
            response = db.table('users').delete().eq('id', user_id).execute()
            
            if response.data:
                print(f"✅ User berhasil dihapus")
                return True
            return False
            
        except Exception as e:
            print(f"❌ Error saat delete: {e}")
            return False