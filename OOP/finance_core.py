from __future__ import annotations
import uuid
import datetime
import getpass
import json
import os
from typing import List, Optional, Dict, Any

# Utilities / Validation
def gen_id(prefix: str = "") -> str:
    return prefix + str(uuid.uuid4())[:8]

def now_iso() -> str:
    return datetime.datetime.utcnow().isoformat()

def input_nonempty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Поле не может быть пустым. Повторите ввод.")

def input_positive_float(prompt: str) -> float:
    while True:
        s = input(prompt).replace(",", ".").strip()
        try:
            v = float(s)
            if v > 0:
                return v
            print("Введите число > 0.")
        except:
            print("Невалидный ввод. Введите число.")

# Domain models
class LogEntry:
    def __init__(self, actor_id: str, action: str, payload: dict, timestamp: Optional[str] = None):
        self.id = gen_id("log_")
        self.actor_id = actor_id
        self.action = action
        self.payload = payload
        self.timestamp = timestamp or now_iso()

    def to_dict(self):
        return {"id": self.id, "actor_id": self.actor_id, "action": self.action, "payload": self.payload, "timestamp": self.timestamp}

class Transaction:
    def __init__(self, src_type: str, src_id: str, dst_type: str, 
                 dst_id: str, amount: float, actor_id: str):
        self.id = gen_id("tx_")
        self.src_type = src_type  
        self.src_id = src_id
        self.dst_type = dst_type
        self.dst_id = dst_id
        self.amount = amount
        self.timestamp = now_iso()
        self.actor_id = actor_id

    def to_dict(self):
        return {
            "id": self.id,
            "src_type": self.src_type,
            "src_id": self.src_id,
            "dst_type": self.dst_type,
            "dst_id": self.dst_id,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "actor_id": self.actor_id,
        }

class Account:
    def __init__(self, bank_id: str, owner_id: str, 
                 balance: float = 0.0, blocked: bool = False):
        self.id = gen_id("acc_")
        self.bank_id = bank_id
        self.owner_id = owner_id
        self.balance = float(balance)
        self.blocked = blocked
        self.history: List[Transaction] = []

    def deposit(self, amount: float, tx: Transaction):
        if self.blocked:
            raise ValueError("Счет заблокирован.")
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0.")
        self.balance += amount
        self.history.append(tx)

    def withdraw(self, amount: float, tx: Transaction):
        if self.blocked:
            raise ValueError("Счет заблокирован.")
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0.")
        if self.balance < amount:
            raise ValueError("Недостаточно средств.")
        self.balance -= amount
        self.history.append(tx)

    def to_dict(self):
        return {"id": self.id, "bank_id": self.bank_id, 
                "owner_id": self.owner_id, "balance": self.balance, 
                "blocked": self.blocked}

class Deposit:
    def __init__(self, bank_id: str, owner_id: str, principal: float, 
                 rate_pct: float, term_months: int, blocked: bool = False):
        self.id = gen_id("dep_")
        self.bank_id = bank_id
        self.owner_id = owner_id
        self.principal = float(principal)
        self.rate_pct = float(rate_pct)
        self.term_months = int(term_months)
        self.blocked = blocked
        self.created_at = now_iso()
        self.history: List[Transaction] = []

    def accrue_month(self):
        # простая месячная капитализация
        monthly_rate = self.rate_pct / 100.0 / 12.0
        self.principal += self.principal * monthly_rate

    def to_dict(self):
        return {"id": self.id, "bank_id": self.bank_id,
                "owner_id": self.owner_id, "principal": self.principal, 
                "rate_pct": self.rate_pct, "term_months": self.term_months, "blocked": self.blocked}

class Bank:
    def __init__(self, name: str):
        self.id = gen_id("bank_")
        self.name = name
        self.accounts: Dict[str, Account] = {}
        self.deposits: Dict[str, Deposit] = {}

    def to_dict(self):
        return {"id": self.id, "name": self.name}

class Enterprise:
    def __init__(self, name: str, manager_id: Optional[str] = None, funds: float = 0.0):
        self.id = gen_id("ent_")
        self.name = name
        self.manager_id = manager_id 
        self.employees: List[str] = [] 
        self.funds = float(funds)
        self.payroll_requests: Dict[str, Dict[str, Any]] = {}  
    def to_dict(self):
        return {"id": self.id, "name": self.name, "funds": self.funds}

class User:
    def __init__(self, login: str, full_name: str, role: str, password: str):
        self.id = gen_id("usr_")
        self.login = login
        self.full_name = full_name
        self.role = role 
        self.password = password
        self.confirmed = role != "client"  

    def to_dict(self):
        return {"id": self.id, "login": self.login, "full_name": self.full_name, 
                "role": self.role, "confirmed": self.confirmed}

# Repositories / Managers (Single Responsibility)
class DataStore:
    """Хранит все сущности в памяти (для demo). Можно добавить сериализацию."""
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.banks: Dict[str, Bank] = {}
        self.enterprises: Dict[str, Enterprise] = {}
        self.logs: List[LogEntry] = []
        self.transactions: Dict[str, Transaction] = {}

        self.accounts_index: Dict[str, Account] = {}
        self.deposits_index: Dict[str, Deposit] = {}

    def save_log(self, entry: LogEntry):
        self.logs.append(entry)

    def save_tx(self, tx: Transaction):
        self.transactions[tx.id] = tx

    def dump_to_file(self, path="demo_state.json"):
        obj = {
            "users": {u_id: u.to_dict() for u_id, u in self.users.items()},
            "banks": {b_id: {"meta": bank.to_dict(),
                             "accounts": {acc.id: acc.to_dict() for acc in bank.accounts.values()},
                             "deposits": {dep.id: dep.to_dict() for dep in bank.deposits.values()}} 
                             for b_id, bank in self.banks.items()},
            "enterprises": {e_id: ent.to_dict() for e_id, ent in self.enterprises.items()},
            "logs": [l.to_dict() for l in self.logs],
            "transactions": {tx_id: tx.to_dict() for tx_id, tx in self.transactions.items()}
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
        print(f"State dumped to {path}")

# Services (Open/Closed, Single Responsibility)
class AuthService:
    def __init__(self, store: DataStore):
        self.store = store

    def register_client(self, login: str, full_name: str, password: str) -> User:
        # validation
        if any(u.login == login for u in self.store.users.values()):
            raise ValueError("Пользователь с таким логином уже существует.")
        if len(password) < 4:
            raise ValueError("Пароль должен быть не короче 4 символов.")
        user = User(login=login, full_name=full_name, role="client", password=password)
        user.confirmed = False
        self.store.users[user.id] = user
        self.store.save_log(LogEntry(actor_id=user.id, action="register_client", payload=user.to_dict()))
        return user

    def create_user(self, login: str, full_name: str, role: str, 
                    password: str, confirmed: bool = True) -> User:
        if any(u.login == login for u in self.store.users.values()):
            raise ValueError("Пользователь с таким логином уже существует.")
        user = User(login=login, full_name=full_name, role=role, password=password)
        user.confirmed = confirmed
        self.store.users[user.id] = user
        self.store.save_log(LogEntry(actor_id=user.id, action="create_user", payload=user.to_dict()))
        return user

    def authenticate(self, login: str, password: str) -> Optional[User]:
        for u in self.store.users.values():
            if u.login == login and u.password == password:
                if not u.confirmed and u.role == "client":
                    # client poshel naxer
                    return None
                return u
        return None

class BankService:
    def __init__(self, store: DataStore):
        self.store = store

    def create_bank(self, name: str) -> Bank:
        bank = Bank(name)
        self.store.banks[bank.id] = bank
        self.store.save_log(LogEntry(actor_id="system", action="create_bank", payload=bank.to_dict()))
        return bank

    def open_account(self, bank_id: str, owner_id: str, initial: float = 0.0) -> Account:
        if bank_id not in self.store.banks:
            raise ValueError("Нет такого банка.")
        acc = Account(bank_id=bank_id, owner_id=owner_id, balance=initial)
        bank = self.store.banks[bank_id]
        bank.accounts[acc.id] = acc
        self.store.accounts_index[acc.id] = acc
        self.store.save_log(LogEntry(actor_id=owner_id, action="open_account", payload=acc.to_dict()))
        return acc

    def close_account(self, account_id: str, actor_id: str):
        acc = self._get_account(account_id)
        if acc.balance != 0:
            raise ValueError("Счет должен быть пуст (баланс 0) для закрытия.")
        bank = self.store.banks[acc.bank_id]
        del bank.accounts[acc.id]
        del self.store.accounts_index[acc.id]
        self.store.save_log(LogEntry(actor_id=actor_id, action="close_account", payload={"account_id": account_id}))

    def get_account(self, account_id: str) -> Account:
        return self._get_account(account_id)

    def _get_account(self, account_id: str) -> Account:
        if account_id not in self.store.accounts_index:
            raise ValueError("Счет не найден.")
        return self.store.accounts_index[account_id]

    def create_deposit(self, bank_id: str, owner_id: str, principal: float, 
                       rate_pct: float, term_months: int) -> Deposit:
        if bank_id not in self.store.banks:
            raise ValueError("Нет такого банка.")
        dep = Deposit(bank_id=bank_id, owner_id=owner_id, principal=principal, 
                      rate_pct=rate_pct, term_months=term_months)
        bank = self.store.banks[bank_id]
        bank.deposits[dep.id] = dep
        self.store.deposits_index[dep.id] = dep
        self.store.save_log(LogEntry(actor_id=owner_id, action="create_deposit", payload=dep.to_dict()))
        return dep

    def close_deposit(self, deposit_id: str, actor_id: str):
        dep = self._get_deposit(deposit_id)
        bank = self.store.banks[dep.bank_id]
        del bank.deposits[dep.id]
        del self.store.deposits_index[dep.id]
        self.store.save_log(LogEntry(actor_id=actor_id, action="close_deposit", payload={"deposit_id": deposit_id}))

    def _get_deposit(self, deposit_id: str) -> Deposit:
        if deposit_id not in self.store.deposits_index:
            raise ValueError("Вклад не найден.")
        return self.store.deposits_index[deposit_id]

class TransactionService:
    def __init__(self, store: DataStore, bank_service: BankService):
        self.store = store
        self.bank_service = bank_service

    def transfer(self, src_type: str, src_id: str, dst_type: str, 
                 dst_id: str, amount: float, actor_id: str) -> Transaction:
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0.")
        src_obj = self._resolve_entity(src_type, src_id)
        dst_obj = self._resolve_entity(dst_type, dst_id)

        if hasattr(src_obj, "blocked") and src_obj.blocked:
            raise ValueError("Источник заблокирован.")
        if hasattr(dst_obj, "blocked") and dst_obj.blocked:
            raise ValueError("Назначение заблокировано.")

        tx = Transaction(src_type=src_type, src_id=src_id, dst_type=dst_type, 
                         dst_id=dst_id, amount=amount, actor_id=actor_id)

        if src_type == "account":
            acc = src_obj
            acc.withdraw(amount, tx)
        elif src_type == "deposit":
            dep = src_obj
            if dep.principal < amount:
                raise ValueError("Недостаточно на вкладе.")
            dep.principal -= amount
            dep.history.append(tx)
        elif src_type == "enterprise":
            ent = src_obj
            if ent.funds < amount:
                raise ValueError("У предприятия недостаточно средств.")
            ent.funds -= amount
        else:
            raise ValueError("Неподдерживаемый тип источника.")

        if dst_type == "account":
            dst_acc = dst_obj
            dst_acc.deposit(amount, tx)
        elif dst_type == "deposit":
            dst_dep = dst_obj
            dst_dep.principal += amount
            dst_dep.history.append(tx)
        elif dst_type == "enterprise":
            dst_ent = dst_obj
            dst_ent.funds += amount
        else:
            raise ValueError("Неподдерживаемый тип назначения.")

        self.store.save_tx(tx)
        self.store.save_log(LogEntry(actor_id=actor_id, action="transfer", payload=tx.to_dict()))
        return tx

    def _resolve_entity(self, typ: str, id_: str):
        if typ == "account":
            return self.bank_service.get_account(id_)
        if typ == "deposit":
            return self.bank_service._get_deposit(id_)
        if typ == "enterprise":
            if id_ not in self.store.enterprises:
                raise ValueError("Предприятие не найдено.")
            return self.store.enterprises[id_]
        raise ValueError("Неизвестный тип сущности.")

class EnterpriseService:
    def __init__(self, store: DataStore):
        self.store = store

    def create_enterprise(self, name: str, manager_id: Optional[str] = None, funds: float = 0.0) -> Enterprise:
        ent = Enterprise(name=name, manager_id=manager_id, funds=funds)
        self.store.enterprises[ent.id] = ent
        self.store.save_log(LogEntry(actor_id=manager_id or "system", action="create_enterprise", 
                                     payload=ent.to_dict()))
        return ent

    def list_available_for_client(self, client_id: str) -> List[Enterprise]:
        return [e for e in self.store.enterprises.values()]

    def submit_payroll_request(self, enterprise_id: str, client_id: str, amount: float) -> str:
        ent = self.store.enterprises[enterprise_id]
        req_id = gen_id("pr_")
        ent.payroll_requests[req_id] = {"client_id": client_id, "amount": amount, 
                                        "approved": False, "approved_by": None}
        self.store.save_log(LogEntry(actor_id=client_id, action="submit_payroll_request", 
                                     payload={"enterprise_id": enterprise_id, "req_id": req_id, "amount": amount} ))
        return req_id

    def approve_payroll_request(self, enterprise_id: str, req_id: str, manager_id: str):
        ent = self.store.enterprises[enterprise_id]
        if req_id not in ent.payroll_requests:
            raise ValueError("Нет такого запроса.")
        ent.payroll_requests[req_id]["approved"] = True
        ent.payroll_requests[req_id]["approved_by"] = manager_id
        self.store.save_log(LogEntry(actor_id=manager_id, action="approve_payroll_request", 
                                     payload={"enterprise_id": enterprise_id, "req_id": req_id}))

    def add_employee(self, enterprise_id: str, client_id: str, manager_id: str):
        ent = self.store.enterprises[enterprise_id]
        if client_id in ent.employees:
            raise ValueError("Клиент уже сотрудник.")
        ent.employees.append(client_id)
        self.store.save_log(LogEntry(actor_id=manager_id, action="add_employee", 
                                     payload={"enterprise_id": enterprise_id, "client_id": client_id}))

    def remove_employee(self, enterprise_id: str, client_id: str, manager_id: str):
        ent = self.store.enterprises[enterprise_id]
        if client_id not in ent.employees:
            raise ValueError("Клиент не является сотрудником.")
        ent.employees.remove(client_id)
        self.store.save_log(LogEntry(actor_id=manager_id, action="remove_employee", 
                                     payload={"enterprise_id": enterprise_id, "client_id": client_id}))

# Admin: view logs and undo
class AdminService:
    def __init__(self, store: DataStore, bank_service: BankService, tx_service: TransactionService):
        self.store = store
        self.bank_service = bank_service
        self.tx_service = tx_service

    def view_logs(self) -> List[LogEntry]:
        return list(self.store.logs)

    def undo_transaction(self, tx_id: str, actor_id: str):
        if tx_id not in self.store.transactions:
            raise ValueError("Транзакция не найдена.")
        tx = self.store.transactions[tx_id]
        rev = Transaction(src_type=tx.dst_type, src_id=tx.dst_id, dst_type=tx.src_type, 
                          dst_id=tx.src_id, amount=tx.amount, actor_id=actor_id)

        self.tx_service.transfer(rev.src_type, rev.src_id, rev.dst_type, rev.dst_id, rev.amount, actor_id)
        self.store.save_log(LogEntry(actor_id=actor_id, action="undo_transaction", 
                                     payload={"original_tx": tx.to_dict(), "undo_tx": rev.to_dict()}))
        return rev

# Application / CLI (UI)
class CLIApp:
    def __init__(self):
        self.store = DataStore()
        self.auth = AuthService(self.store)
        self.bank_service = BankService(self.store)
        self.enterprise_service = EnterpriseService(self.store)
        self.tx_service = TransactionService(self.store, self.bank_service)
        self.admin_service = AdminService(self.store, self.bank_service, self.tx_service)
        self.current_user: Optional[User] = None
        self.seed_demo_data()

    def seed_demo_data(self):

        mgr = self.auth.create_user(login="manager", full_name="Менеджер Demo", role="manager", 
                                    password="mgrpass", confirmed=True)
        admin = self.auth.create_user(login="admin", full_name="Админ Demo", role="admin", 
                                      password="adminpass", confirmed=True)
        
        b1 = self.bank_service.create_bank("DemoBank A")
        b2 = self.bank_service.create_bank("Local Credit")

        c1 = self.auth.register_client(login="alice", full_name="Alice Client", password="alice123")
        c2 = self.auth.register_client(login="bob", full_name="Bob Client", password="bob123")

        c1.confirmed = True

        self.store.save_log(LogEntry(actor_id=mgr.id, action="confirm_client", payload={"client_id": c1.id}))
        acc_a = self.bank_service.open_account(b1.id, c1.id, initial=1000.0)
        acc_b = self.bank_service.open_account(b2.id, c2.id, initial=50.0)

        dep_a = self.bank_service.create_deposit(b1.id, c1.id, principal=500.0, rate_pct=5.0, term_months=12)
        ent = self.enterprise_service.create_enterprise("ООО Рога и Копыта", manager_id=mgr.id, funds=10000.0)
        self.store.save_log(LogEntry(actor_id="system", action="seeded_demo", 
                                     payload={"banks": [b1.to_dict(), b2.to_dict()], "users": [c1.to_dict(), c2.to_dict()]}))

    def run(self):
        print("=== Система: Управление финансовой системой (консольная демонстрация) ===")
        while True:
            if not self.current_user:
                print("\n1) Войти\n2) Зарегистрироваться (клиент)\n3) Выход")
                choice = input("Выберите: ").strip()
                if choice == "1":
                    self.menu_login()
                elif choice == "2":
                    self.menu_register()
                elif choice == "3":
                    print("Выход. До свидания.")
                    break
                else:
                    print("Неправильный выбор.")
            else:
                role = self.current_user.role
                if role == "client":
                    self.menu_client()
                elif role == "manager":
                    self.menu_manager()
                elif role == "admin":
                    self.menu_admin()
                else:
                    print("Неизвестная роль. Выход.")
                    break

    # def menu_login(self):
    #     login = input_nonempty("Логин: ")
    #     password = getpass.getpass("Пароль: ")
    #     user = self.auth.authenticate(login, password)
    #     if user is None:
    #         print("Аутентификация не удалась (возможно, нужно подтверждение менеджера или неверный пароль).")
    #         return
    #     self.current_user = user
    #     print(f"Вход выполнен. Привет, {user.full_name} ({user.role}).")

    # def menu_register(self):
    #     print("=== Регистрация клиента ===")
    #     login = input_nonempty("Логин: ")
    #     full_name = input_nonempty("ФИО: ")
    #     password = getpass.getpass("Пароль (мин 4): ")
    #     try:
    #         user = self.auth.register_client(login=login, full_name=full_name, password=password)
    #         print("Зарегистрировано. Ожидает подтверждения менеджера. Когда менеджер подтвердит, вы сможете войти.")
    #         print(f"Ваш идентификатор: {user.id}")
    #     except Exception as e:
    #         print("Ошибка регистрации:", str(e))

    # # Client menu
    # def menu_client(self):
    #     user = self.current_user
    #     assert user and user.role == "client"
    #     print("\n--- Клиентское меню ---")
    #     print("1) Просмотреть банки")
    #     print("2) Открыть счет")
    #     print("3) Закрыть счет")
    #     print("4) Перевести средства")
    #     print("5) Просмотр истории счетов")
    #     print("6) Создать вклад")
    #     print("7) Закрыть вклад")
    #     print("8) Перевести на вклад / со вклада")
    #     print("9) Посмотреть предприятия")
    #     print("10) Подать заявку на зарплатный проект")
    #     print("11) Получить зарплату (после одобрения менеджером)")
    #     print("0) Выйти (Logout)")
    #     c = input("Выберите: ").strip()
    #     try:
    #         if c == "1":
    #             self.client_view_banks()
    #         elif c == "2":
    #             self.client_open_account()
    #         elif c == "3":
    #             self.client_close_account()
    #         elif c == "4":
    #             self.client_transfer()
    #         elif c == "5":
    #             self.client_view_history()
    #         elif c == "6":
    #             self.client_create_deposit()
    #         elif c == "7":
    #             self.client_close_deposit()
    #         elif c == "8":
    #             self.client_transfer_to_from_deposit()
    #         elif c == "9":
    #             self.client_view_enterprises()
    #         elif c == "10":
    #             self.client_submit_payroll()
    #         elif c == "11":
    #             self.client_get_salary()
    #         elif c == "0":
    #             print("Выход.")
    #             self.current_user = None
    #         else:
    #             print("Неверный выбор.")
    #     except Exception as e:
    #         print("Ошибка:", e)

    # def client_view_banks(self):
    #     print("Банки в системе:")
    #     for b in self.store.banks.values():
    #         print(f"- {b.name} (id={b.id})")

    # def client_open_account(self):
    #     print("Открытие счета. Выберите банк (id):")
    #     for b in self.store.banks.values():
    #         print(f"{b.id}: {b.name}")
    #     bid = input_nonempty("bank_id: ")
    #     initial = input_positive_float("Начальный депозит: ")
    #     acc = self.bank_service.open_account(bid, self.current_user.id, initial=initial)
    #     print("Счет открыт:", acc.id)

    # def client_close_account(self):
    #     print("Ваши счета:")
    #     my_accs = [acc for acc in self.store.accounts_index.values() if acc.owner_id == self.current_user.id]
    #     if not my_accs:
    #         print("У вас нет счетов.")
    #         return
    #     for acc in my_accs:
    #         print(f"{acc.id}: Bank {self.store.banks[acc.bank_id].name} Balance={acc.balance} Blocked={acc.blocked}")
    #     aid = input_nonempty("Введите id счета для закрытия: ")
    #     self.bank_service.close_account(aid, actor_id=self.current_user.id)
    #     print("Счет закрыт.")

    # def client_transfer(self):
    #     print("Перевод средств.")
    #     # list user's accounts and deposits
    #     my_accounts = [a for a in self.store.accounts_index.values() if a.owner_id == self.current_user.id]
    #     my_deposits = [d for d in self.store.deposits_index.values() if d.owner_id == self.current_user.id]
    #     print("Ваши счета:")
    #     for a in my_accounts:
    #         print(f"{a.id}: Balance={a.balance} Bank={self.store.banks[a.bank_id].name} Blocked={a.blocked}")
    #     print("Ваши вклады:")
    #     for d in my_deposits:
    #         print(f"{d.id}: Principal={d.principal} Bank={self.store.banks[d.bank_id].name} Blocked={d.blocked}")
    #     src_type = input_nonempty("Источник (account/deposit): ")
    #     src_id = input_nonempty("id источника: ")
    #     dst_type = input_nonempty("Назначение (account/deposit/enterprise): ")
    #     dst_id = input_nonempty("id назначения: ")
    #     amount = input_positive_float("Сумма: ")
    #     tx = self.tx_service.transfer(src_type, src_id, dst_type, dst_id, amount, actor_id=self.current_user.id)
    #     print("Перевод выполнен. tx_id:", tx.id)

    # def client_view_history(self):
    #     print("История по вашим счетам и вкладам:")
    #     for acc in [a for a in self.store.accounts_index.values() if a.owner_id == self.current_user.id]:
    #         print(f"\nСчет {acc.id} (Bank {self.store.banks[acc.bank_id].name}):")
    #         for tx in acc.history:
    #             print(f"  {tx.timestamp}: {tx.id} {tx.src_type}:{tx.src_id} -> {tx.dst_type}:{tx.dst_id} amount={tx.amount}")
    #     for dep in [d for d in self.store.deposits_index.values() if d.owner_id == self.current_user.id]:
    #         print(f"\nВклад {dep.id} (Bank {self.store.banks[dep.bank_id].name}):")
    #         for tx in dep.history:
    #             print(f"  {tx.timestamp}: {tx.id} {tx.src_type}:{tx.src_id} -> {tx.dst_type}:{tx.dst_id} amount={tx.amount}")

    # def client_create_deposit(self):
    #     print("Создание вклада.")
    #     for b in self.store.banks.values():
    #         print(f"{b.id}: {b.name}")
    #     bid = input_nonempty("bank_id: ")
    #     principal = input_positive_float("Сумма вклада: ")
    #     rate = input_positive_float("Годовой процент (например 5.0): ")
    #     term = int(input_nonempty("Срок в месяцах (целое число): "))
    #     dep = self.bank_service.create_deposit(bid, self.current_user.id, principal, rate, term)
    #     print("Вклад создан:", dep.id)

    # def client_close_deposit(self):
    #     print("Ваши вклады:")
    #     my_deps = [d for d in self.store.deposits_index.values() if d.owner_id == self.current_user.id]
    #     for d in my_deps:
    #         print(f"{d.id}: principal={d.principal} bank={self.store.banks[d.bank_id].name} blocked={d.blocked}")
    #     did = input_nonempty("id вклада для закрытия: ")
    #     self.bank_service.close_deposit(did, actor_id=self.current_user.id)
    #     print("Вклад закрыт.")

    # def client_transfer_to_from_deposit(self):
    #     print("Перевод между счетом и вкладом.")
    #     src_type = input_nonempty("Источник (account/deposit): ")
    #     src_id = input_nonempty("id источника: ")
    #     dst_type = input_nonempty("Назначение (account/deposit): ")
    #     dst_id = input_nonempty("id назначения: ")
    #     amount = input_positive_float("Сумма: ")
    #     tx = self.tx_service.transfer(src_type, src_id, dst_type, dst_id, amount, actor_id=self.current_user.id)
    #     print("Операция выполнена. tx_id:", tx.id)

    # def client_view_enterprises(self):
    #     print("Доступные предприятия (для подачи на зарплатный проект):")
    #     for e in self.enterprise_service.list_available_for_client(self.current_user.id):
    #         print(f"{e.id}: {e.name} Funds={e.funds}")

    # def client_submit_payroll(self):
    #     self.client_view_enterprises()
    #     eid = input_nonempty("Введите id предприятия для подачи заявки: ")
    #     amount = input_positive_float("Желаемая сумма зарплаты: ")
    #     req_id = self.enterprise_service.submit_payroll_request(eid, self.current_user.id, amount)
    #     print("Заявка отправлена. req_id:", req_id)

    # def client_get_salary(self):
    #     print("Список предприятий с одобренными заявками на вас:")
    #     for e in self.store.enterprises.values():
    #         for rid, req in e.payroll_requests.items():
    #             if req["client_id"] == self.current_user.id and req.get("approved"):
    #                 print(f"{e.id}:{e.name} request {rid} amount {req['amount']}")
    #     eid = input_nonempty("Введите id предприятия (откуда получать): ")
    #     rid = input_nonempty("Введите id заявки (req_id): ")
    #     ent = self.store.enterprises[eid]
    #     if rid not in ent.payroll_requests:
    #         print("Нет такой заявки.")
    #         return
    #     req = ent.payroll_requests[rid]
    #     if not req.get("approved"):
    #         print("Заявка ещё не одобрена менеджером.")
    #         return
    #     amount = float(req["amount"])

    #     my_accounts = [a for a in self.store.accounts_index.values() if a.owner_id == self.current_user.id]
    #     if not my_accounts:
    #         print("У вас нет счёта для получения зарплаты. Сначала откройте счёт.")
    #         return
    #     print("Выберите счёт для зачисления:")
    #     for a in my_accounts:
    #         print(f"{a.id}: Balance={a.balance} Bank={self.store.banks[a.bank_id].name}")
    #     aid = input_nonempty("account id: ")

    #     tx = self.tx_service.transfer("enterprise", eid, "account", aid, amount, actor_id=self.current_user.id)
    #     print("Зарплата получена. tx_id:", tx.id)

    #     del ent.payroll_requests[rid]
    #     self.store.save_log(LogEntry(actor_id=self.current_user.id, action="receive_salary", 
    #                                  payload={"enterprise_id": eid, "account_id": aid, "amount": amount}))

    # # Manager menu
    # def menu_manager(self):
    #     user = self.current_user
    #     assert user and user.role == "manager"
    #     print("\n--- Менеджерское меню ---")
    #     print("1) Подтвердить регистрацию клиента")
    #     print("2) Просмотреть предприятия и сотрудников")
    #     print("3) Добавить клиента в предприятие (сделать сотрудником)")
    #     print("4) Удалить клиента из предприятия")
    #     print("5) Подтвердить заявку на зарплатный проект")
    #     print("6) Блокировка/разблокировка счетов и вкладов клиента")
    #     print("7) Просмотр истории движений счетов клиентов")
    #     print("0) Выйти (Logout)")
    #     c = input("Выберите: ").strip()
    #     try:
    #         if c == "1":
    #             self.manager_confirm_client()
    #         elif c == "2":
    #             self.manager_view_enterprises()
    #         elif c == "3":
    #             self.manager_add_employee()
    #         elif c == "4":
    #             self.manager_remove_employee()
    #         elif c == "5":
    #             self.manager_approve_payroll()
    #         elif c == "6":
    #             self.manager_block_unblock()
    #         elif c == "7":
    #             self.manager_view_client_history()
    #         elif c == "0":
    #             print("Выход.")
    #             self.current_user = None
    #         else:
    #             print("Неверный выбор.")
    #     except Exception as e:
    #         print("Ошибка:", e)

    # def manager_confirm_client(self):
    #     # list unconfirmed clients
    #     unconfirmed = [u for u in self.store.users.values() if u.role == "client" and not u.confirmed]
    #     if not unconfirmed:
    #         print("Нет клиентов, ожидающих подтверждения.")
    #         return
    #     for u in unconfirmed:
    #         print(f"{u.id}: {u.full_name} (login={u.login})")
    #     uid = input_nonempty("Введите id клиента для подтверждения: ")
    #     if uid not in self.store.users:
    #         print("Не найден.")
    #         return
    #     user = self.store.users[uid]
    #     user.confirmed = True
    #     self.store.save_log(LogEntry(actor_id=self.current_user.id, action="confirm_client", 
    #                                  payload={"client_id": uid}))
    #     print("Клиент подтвержден.")

    # def manager_view_enterprises(self):
    #     for e in self.store.enterprises.values():
    #         print(f"{e.id}: {e.name} Funds={e.funds} Manager={e.manager_id}")
    #         print(" Employees:")
    #         for emp in e.employees:
    #             u = self.store.users.get(emp)
    #             print(f"   - {emp}: {u.full_name if u else 'unknown'}")

    # def manager_add_employee(self):
    #     self.manager_view_enterprises()
    #     eid = input_nonempty("enterprise id: ")
    #     print("Клиенты:")
    #     for u in self.store.users.values():
    #         if u.role == "client":
    #             print(f"{u.id}: {u.full_name} confirmed={u.confirmed}")
    #     cid = input_nonempty("client id для добавления: ")
    #     self.enterprise_service.add_employee(eid, cid, manager_id=self.current_user.id)
    #     print("Клиент добавлен в предприятие.")

    # def manager_remove_employee(self):
    #     self.manager_view_enterprises()
    #     eid = input_nonempty("enterprise id: ")
    #     cid = input_nonempty("client id для удаления: ")
    #     self.enterprise_service.remove_employee(eid, cid, manager_id=self.current_user.id)
    #     print("Клиент удалён из предприятия.")

    # def manager_approve_payroll(self):
    #     print("Заявки на зарплатный проект:")
    #     for e in self.store.enterprises.values():
    #         for rid, req in e.payroll_requests.items():
    #             print(f"Enterprise {e.id}:{e.name} request {rid} client {req['client_id']} amount {req['amount']} approved={req.get('approved')}")
    #     eid = input_nonempty("enterprise id: ")
    #     rid = input_nonempty("req_id: ")
    #     self.enterprise_service.approve_payroll_request(eid, rid, manager_id=self.current_user.id)
    #     print("Заявка одобрена менеджером. Клиент может получить зарплату (через интерфейс клиента).")

    # def manager_block_unblock(self):
    #     print("1) Заблокировать/разблокировать счет")
    #     print("2) Заблокировать/разблокировать вклад")
    #     c = input("Выберите: ").strip()
    #     if c == "1":
    #         for a in self.store.accounts_index.values():
    #             print(f"{a.id}: owner={a.owner_id} Balance={a.balance} blocked={a.blocked}")
    #         aid = input_nonempty("account id: ")
    #         a = self.bank_service.get_account(aid)
    #         a.blocked = not a.blocked
    #         self.store.save_log(LogEntry(actor_id=self.current_user.id, action="toggle_block_account", 
    #                                      payload={"account_id": aid, "new_state": a.blocked}))
    #         print("Новый статус:", a.blocked)
    #     elif c == "2":
    #         for d in self.store.deposits_index.values():
    #             print(f"{d.id}: owner={d.owner_id} principal={d.principal} blocked={d.blocked}")
    #         did = input_nonempty("deposit id: ")
    #         d = self.bank_service._get_deposit(did)
    #         d.blocked = not d.blocked
    #         self.store.save_log(LogEntry(actor_id=self.current_user.id, action="toggle_block_deposit", 
    #                                      payload={"deposit_id": did, "new_state": d.blocked}))
    #         print("Новый статус:", d.blocked)
    #     else:
    #         print("Неверный выбор.")

    # def manager_view_client_history(self):
    #     cid = input_nonempty("Введите id клиента для просмотра истории: ")
    #     print(f"История для клиента {cid}:")
    #     for acc in [a for a in self.store.accounts_index.values() if a.owner_id == cid]:
    #         print(f"\nСчет {acc.id}:")
    #         for tx in acc.history:
    #             print(f"  {tx.timestamp}: {tx.id} {tx.src_type}:{tx.src_id} -> {tx.dst_type}:{tx.dst_id} amount={tx.amount}")

    # # Admin menu
    # def menu_admin(self):
    #     user = self.current_user
    #     assert user and user.role == "admin"
    #     print("\n--- Админское меню ---")
    #     print("1) Просмотр всех логов")
    #     print("2) Отмена (undo) транзакции")
    #     print("3) Сброс состояния в файл (dump)")
    #     print("0) Выйти (Logout)")
    #     c = input("Выберите: ").strip()
    #     try:
    #         if c == "1":
    #             self.admin_view_logs()
    #         elif c == "2":
    #             self.admin_undo_tx()
    #         elif c == "3":
    #             self.store.dump_to_file()
    #         elif c == "0":
    #             print("Выход.")
    #             self.current_user = None
    #         else:
    #             print("Неверный выбор.")
    #     except Exception as e:
    #         print("Ошибка:", e)

    # def admin_view_logs(self):
    #     logs = self.admin_service.view_logs()
    #     for l in logs:
    #         print(f"{l.timestamp} | {l.actor_id} | {l.action} | {json.dumps(l.payload, ensure_ascii=False)}")

    # def admin_undo_tx(self):
    #     txid = input_nonempty("Введите tx_id для отмены: ")
    #     rev = self.admin_service.undo_transaction(txid, actor_id=self.current_user.id)
    #     print("Создан обратный перевод (undo). undo_tx_id:", rev.id)

    # def admin_service(self) -> AdminService:
    #     return self.admin_service_ref() if hasattr(self, "admin_service_ref") else self.admin_service


# def main():
#     root = CLIApp()
#     root.run()

# if __name__ == "__main__":
#     main()

# менедж:     логин manager, пароль mgrpass
# админ:        логин admin, пароль adminpass
# клиент        (одобрен): логин alice, пароль alice123 (есть счёт и вклад)
# клиент        (неподтверждён): логин bob, пароль bob123 (нужно подтверждение менеджера)