from supabase import create_client
from config.config import supabase_key, supabase_url

class ClientDB:
    def __init__(self):
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL and Key must be set in environment variables.")
        self.client = create_client(supabase_url, supabase_key)
    
    def table(self, table_name):
        return self.client.table(table_name)

db = ClientDB()