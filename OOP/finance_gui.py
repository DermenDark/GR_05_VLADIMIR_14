import tkinter as tk
from tkinter import simpledialog, messagebox
from finance_core import CoreApp
from window.role_window import ClientGUI, ManagerGUI, AdminGUI


class FinanceGUI(tk.Tk):
    """Главное окно, которое выбирает GUI в зависимости от роли"""
    def __init__(self):
        super().__init__()
        self.title("Управление финансовой системой")
        self.geometry("1500x800")

        self.core = CoreApp()
        self.store = self.core.store
        self.auth = self.core.auth
        self.bank_service = self.core.bank_service
        self.tx_service = self.core.tx_service
        self.enterprise_service = self.core.enterprise_service
        self.admin_service = self.core.admin_service

        self.current_user = None
        self.active_gui = None  # ссылка на ClientGUI/ManagerGUI/AdminGUI

        self.login_frame = None
        self.dashboard_frame = None

        self.build_login()

    def build_login(self):
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
            self.dashboard_frame = None
        if self.login_frame:
            self.login_frame.destroy()

        self.login_frame = tk.Frame(self, padx=20, pady=20)
        self.login_frame.pack(fill="both", expand=True)

        tk.Label(self.login_frame, text="Login", font=("Arial", 18)).pack(pady=8)
        tk.Label(self.login_frame, text="Логин:").pack(anchor="w")
        self.login_entry = tk.Entry(self.login_frame)
        self.login_entry.pack(fill="x")

        tk.Label(self.login_frame, text="Пароль:").pack(anchor="w", pady=(10,0))
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(fill="x")

        btn_frame = tk.Frame(self.login_frame)
        btn_frame.pack(pady=12)

        tk.Button(btn_frame, text="Войти", command=self.on_login).grid(row=0, column=0, padx=6)
        tk.Button(btn_frame, text="Зарегистрироваться (клиент)", command=self.on_register).grid(row=0, column=1, padx=6)
        tk.Button(btn_frame, text="Выход", command=self.quit).grid(row=0, column=2, padx=6)

        hints = (
            "Демо-аккаунты: manager/mgrpass, admin/adminpass, alice/alice123 (client confirmed), bob/bob123 (unconfirmed)"
        )
        tk.Label(self.login_frame, text=hints, fg="gray").pack(pady=8)

    def on_register(self):
        login = simpledialog.askstring("Регистрация", "Логин:", parent=self)
        if not login:
            return
        full_name = simpledialog.askstring("Регистрация", "ФИО:", parent=self)
        if not full_name:
            return
        pwd = simpledialog.askstring("Регистрация", "Пароль (мин 4):", parent=self, show="*")
        if not pwd:
            return
        try:
            user = self.auth.register_client(login=login, full_name=full_name, password=pwd)
            messagebox.showinfo("Регистрация", f"Зарегистрировано. ID: {user.id}\nОжидает подтверждения менеджера.")
        except Exception as e:
            messagebox.showerror("Ошибка регистрации", str(e))

    def on_login(self):
        login = self.login_entry.get().strip()
        pwd = self.password_entry.get().strip()
        if not login or not pwd:
            messagebox.showwarning("Вход", "Введите логин и пароль.")
            return

        user = self.auth.authenticate(login, pwd)
        if user is None:
            messagebox.showerror("Вход не выполнен", "Неверный логин/пароль или клиент не подтверждён менеджером.")
            return

        self.current_user = user
        messagebox.showinfo("Вход", f"Привет, {user.full_name} ({user.role})")

        # Убираем экран логина
        if self.login_frame:
            try:
                self.login_frame.destroy()
            except Exception:
                pass
            self.login_frame = None

        # Перейти к созданию dashboard'а
        self.on_login_success()

    def on_login_success(self):
        """Вызывается после успешного входа — создаёт dashboard и нужный role-GUI."""
        if self.dashboard_frame:
            try:
                self.dashboard_frame.destroy()
            except Exception:
                pass
            self.dashboard_frame = None

        if self.active_gui:
            try:
                self.active_gui.destroy()
            except Exception:
                pass
            self.active_gui = None

        self.dashboard_frame = tk.Frame(self, padx=10, pady=10)
        self.dashboard_frame.pack(fill="both", expand=True)

        # Добавим кнопку выхода из аккаунта
        top_frame = tk.Frame(self.dashboard_frame)
        top_frame.pack(fill="x", pady=(0,6))
        tk.Button(top_frame, text="Выход из аккаунта", command=self.logout).pack(side="right")

        role = self.current_user.role
        if role == "client":
            self.active_gui = ClientGUI(self.dashboard_frame, self.store, self.auth,
                                        self.bank_service, self.tx_service, self.enterprise_service,
                                        self.current_user)
        elif role == "manager":
            self.active_gui = ManagerGUI(self.dashboard_frame, self.store,
                                        self.enterprise_service, self.bank_service,
                                        self.current_user)
        elif role == "admin":
            self.active_gui = AdminGUI(self.dashboard_frame, self.store,
                                    self.admin_service, self.current_user)
        else:
            tk.Label(self.dashboard_frame, text="Неизвестная роль").pack()

    def logout(self):
        """Корректно разлогиниться и вернуть экран логина."""
        self.current_user = None
        if self.active_gui:
            try:
                self.active_gui.destroy()
            except Exception:
                pass
            self.active_gui = None

        # Уничтожаем dashboard
        if self.dashboard_frame:
            try:
                self.dashboard_frame.destroy()
            except Exception:
                pass
            self.dashboard_frame = None

        self.build_login()

def main():
    root = FinanceGUI()
    root.mainloop()

if __name__ == "__main__":
    main()