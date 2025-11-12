from services.user_service import UserService
from services.book_service import BookService
from services.loan_service import LoanService
from ui.login_window import LoginWindow
from ui.user_window import UserWindow
from ui.admin_window import AdminWindow

def main():
    user_svc = UserService()
    book_svc = BookService()
    loan_svc = LoanService()

    def on_login(user):
        if user.is_admin:
            win = AdminWindow(user, book_svc, loan_svc, title="Admin - Book Loan", size="900x700")
            win.run()
        else:
            win = UserWindow(user, book_svc, loan_svc, title="User - Book Loan", size="900x700")
            win.run()

    login = LoginWindow(user_svc, on_login, title="Login - Book Loan", size="400x200")
    login.run()

if __name__ == "__main__":
    main()
