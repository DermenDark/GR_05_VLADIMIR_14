# window/role_window.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from data.DataStore import LogEntry
from window.helper_window import TransferDialog, CreateDepositDialog
import json

class RoleGUIBase:
    """Базовый GUI-класс для всех ролей."""
    def __init__(self, parent, store, current_user):
        self.parent = parent
        self.store = store
        self.current_user = current_user

        self.main_frame = None

    def build_main_frame(self):
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True)
        return self.main_frame

    def destroy(self):
        try:
            if self.main_frame:
                self.main_frame.destroy()
                self.main_frame = None
        except Exception:
            pass

    def ask_string(self, title, prompt):
        return simpledialog.askstring(title, prompt, parent=self.parent)

    def ask_float(self, title, prompt):
        return simpledialog.askfloat(title, prompt, parent=self.parent)

    def show_info(self, title, text):
        messagebox.showinfo(title, text, parent=self.parent)

    def show_error(self, title, text):
        messagebox.showerror(title, text, parent=self.parent)

    def show_warning(self, title, text):
        messagebox.showwarning(title, text, parent=self.parent)

    def wait_window(self, widget):
        self.parent.wait_window(widget)

class ClientGUI(RoleGUIBase):
    """Интерфейс и методы для клиента"""
    def __init__(self, parent, store, auth, bank_service, tx_service, enterprise_service, current_user):
        super().__init__(parent, store, current_user)
        self.auth = auth
        self.bank_service = bank_service
        self.tx_service = tx_service
        self.enterprise_service = enterprise_service

        self.accounts_tree = None
        self.deposits_tree = None
        self.banks_list = None
        self.build_client_ui()

    def build_client_ui(self):
        frame = self.build_main_frame()

        left = tk.Frame(frame)
        left.pack(side="left", fill="both", expand=True, padx=6)

        mid = tk.Frame(frame)
        mid.pack(side="left", fill="both", expand=True, padx=6)

        right = tk.Frame(frame)
        right.pack(side="left", fill="both", expand=True, padx=6)

        # Banks list + open account
        tk.Label(left, text="Банки:").pack(anchor="w")
        self.banks_list = tk.Listbox(left, height=6)
        self.banks_list.pack(fill="x")
        for b in self.store.banks.values():
            self.banks_list.insert("end", f"{b.id} — {b.name}")
        tk.Button(left, text="Открыть счет в выбранном банке", command=self.client_open_account).pack(pady=6, anchor="w")
        tk.Button(left, text="Закрыть выбранный счет", command=self.client_close_account).pack(pady=2, anchor="w")

        # Accounts
        tk.Label(mid, text="Ваши счета:").pack(anchor="w")
        self.accounts_tree = ttk.Treeview(mid, columns=("bank", "balance", "blocked"), show="headings", height=8)
        self.accounts_tree.heading("bank", text="Банк")
        self.accounts_tree.heading("balance", text="Баланс")
        self.accounts_tree.heading("blocked", text="Заблокирован")
        self.accounts_tree.pack(fill="both", expand=True)
        tk.Button(mid, text="Обновить счета", command=self.refresh_client_accounts).pack(pady=4)
        tk.Button(mid, text="Перевести (счет/вклад)", command=self.client_transfer_dialog).pack(pady=4)
        tk.Button(mid, text="История движений (в новом окне)", command=self.client_view_history_window).pack(pady=4)

        # Deposits area
        tk.Label(right, text="Ваши вклады:").pack(anchor="w")
        self.deposits_tree = ttk.Treeview(right, columns=("bank", "principal", "rate", "term", "blocked"),
                                          show="headings", height=8)
        self.deposits_tree.heading("bank", text="Банк")
        self.deposits_tree.heading("principal", text="Сумма")
        self.deposits_tree.heading("rate", text="% годовых")
        self.deposits_tree.heading("term", text="Срок (мес)")
        self.deposits_tree.heading("blocked", text="Заблокирован")
        self.deposits_tree.pack(fill="both", expand=True)
        tk.Button(right, text="Обновить вклады", command=self.refresh_client_deposits).pack(pady=4)
        tk.Button(right, text="Создать вклад", command=self.client_create_deposit).pack(pady=2)
        tk.Button(right, text="Закрыть выбранный вклад", command=self.client_close_deposit).pack(pady=2)
        tk.Button(right, text="Перевести между счётом и вкладом", command=self.client_transfer_dialog).pack(pady=2)
        tk.Button(right, text="Накопить (1 месяц) на выбранном вкладе", command=self.client_accrue_deposit).pack(pady=2)

        # Enterprises / payroll
        bottom = tk.Frame(frame)
        bottom.pack(fill="x", pady=(8, 0))
        tk.Button(bottom, text="Посмотреть предприятия и подать заявку на зарплатный проект",
                  command=self.client_view_enterprises_window).pack(side="left", padx=6)
        tk.Button(bottom, text="Получить зарплату (если есть одобренная заявка)",
                  command=self.client_receive_salary_dialog).pack(side="left", padx=6)

        # начальная загрузка данных
        self.refresh_client_accounts()
        self.refresh_client_deposits()

    def refresh_client_accounts(self):
        if not self.accounts_tree:
            return
        for i in self.accounts_tree.get_children():
            self.accounts_tree.delete(i)
        for a in self.store.accounts_index.values():
            if a.owner_id == self.current_user.id:
                bank_name = self.store.banks[a.bank_id].name
                self.accounts_tree.insert("", "end", iid=a.id, values=(bank_name, f"{a.balance:.2f}", str(a.blocked)))

    def refresh_client_deposits(self):
        if not self.deposits_tree:
            return
        for i in self.deposits_tree.get_children():
            self.deposits_tree.delete(i)
        for d in self.store.deposits_index.values():
            if d.owner_id == self.current_user.id:
                bank_name = self.store.banks[d.bank_id].name
                self.deposits_tree.insert("", "end", iid=d.id,
                                          values=(bank_name, f"{d.principal:.2f}", f"{d.rate_pct:.2f}",
                                                  str(d.term_months), str(d.blocked)))

    def client_open_account(self):
        sel = self.banks_list.curselection()
        if not sel:
            self.show_warning("Открытие счета", "Выберите банк.")
            return
        line = self.banks_list.get(sel[0])
        bank_id = line.split(" — ")[0]
        initial = simpledialog.askfloat("Открытие счета", "Начальный депозит:", parent=self.parent)
        if initial is None:
            return
        try:
            acc = self.bank_service.open_account(bank_id, self.current_user.id, initial=initial)
            self.show_info("Открытие счета", f"Счет открыт: {acc.id}")
            self.refresh_client_accounts()
        except Exception as e:
            self.show_error("Ошибка", str(e))

    def client_close_account(self):
        sel = self.accounts_tree.selection()
        if not sel:
            self.show_warning("Закрытие счета", "Выберите счёт.")
            return
        aid = sel[0]
        try:
            self.bank_service.close_account(aid, actor_id=self.current_user.id)
            self.show_info("Закрытие", "Счёт закрыт.")
            self.refresh_client_accounts()
        except Exception as e:
            self.show_error("Ошибка", str(e))

    def client_create_deposit(self):
        banks = list(self.store.banks.values())
        bank_choices = {b.id: b.name for b in banks}
        d = CreateDepositDialog(self.parent, bank_choices)
        self.wait_window(d)
        if not getattr(d, "result", None):
            return
        bank_id, principal, rate, term = d.result
        try:
            dep = self.bank_service.create_deposit(bank_id, self.current_user.id, principal, rate, term)
            self.show_info("Вклад", f"Вклад создан: {dep.id}")
            self.refresh_client_deposits()
        except Exception as e:
            self.show_error("Ошибка", str(e))

    def client_close_deposit(self):
        sel = self.deposits_tree.selection()
        if not sel:
            self.show_warning("Закрытие вклада", "Выберите вклад.")
            return
        did = sel[0]
        try:
            self.bank_service.close_deposit(did, actor_id=self.current_user.id)
            self.show_info("Вклад", "Вклад закрыт.")
            self.refresh_client_deposits()
        except Exception as e:
            self.show_error("Ошибка", str(e))

    def client_accrue_deposit(self):
        sel = self.deposits_tree.selection()
        if not sel:
            self.show_warning("Накопление", "Выберите вклад.")
            return
        did = sel[0]
        try:
            dep = self.bank_service._get_deposit(did)
            dep.accrue_month()
            self.store.save_log(LogEntry(actor_id=self.current_user.id, action="accrue_deposit",
                                        payload={"deposit_id": did, "new_principal": dep.principal}))
            self.show_info("Накопление", f"Капитализация выполнена. Новый принципал: {dep.principal:.2f}")
            self.refresh_client_deposits()
        except Exception as e:
            self.show_error("Ошибка", str(e))

    def client_transfer_dialog(self):
        dlg = TransferDialog(self.parent, self.store, self.tx_service, self.current_user)
        self.wait_window(dlg)
        self.refresh_client_accounts()
        self.refresh_client_deposits()

    def client_view_history_window(self):
        w = tk.Toplevel(self.parent)
        w.title("История клиента")
        txt = tk.Text(w, width=120, height=40)
        txt.pack(fill="both", expand=True)
        for acc in [a for a in self.store.accounts_index.values() if a.owner_id == self.current_user.id]:
            txt.insert("end", f"\nСчет {acc.id} ({self.store.banks[acc.bank_id].name}):\n")
            for tx in acc.history:
                txt.insert("end", f"  {tx.timestamp} {tx.id} {tx.src_type}:{tx.src_id} -> "
                                  f"{tx.dst_type}:{tx.dst_id} amount={tx.amount}\n")
        for dep in [d for d in self.store.deposits_index.values() if d.owner_id == self.current_user.id]:
            txt.insert("end", f"\nВклад {dep.id} ({self.store.banks[dep.bank_id].name}):\n")
            for tx in dep.history:
                txt.insert("end", f"  {tx.timestamp} {tx.id} {tx.src_type}:{tx.src_id} -> "
                                  f"{tx.dst_type}:{tx.dst_id} amount={tx.amount}\n")
        txt.config(state="disabled")

    def client_view_enterprises_window(self):
        w = tk.Toplevel(self.parent)
        w.title("Предприятия")
        tree = ttk.Treeview(w, columns=("funds", "manager"), show="headings")
        tree.heading("funds", text="Funds")
        tree.heading("manager", text="Manager ID")
        tree.pack(fill="both", expand=True)
        for e in self.store.enterprises.values():
            tree.insert("", "end", iid=e.id, values=(f"{e.funds:.2f}", str(e.manager_id)))
        tk.Button(w, text="Подать заявку на зарплатный проект",
                  command=lambda: self.client_submit_payroll_dialog(w, tree)).pack(pady=6)

    def client_submit_payroll_dialog(self, parent, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Заявка", "Выберите предприятие.", parent=parent)
            return
        eid = sel[0]
        amount = simpledialog.askfloat("Заявка", "Желаемая сумма:", parent=parent)
        if amount is None:
            return
        try:
            req_id = self.enterprise_service.submit_payroll_request(eid, self.current_user.id, amount)
            messagebox.showinfo("Заявка", f"Заявка отправлена. req_id: {req_id}", parent=parent)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e), parent=parent)

    def client_receive_salary_dialog(self):
        approved = []
        for e in self.store.enterprises.values():
            for rid, req in e.payroll_requests.items():
                if req["client_id"] == self.current_user.id and req.get("approved"):
                    approved.append((e, rid, req))
        if not approved:
            self.show_info("Зарплата", "Нет одобренных заявок.")
            return

        w = tk.Toplevel(self.parent)
        w.title("Получение зарплаты")
        tree = ttk.Treeview(w, columns=("enterprise", "amount"), show="headings")
        tree.heading("enterprise", text="Enterprise")
        tree.heading("amount", text="Amount")
        tree.pack(fill="both", expand=True)
        for e, rid, req in approved:
            tree.insert("", "end", iid=rid, values=(f"{e.name} ({e.id})", f"{req['amount']:.2f}"))

        def do_receive():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Получение", "Выберите заявку.", parent=w)
                return
            rid = sel[0]

            ent_id = None
            amount = None
            for e, r, req in approved:
                if r == rid:
                    ent_id = e.id
                    amount = req["amount"]
                    break
            if ent_id is None:
                messagebox.showerror("Ошибка", "Не найдено.", parent=w)
                return

            my_accs = [a for a in self.store.accounts_index.values() if a.owner_id == self.current_user.id]
            if not my_accs:
                messagebox.showwarning("Получение", "У вас нет счетов. Сначала откройте счет.", parent=w)
                return

            sel_acc = simpledialog.askstring("Выбор счета",
                                            f"Введите id счета для получения зарплаты:\nДоступные: {', '.join(a.id for a in my_accs)}",
                                            parent=w)
            if not sel_acc:
                return
            try:
                tx = self.tx_service.transfer("enterprise", ent_id, "account", sel_acc, float(amount),
                                              actor_id=self.current_user.id)
                messagebox.showinfo("Успех", f"Зарплата получена. tx_id: {tx.id}", parent=self.parent)

                ent = self.store.enterprises[ent_id]
                if rid in ent.payroll_requests:
                    del ent.payroll_requests[rid]
                self.store.save_log(LogEntry(actor_id=self.current_user.id, action="receive_salary",
                                            payload={"enterprise_id": ent_id, "account_id": sel_acc, "amount": amount}))
                self.refresh_client_accounts()
                w.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e), parent=w)

class ManagerGUI(RoleGUIBase):
    """Интерфейс и методы для менеджера"""
    def __init__(self, parent, store, enterprise_service, bank_service, current_user):
        super().__init__(parent, store, current_user)
        self.enterprise_service = enterprise_service
        self.bank_service = bank_service

        self.unconfirmed_list = None
        self.ent_tree = None
        self.payroll_tree = None

        self.build_manager_ui()

    def build_manager_ui(self):
        frame = self.build_main_frame()

        left = tk.Frame(frame)
        left.pack(side="left", fill="both", expand=True, padx=6)

        mid = tk.Frame(frame)
        mid.pack(side="left", fill="both", expand=True, padx=6)

        right = tk.Frame(frame)
        right.pack(side="left", fill="both", expand=True, padx=6)

        # Unconfirmed clients
        tk.Label(left, text="Клиенты, ожидающие подтверждения:").pack(anchor="w")
        self.unconfirmed_list = tk.Listbox(left, height=10)
        self.unconfirmed_list.pack(fill="both", expand=True)
        tk.Button(left, text="Обновить", command=self.refresh_unconfirmed).pack(pady=4)
        tk.Button(left, text="Подтвердить выделенного клиента", command=self.manager_confirm_selected).pack(pady=4)

        # Enterprises & employees
        tk.Label(mid, text="Предприятия:").pack(anchor="w")
        self.ent_tree = ttk.Treeview(mid, columns=("funds", "manager"), show="headings", height=10)
        self.ent_tree.heading("funds", text="Funds")
        self.ent_tree.heading("manager", text="Manager ID")
        self.ent_tree.pack(fill="both", expand=True)
        tk.Button(mid, text="Обновить предприятия", command=self.refresh_enterprises).pack(pady=4)
        tk.Button(mid, text="Добавить клиента в предприятие", command=self.manager_add_employee_dialog).pack(pady=2)
        tk.Button(mid, text="Удалить клиента из предприятия", command=self.manager_remove_employee_dialog).pack(pady=2)

        # Payroll approvals + history + block/unblock
        tk.Label(right, text="Заявки на зарплатный проект (все):").pack(anchor="w")
        self.payroll_tree = ttk.Treeview(right, columns=("enterprise", "req", "client", "amount", "approved"),
                                        show="headings", height=8)
        for col, txt in [("enterprise", "Enterprise"), ("req", "ReqID"), ("client", "ClientID"), ("amount", "Amount"), ("approved", "Approved")]:
            self.payroll_tree.heading(col, text=txt)
        self.payroll_tree.pack(fill="both", expand=True)
        tk.Button(right, text="Обновить заявки", command=self.refresh_payroll_requests).pack(pady=4)
        tk.Button(right, text="Одобрить выбранную заявку", command=self.manager_approve_selected_payroll).pack(pady=2)

        tk.Button(right, text="Блокировать/Разблокировать счёт", command=self.manager_block_unblock_account).pack(pady=6)
        tk.Button(right, text="Блокировать/Разблокировать вклад", command=self.manager_block_unblock_deposit).pack(pady=2)

        tk.Button(right, text="Просмотр истории клиента", command=self.manager_view_client_history_dialog).pack(pady=6)

        # initial
        self.refresh_unconfirmed()
        self.refresh_enterprises()
        self.refresh_payroll_requests()

    def refresh_unconfirmed(self):
        if not self.unconfirmed_list:
            return
        self.unconfirmed_list.delete(0, "end")
        for u in self.store.users.values():
            if u.role == "client" and not u.confirmed:
                self.unconfirmed_list.insert("end", f"{u.id} — {u.full_name} (login={u.login})")

    def manager_confirm_selected(self):
        sel = self.unconfirmed_list.curselection()
        if not sel:
            self.show_warning("Подтверждение", "Выберите клиента.")
            return
        line = self.unconfirmed_list.get(sel[0])
        client_id = line.split(" — ")[0]
        if client_id not in self.store.users:
            self.show_error("Ошибка", "Клиент не найден.")
            return
        self.store.users[client_id].confirmed = True
        self.store.save_log(LogEntry(actor_id=self.current_user.id, action="confirm_client", payload={"client_id": client_id}))
        self.show_info("Подтверждение", "Клиент подтверждён.")
        self.refresh_unconfirmed()

    def refresh_enterprises(self):
        if not self.ent_tree:
            return
        for i in self.ent_tree.get_children():
            self.ent_tree.delete(i)
        for e in self.store.enterprises.values():
            self.ent_tree.insert("", "end", iid=e.id, values=(f"{e.funds:.2f}", str(e.manager_id)))

    def manager_add_employee_dialog(self):
        ent_ids = list(self.store.enterprises.keys())
        if not ent_ids:
            self.show_info("Добавление", "Нет предприятий.")
            return
        eid = simpledialog.askstring("Добавить в предприятие",
                                     f"Введите id предприятия:\nДоступные: {', '.join(ent_ids)}", parent=self.parent)
        if not eid or eid not in self.store.enterprises:
            self.show_warning("Ошибка", "Неверный enterprise id.")
            return
        clients = [u for u in self.store.users.values() if u.role == "client"]
        if not clients:
            self.show_info("Добавление", "Нет клиентов.")
            return
        cid = simpledialog.askstring("Добавить клиента",
                                     f"Введите id клиента:\nДоступные: {', '.join(u.id for u in clients)}", parent=self.parent)
        if not cid or cid not in self.store.users:
            self.show_warning("Ошибка", "Неверный client id.")
            return
        try:
            self.enterprise_service.add_employee(eid, cid, manager_id=self.current_user.id)
            self.store.save_log(LogEntry(actor_id=self.current_user.id, action="add_employee",
                                        payload={"enterprise_id": eid, "client_id": cid}))
            self.show_info("Добавление", "Клиент добавлен в предприятие.")
            self.refresh_enterprises()
        except Exception as e:
            self.show_error("Ошибка", str(e))

    def manager_remove_employee_dialog(self):
        eid = simpledialog.askstring("Удалить из предприятия", "Введите id предприятия:", parent=self.parent)
        if not eid or eid not in self.store.enterprises:
            self.show_warning("Ошибка", "Неверный enterprise id.")
            return
        cid = simpledialog.askstring("Клиент id", "Введите id клиента для удаления:", parent=self.parent)
        if not cid or cid not in self.store.users:
            self.show_warning("Ошибка", "Неверный client id.")
            return
        try:
            self.enterprise_service.remove_employee(eid, cid, manager_id=self.current_user.id)
            self.store.save_log(LogEntry(actor_id=self.current_user.id, action="remove_employee",
                                        payload={"enterprise_id": eid, "client_id": cid}))
            self.show_info("Удаление", "Клиент удалён из предприятия.")
            self.refresh_enterprises()
        except Exception as e:
            self.show_error("Ошибка", str(e))

    def refresh_payroll_requests(self):
        if not self.payroll_tree:
            return
        for i in self.payroll_tree.get_children():
            self.payroll_tree.delete(i)
        for e in self.store.enterprises.values():
            for rid, req in e.payroll_requests.items():
                self.payroll_tree.insert("", "end", iid=rid,
                                         values=(f"{e.name} ({e.id})", rid, req["client_id"], f"{req['amount']:.2f}",
                                                 str(req.get("approved", False))))

    def manager_approve_selected_payroll(self):
        sel = self.payroll_tree.selection()
        if not sel:
            self.show_warning("Одобрение", "Выберите заявку.")
            return
        rid = sel[0]

        ent_id = None
        for e in self.store.enterprises.values():
            if rid in e.payroll_requests:
                ent_id = e.id
                break
        if ent_id is None:
            self.show_error("Ошибка", "Заявка не найдена.")
            return
        try:
            self.enterprise_service.approve_payroll_request(ent_id, rid, manager_id=self.current_user.id)
            self.store.save_log(LogEntry(actor_id=self.current_user.id, action="approve_payroll_request",
                                        payload={"enterprise_id": ent_id, "req_id": rid}))
            self.show_info("Одобрение", "Заявка одобрена менеджером.")
            self.refresh_payroll_requests()
        except Exception as e:
            self.show_error("Ошибка", str(e))

    def manager_block_unblock_account(self):
        w = tk.Toplevel(self.parent)
        w.title("Блокировка / Разблокировка счетов")
        tree = ttk.Treeview(w, columns=("owner", "bank", "balance", "blocked"), show="headings")
        for col, txt in [("owner", "Owner"), ("bank", "Bank"), ("balance", "Balance"), ("blocked", "Blocked")]:
            tree.heading(col, text=txt)
        tree.pack(fill="both", expand=True)
        for a in self.store.accounts_index.values():
            tree.insert("", "end", iid=a.id, values=(a.owner_id, self.store.banks[a.bank_id].name,
                                                     f"{a.balance:.2f}", str(a.blocked)))

        def toggle():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Toggle", "Выберите счёт.", parent=w)
                return
            aid = sel[0]
            a = self.bank_service.get_account(aid)
            a.blocked = not a.blocked
            self.store.save_log(LogEntry(actor_id=self.current_user.id, action="toggle_block_account",
                                        payload={"account_id": aid, "new_state": a.blocked}))
            messagebox.showinfo("Toggle", f"Новый статус: {a.blocked}", parent=w)
            tree.set(aid, "blocked", str(a.blocked))

        tk.Button(w, text="Toggle blocked", command=toggle).pack(pady=6)

    def manager_block_unblock_deposit(self):
        w = tk.Toplevel(self.parent)
        w.title("Блокировка / Разблокировка вкладов")
        tree = ttk.Treeview(w, columns=("owner", "bank", "principal", "blocked"), show="headings")
        for col, txt in [("owner", "Owner"), ("bank", "Bank"), ("principal", "Principal"), ("blocked", "Blocked")]:
            tree.heading(col, text=txt)
        tree.pack(fill="both", expand=True)
        for d in self.store.deposits_index.values():
            tree.insert("", "end", iid=d.id, values=(d.owner_id, self.store.banks[d.bank_id].name,
                                                     f"{d.principal:.2f}", str(d.blocked)))

        def toggle():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Toggle", "Выберите вклад.", parent=w)
                return
            did = sel[0]
            dep = self.bank_service._get_deposit(did)
            dep.blocked = not dep.blocked
            self.store.save_log(LogEntry(actor_id=self.current_user.id, action="toggle_block_deposit",
                                        payload={"deposit_id": did, "new_state": dep.blocked}))
            messagebox.showinfo("Toggle", f"Новый статус: {dep.blocked}", parent=w)
            tree.set(did, "blocked", str(dep.blocked))

        tk.Button(w, text="Toggle blocked", command=toggle).pack(pady=6)

    def manager_view_client_history_dialog(self):
        cid = simpledialog.askstring("История клиента", "Введите id клиента:", parent=self.parent)
        if not cid:
            return
        if cid not in [u.id for u in self.store.users.values()]:
            messagebox.showerror("Ошибка", "Клиент не найден.", parent=self.parent)
            return
        w = tk.Toplevel(self.parent)
        w.title(f"История клиента {cid}")
        txt = tk.Text(w, width=120, height=40)
        txt.pack(fill="both", expand=True)
        for acc in [a for a in self.store.accounts_index.values() if a.owner_id == cid]:
            txt.insert("end", f"\nСчет {acc.id} ({self.store.banks[acc.bank_id].name}):\n")
            for tx in acc.history:
                txt.insert("end", f"  {tx.timestamp} {tx.id} {tx.src_type}:{tx.src_id} -> {tx.dst_type}:{tx.dst_id} amount={tx.amount}\n")
        for dep in [d for d in self.store.deposits_index.values() if d.owner_id == cid]:
            txt.insert("end", f"\nВклад {dep.id} ({self.store.banks[dep.bank_id].name}):\n")
            for tx in dep.history:
                txt.insert("end", f"  {tx.timestamp} {tx.id} {tx.src_type}:{tx.src_id} -> {tx.dst_type}:{tx.dst_id} amount={tx.amount}\n")
        txt.config(state="disabled")

class AdminGUI(RoleGUIBase):
    """Интерфейс и методы для админа"""
    def __init__(self, parent, store, admin_service, current_user):
        super().__init__(parent, store, current_user)
        self.admin_service = admin_service

        self.logs_tree = None

        self.build_admin_ui()

    def build_admin_ui(self):
        frame = self.build_main_frame()

        tk.Label(frame, text="Логи действий (последние):").pack(anchor="w")
        self.logs_tree = ttk.Treeview(frame, columns=("actor", "action", "payload", "time"), show="headings")
        self.logs_tree.heading("actor", text="Actor")
        self.logs_tree.heading("action", text="Action")
        self.logs_tree.heading("payload", text="Payload")
        self.logs_tree.heading("time", text="Timestamp")
        self.logs_tree.pack(fill="both", expand=True)
        tk.Button(frame, text="Обновить логи", command=self.refresh_logs).pack(pady=6)
        tk.Button(frame, text="Показать транзакции и отменить (undo)",
                  command=self.admin_tx_undo_dialog).pack(pady=4)
        self.refresh_logs()

    def refresh_logs(self):
        if not self.logs_tree:
            return
        for i in self.logs_tree.get_children():
            self.logs_tree.delete(i)
        for l in self.store.logs[-500:]:
            payload = json.dumps(l.payload, ensure_ascii=False)
            self.logs_tree.insert("", "end", values=(l.actor_id, l.action, payload, l.timestamp))

    def admin_tx_undo_dialog(self):
        txs = list(self.store.transactions.values())
        if not txs:
            messagebox.showinfo("Undo", "Нет транзакций.", parent=self.parent)
            return
        w = tk.Toplevel(self.parent)
        w.title("Список транзакций (выберите для undo)")
        tree = ttk.Treeview(w, columns=("srcdst", "amount", "time"), show="headings")
        tree.heading("srcdst", text="Src -> Dst")
        tree.heading("amount", text="Amount")
        tree.heading("time", text="Timestamp")
        tree.pack(fill="both", expand=True)
        for tx in txs:
            tree.insert("", "end", iid=tx.id, values=(f"{tx.src_type}:{tx.src_id} -> {tx.dst_type}:{tx.dst_id}",
                                                       f"{tx.amount:.2f}", tx.timestamp))

        def do_undo():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Undo", "Выберите транзакцию.", parent=w)
                return
            txid = sel[0]
            try:
                rev = self.admin_service.undo_transaction(txid, actor_id=self.current_user.id)
                messagebox.showinfo("Undo", f"Создан обратный перевод (undo): {rev.id}", parent=self.parent)
                self.refresh_logs()
                w.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка undo", str(e), parent=w)

        tk.Button(w, text="Отменить выбранную транзакцию", command=do_undo).pack(pady=6)