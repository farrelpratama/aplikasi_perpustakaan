from services.db_client import db
from datetime import datetime, timedelta, date
from models.loan import Loan

class LoanService:

    def request_loan(self, user_id, book_id, days=7, note=None):
        # check availability
        book_q = self.db.table("books").select("*").eq("id", book_id).single().execute()
        book = book_q.data
        if not book:
            raise Exception("Buku tidak ditemukan")
        if book["available_count"] <= 0:
            raise Exception("Buku tidak tersedia")
        due = (date.today() + timedelta(days=days)).isoformat()
        res = self.db.table("loans").insert({
            "user_id": user_id,
            "book_id": book_id,
            "due_date": due,
            "status": "requested",
            "loan_date": None,  # akan diisi saat approve
            "returned_date": None
        }).execute()
        return Loan(
            loan_id=res.data[0]["id"],
            user_id=res.data[0]["user_id"],
            book_id=res.data[0]["book_id"],
            approved_at=res.data[0].get("loan_date"),
            returned_at=res.data[0].get("returned_date"),
            due_date=res.data[0]["due_date"],
            status=res.data[0]["status"]
        )

    def approve_loan(self, loan_id, admin_id=None):
        # set status approved, decrease book available_count, set loan_date
        loan_q = self.db.table("loans").select("*").eq("id", loan_id).single().execute()
        if not loan_q.data:
            raise Exception("Loan tidak ditemukan")
        loan = loan_q.data
        if loan["status"] != "requested":
            raise Exception("Loan bukan dalam status 'requested'")
        # decrement book available_count
        book_q = self.db.table("books").select("*").eq("id", loan["book_id"]).single().execute()
        book = book_q.data
        if book["available_count"] <= 0:
            raise Exception("Buku tidak tersedia")
        self.db.table("books").update({"available_count": book["available_count"] - 1}).eq("id", book["id"]).execute()
        res = self.db.table("loans").update({
            "status": "approved",
            "loan_date": datetime.utcnow().isoformat()  # ganti approved_at jadi loan_date
        }).eq("id", loan_id).execute()
        return Loan(
            loan_id=res.data[0]["id"],
            user_id=res.data[0]["user_id"],
            book_id=res.data[0]["book_id"],
            approved_at=res.data[0].get("loan_date"),
            returned_at=res.data[0].get("returned_date"),
            due_date=res.data[0]["due_date"],
            status=res.data[0]["status"]
        )

    def return_loan(self, loan_id):
        loan_q = self.db.table("loans").select("*").eq("id", loan_id).single().execute()
        loan = loan_q.data
        if not loan:
            raise Exception("Loan tidak ditemukan")
        if loan["status"] not in ["approved", "overdue"]:
            raise Exception("Loan tidak dapat dikembalikan")
        # increment available_count
        book_q = self.db.table("books").select("*").eq("id", loan["book_id"]).single().execute()
        book = book_q.data
        self.db.table("books").update({"available_count": book["available_count"] + 1}).eq("id", book["id"]).execute()
        res = self.db.table("loans").update({
            "status": "returned",
            "returned_date": datetime.utcnow().isoformat()  # ganti returned_at jadi returned_date
        }).eq("id", loan_id).execute()
        return Loan(
            loan_id=res.data[0]["id"],
            user_id=res.data[0]["user_id"],
            book_id=res.data[0]["book_id"],
            approved_at=res.data[0].get("loan_date"),
            returned_at=res.data[0].get("returned_date"),
            due_date=res.data[0]["due_date"],
            status=res.data[0]["status"]
        )

    def list_loans_by_user(self, user_id):
        res = self.db.table("loans").select("*").eq("user_id", user_id).execute()
        return [Loan(
            loan_id=r["id"],
            user_id=r["user_id"],
            book_id=r["book_id"],
            approved_at=r.get("loan_date"),
            returned_at=r.get("returned_date"),
            due_date=r["due_date"],
            status=r["status"]
        ) for r in res.data]

    def list_all_loans(self):
        res = self.db.table("loans").select("*").execute()
        return [Loan(
            loan_id=r["id"],
            user_id=r["user_id"],
            book_id=r["book_id"],
            approved_at=r.get("loan_date"),
            returned_at=r.get("returned_date"),
            due_date=r["due_date"],
            status=r["status"]
        ) for r in res.data]

    def mark_overdue(self):
        # find loans where due_date < today and status approved
        today = date.today().isoformat()
        res = self.db.table("loans").select("*").lt("due_date", today).eq("status", "approved").execute()
        for r in res.data:
            self.db.table("loans").update({"status": "overdue"}).eq("id", r["id"]).execute()
        return True