class Loan:
      def __init__(self, loan_id: str, user_id: str, book_id: str, approved_at: str, returned_at: str, due_date: str, status: str):
          self.id = loan_id
          self.user_id = user_id
          self.book_id = book_id
          self.loan_date = approved_at
          self.returned_date = returned_at
          self.due_date = due_date
          self.status = status

      def __repr__(self):
          return f"<Loan ID: {self.id}, User: {self.user_id}, Book: {self.book_id}, Status: {self.status}>"

      def to_dict(self):
          """
          Mengembalikan representasi dictionary dari objek Loan.
          """
          return {
              "id": self.id,
              "user_id": self.user_id,
              "book_id": self.book_id,
              "approved_at": self.loan_date,
              "returned_date": self.returned_date,
              "due_date": self.due_date,
              "status": self.status
          }
  