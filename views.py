import tkinter as tk
from tkinter import messagebox, ttk

class ATMView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("640x580")
        self.resizable(False, False)

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        self._setup_styles()
        self.configure(bg="#ECEFF1")
        self.main_container = ttk.Frame(self, padding=0)
        self.main_container.pack(fill="both", expand=True)
        self.current_frame = None
        self._frame_class = None
        self._frame_args = ()
        self._frame_kwargs = {}

    def _setup_styles(self):
        BG = "#ECEFF1"
        ACCENT = "#1565C0"
        GREEN = "#2E7D32"
        ORANGE = "#E65100"
        PURPLE = "#6A1B9A"
        RED = "#C62828"

        self.style.configure("TFrame", background=BG)
        self.style.configure("TLabel", background=BG, foreground="#37474F", font=("微软雅黑", 10))
        self.style.configure("Title.TLabel", font=("微软雅黑", 18, "bold"), foreground=ACCENT)
        self.style.configure("Heading.TLabel", font=("微软雅黑", 14, "bold"), foreground="#263238")
        self.style.configure("Balance.TLabel", font=("Consolas", 26, "bold"), foreground=ACCENT)
        self.style.configure("Hint.TLabel", font=("微软雅黑", 9), foreground="#78909C")

        for name, color in [("Primary", ACCENT), ("Success", GREEN),
                             ("Warning", ORANGE), ("Purple", PURPLE), ("Danger", RED)]:
            self.style.configure(f"{name}.TButton", font=("微软雅黑", 10, "bold"), padding=8)
            self.style.map(f"{name}.TButton",
                           background=[("active", color), ("!active", color)],
                           foreground=[("active", "white"), ("!active", "white")])

        self.style.configure("Menu.TButton", font=("微软雅黑", 11), padding=10, width=22)
        self.style.configure("Lang.TButton", font=("微软雅黑", 8, "bold"), padding=4)
        self.style.configure("TEntry", fieldbackground="white", padding=6)
        self.style.configure("Treeview", font=("微软雅黑", 9), rowheight=26, background="white")
        self.style.configure("Treeview.Heading", font=("微软雅黑", 9, "bold"), background="#CFD8DC")

    def switch_frame(self, frame_class, *args, **kwargs):
        self._frame_class = frame_class
        self._frame_args = args
        self._frame_kwargs = kwargs
        new_frame = frame_class(self.main_container, *args, **kwargs)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    def refresh_frame(self):
        if self._frame_class is not None:
            self.switch_frame(self._frame_class, *self._frame_args, **self._frame_kwargs)

    def show_message(self, title, message, is_error=False):
        if is_error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)


class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(padding=0)
        tr = controller.tr

        banner = tk.Frame(self, bg="#1565C0", height=120)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        tk.Label(banner, text=tr["banner_title"], font=("微软雅黑", 20, "bold"),
                 fg="white", bg="#1565C0").pack(pady=18)
        tk.Label(banner, text=tr["banner_subtitle"], font=("微软雅黑", 10),
                 fg="#BBDEFB", bg="#1565C0").pack()

        lang_btn = ttk.Button(banner, text=tr["lang_switch"], style="Lang.TButton",
                              command=controller.toggle_language)
        lang_btn.place(relx=1.0, x=-10, y=5, anchor="ne")

        card = ttk.Frame(self, padding=25)
        card.pack(pady=30)

        body = ttk.Frame(card)
        body.pack()

        ttk.Label(body, text=tr["account"], style="TLabel").pack(anchor="w")
        self.acc_entry = tk.Entry(body, font=("微软雅黑", 12), width=22,
                                  bd=1, relief="solid", justify="center")
        self.acc_entry.pack(pady=(2, 12), ipady=4)
        self.acc_entry.insert(0, "123456")

        ttk.Label(body, text=tr["password"], style="TLabel").pack(anchor="w")
        self.pwd_entry = tk.Entry(body, font=("微软雅黑", 12), width=22,
                                  show="*", bd=1, relief="solid", justify="center")
        self.pwd_entry.pack(pady=(2, 20), ipady=4)
        self.pwd_entry.insert(0, "123456")
        self.pwd_entry.bind("<Return>", lambda e: controller.login(
            self.acc_entry.get(), self.pwd_entry.get()))

        btn_row = ttk.Frame(body)
        btn_row.pack()
        ttk.Button(btn_row, text=tr["login_btn"], style="Primary.TButton",
                   command=lambda: controller.login(
                       self.acc_entry.get(), self.pwd_entry.get())).pack(side="left", padx=5)
        ttk.Button(btn_row, text=tr["register_btn"], style="Warning.TButton",
                   command=controller.show_register).pack(side="left", padx=5)


class MenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=0)
        tr = controller.tr

        header = tk.Frame(self, bg="#1565C0", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=tr["menu_title"], font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#1565C0").pack(side="left", padx=15, pady=15)

        lang_btn = ttk.Button(header, text=tr["lang_switch"], style="Lang.TButton",
                              command=controller.toggle_language)
        lang_btn.place(relx=1.0, x=-10, rely=0.5, anchor="e")

        menu_area = ttk.Frame(self, padding=20)
        menu_area.pack(expand=True)

        buttons = [
            (tr["balance_btn"], controller.show_balance, "Primary.TButton"),
            (tr["deposit_btn"], controller.show_deposit, "Success.TButton"),
            (tr["withdraw_btn"], controller.show_withdraw, "Warning.TButton"),
            (tr["transfer_btn"], controller.show_transfer, "Purple.TButton"),
            (tr["change_pwd_btn"], controller.show_change_pwd, "Warning.TButton"),
            (tr["transactions_btn"], controller.show_transactions, "Primary.TButton"),
            (tr["logout_btn"], controller.logout, "Danger.TButton"),
        ]

        for text, cmd, style_name in buttons:
            ttk.Button(menu_area, text=text, style="Menu.TButton",
                       command=cmd).pack(pady=4)


class BalanceFrame(ttk.Frame):
    def __init__(self, parent, controller, balance, back_cmd):
        super().__init__(parent, padding=0)
        tr = controller.tr

        header = tk.Frame(self, bg="#2E7D32", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=tr["balance_title"], font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#2E7D32").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        ttk.Label(body, text=tr["balance_current"], style="Heading.TLabel").pack(pady=(20, 10))
        ttk.Label(body, text=f"¥ {balance:,.2f}", style="Balance.TLabel").pack(pady=20)

        ttk.Button(body, text=tr["back_menu"], style="Primary.TButton",
                   command=back_cmd).pack(pady=20)


class ActionFrame(ttk.Frame):
    def __init__(self, parent, controller, title, label_text, submit_cmd, back_cmd):
        super().__init__(parent, padding=0)
        tr = controller.tr

        header = tk.Frame(self, bg="#1565C0", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=title, font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#1565C0").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        ttk.Label(body, text=label_text, style="Heading.TLabel").pack(pady=(20, 10))
        self.entry = tk.Entry(body, font=("微软雅黑", 14), width=18,
                              bd=1, relief="solid", justify="center")
        self.entry.pack(pady=10, ipady=5)
        self.entry.bind("<Return>", lambda e: submit_cmd(self.entry.get()))

        ttk.Button(body, text=tr["submit"], style="Primary.TButton",
                   command=lambda: submit_cmd(self.entry.get())).pack(pady=10)
        ttk.Button(body, text=tr["back_menu"], style="Warning.TButton",
                   command=back_cmd).pack()


class TransferFrame(ttk.Frame):
    def __init__(self, parent, controller, submit_cmd, back_cmd):
        super().__init__(parent, padding=0)
        tr = controller.tr

        header = tk.Frame(self, bg="#6A1B9A", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=tr["transfer_title"], font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#6A1B9A").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        ttk.Label(body, text=tr["target_account"], style="TLabel").pack(anchor="w", pady=(20, 2))
        self.target_entry = tk.Entry(body, font=("微软雅黑", 13), width=20,
                                     bd=1, relief="solid", justify="center")
        self.target_entry.pack(pady=(0, 12), ipady=4)

        ttk.Label(body, text=tr["transfer_amount"], style="TLabel").pack(anchor="w", pady=(0, 2))
        self.amount_entry = tk.Entry(body, font=("微软雅黑", 13), width=20,
                                     bd=1, relief="solid", justify="center")
        self.amount_entry.pack(pady=(0, 15), ipady=4)

        ttk.Button(body, text=tr["transfer_confirm"], style="Purple.TButton",
                   command=lambda: submit_cmd(
                       self.target_entry.get(), self.amount_entry.get())).pack(pady=5)
        ttk.Button(body, text=tr["back_menu"], style="Warning.TButton",
                   command=back_cmd).pack(pady=5)


class TransactionFrame(ttk.Frame):
    def __init__(self, parent, controller, transactions, back_cmd):
        super().__init__(parent, padding=0)
        tr = controller.tr

        header = tk.Frame(self, bg="#1565C0", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=tr["transactions_title"], font=("微软雅黑", 14, "bold"),
                 fg="white", bg="#1565C0").pack(pady=12)

        tree_frame = ttk.Frame(self, padding=(10, 5))
        tree_frame.pack(fill="both", expand=True)

        col_labels = [tr["col_seq"], tr["col_type"], tr["col_amount"],
                      tr["col_time"], tr["col_balance"], tr["col_target"]]
        columns = ("seq", "type", "amount", "time", "balance", "target")

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15,
                            selectmode="none")
        for col_key, col_text in zip(columns, col_labels):
            tree.heading(col_key, text=col_text)

        tree.column("seq", width=45, anchor="center", stretch=False)
        tree.column("type", width=70, anchor="center", stretch=False)
        tree.column("amount", width=100, anchor="center", stretch=False)
        tree.column("time", width=150, anchor="center", stretch=True)
        tree.column("balance", width=115, anchor="center", stretch=True)
        tree.column("target", width=85, anchor="center", stretch=False)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not transactions:
            tree.insert("", "end", values=("", tr["tx_none"], "", "", "", ""))

        for i, tx in enumerate(transactions, 1):
            tx_type_display = tr.get(tx.get("type_key", ""), tx.get("type_key", ""))
            amount_str = f"¥{tx['amount']:,.2f}"
            balance_str = f"¥{tx['balance_after']:,.2f}"
            target_str = tx.get("target", "") or ""
            tree.insert("", "end", values=(i, tx_type_display, amount_str, tx["time"], balance_str, target_str))

        ttk.Button(self, text=tr["back_menu"], style="Primary.TButton",
                   command=back_cmd).pack(pady=5)


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, controller, submit_cmd, back_cmd):
        super().__init__(parent, padding=0)
        tr = controller.tr

        header = tk.Frame(self, bg="#E65100", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=tr["register_title"], font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#E65100").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        ttk.Label(body, text=tr["register_pwd"], style="TLabel").pack(anchor="w", pady=(20, 2))
        self.pwd_entry = tk.Entry(body, font=("微软雅黑", 12), width=20,
                                  show="*", bd=1, relief="solid", justify="center")
        self.pwd_entry.pack(pady=(0, 12), ipady=3)

        ttk.Label(body, text=tr["register_confirm"], style="TLabel").pack(anchor="w", pady=(0, 2))
        self.confirm_entry = tk.Entry(body, font=("微软雅黑", 12), width=20,
                                      show="*", bd=1, relief="solid", justify="center")
        self.confirm_entry.pack(pady=(0, 12), ipady=3)

        ttk.Label(body, text=tr["register_hint"], style="Hint.TLabel").pack(pady=(0, 10))

        ttk.Button(body, text=tr["register_btn_text"], style="Warning.TButton",
                   command=lambda: submit_cmd(
                       self.pwd_entry.get(), self.confirm_entry.get())).pack(pady=5)
        ttk.Button(body, text=tr["back_login"], style="Primary.TButton",
                   command=back_cmd).pack(pady=5)


class ChangePwdFrame(ttk.Frame):
    def __init__(self, parent, controller, submit_cmd, back_cmd):
        super().__init__(parent, padding=0)
        tr = controller.tr

        header = tk.Frame(self, bg="#E65100", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text=tr["pwd_title"], font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#E65100").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        fields = [
            (tr["pwd_old"], "old_entry"),
            (tr["pwd_new"], "new_entry"),
            (tr["pwd_confirm"], "confirm_entry"),
        ]

        for label_text, attr in fields:
            ttk.Label(body, text=label_text, style="TLabel").pack(anchor="w", pady=(8, 2))
            entry = tk.Entry(body, font=("微软雅黑", 12), width=20,
                             show="*", bd=1, relief="solid", justify="center")
            entry.pack(pady=(0, 6), ipady=3)
            setattr(self, attr, entry)

        ttk.Button(body, text=tr["pwd_change"], style="Warning.TButton",
                   command=lambda: submit_cmd(
                       self.old_entry.get(), self.new_entry.get(),
                       self.confirm_entry.get())).pack(pady=12)
        ttk.Button(body, text=tr["back_menu"], style="Primary.TButton",
                   command=back_cmd).pack()
