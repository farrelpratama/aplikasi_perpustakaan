from datetime import date
class Loan:
      def __init__(self, loan_id: str, user_id: str, book_id: str, loan_date: str, return_date: str or None, status: str):
          self.id = loan_id
          self.user_id = user_id
          self.book_id = book_id
          self.loan_date = loan_date
          self.return_date = return_date
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
              "loan_date": self.loan_date,
              "return_date": self.return_date,
              "status": self.status
          }
  