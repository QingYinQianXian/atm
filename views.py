import tkinter as tk
from tkinter import messagebox, ttk

class ATMView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("大学软件工程项目 - ATM柜员机模拟系统")
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

    def _setup_styles(self):
        BG = "#ECEFF1"
        ACCENT = "#1565C0"
        GREEN = "#2E7D32"
        ORANGE = "#E65100"
        PURPLE = "#6A1B9A"
        RED = "#C62828"
        FONT = ("微软雅黑", 10)

        self.style.configure("TFrame", background=BG)
        self.style.configure("TLabel", background=BG, foreground="#37474F", font=FONT)
        self.style.configure("Title.TLabel", font=("微软雅黑", 18, "bold"), foreground=ACCENT)
        self.style.configure("Heading.TLabel", font=("微软雅黑", 14, "bold"), foreground="#263238")
        self.style.configure("Balance.TLabel", font=("Consolas", 26, "bold"), foreground=ACCENT)
        self.style.configure("Hint.TLabel", font=("微软雅黑", 9), foreground="#78909C")

        self.style.configure("Primary.TButton",
                             font=("微软雅黑", 10, "bold"), padding=8)
        self.style.map("Primary.TButton",
                       background=[("active", "#1976D2"), ("!active", ACCENT)],
                       foreground=[("active", "white"), ("!active", "white")])

        self.style.configure("Success.TButton",
                             font=("微软雅黑", 10, "bold"), padding=8)
        self.style.map("Success.TButton",
                       background=[("active", "#388E3C"), ("!active", GREEN)],
                       foreground=[("active", "white"), ("!active", "white")])

        self.style.configure("Warning.TButton",
                             font=("微软雅黑", 10, "bold"), padding=8)
        self.style.map("Warning.TButton",
                       background=[("active", "#FF9800"), ("!active", ORANGE)],
                       foreground=[("active", "white"), ("!active", "white")])

        self.style.configure("Purple.TButton",
                             font=("微软雅黑", 10, "bold"), padding=8)
        self.style.map("Purple.TButton",
                       background=[("active", "#7B1FA2"), ("!active", PURPLE)],
                       foreground=[("active", "white"), ("!active", "white")])

        self.style.configure("Danger.TButton",
                             font=("微软雅黑", 10, "bold"), padding=8)
        self.style.map("Danger.TButton",
                       background=[("active", "#D32F2F"), ("!active", RED)],
                       foreground=[("active", "white"), ("!active", "white")])

        self.style.configure("Menu.TButton",
                             font=("微软雅黑", 11), padding=10, width=22)

        self.style.configure("TEntry", fieldbackground="white", padding=6)
        self.style.configure("Treeview",
                             font=("微软雅黑", 9), rowheight=26, background="white")
        self.style.configure("Treeview.Heading",
                             font=("微软雅黑", 9, "bold"), background="#CFD8DC")

    def switch_frame(self, frame_class, *args, **kwargs):
        new_frame = frame_class(self.main_container, *args, **kwargs)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack(fill="both", expand=True)

    def show_message(self, title, message, is_error=False):
        if is_error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)


class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(padding=0)

        banner = tk.Frame(self, bg="#1565C0", height=120)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        tk.Label(banner, text="ATM 柜员机模拟系统", font=("微软雅黑", 20, "bold"),
                 fg="white", bg="#1565C0").pack(pady=18)
        tk.Label(banner, text="安全 · 便捷 · 可靠", font=("微软雅黑", 10),
                 fg="#BBDEFB", bg="#1565C0").pack()

        card = ttk.Frame(self, padding=25)
        card.pack(pady=30)

        body = ttk.Frame(card)
        body.pack()

        ttk.Label(body, text="账号", style="TLabel").pack(anchor="w")
        self.acc_entry = tk.Entry(body, font=("微软雅黑", 12), width=22,
                                  bd=1, relief="solid", justify="center")
        self.acc_entry.pack(pady=(2, 12), ipady=4)
        self.acc_entry.insert(0, "123456")

        ttk.Label(body, text="密码", style="TLabel").pack(anchor="w")
        self.pwd_entry = tk.Entry(body, font=("微软雅黑", 12), width=22,
                                  show="*", bd=1, relief="solid", justify="center")
        self.pwd_entry.pack(pady=(2, 20), ipady=4)
        self.pwd_entry.insert(0, "123456")
        self.pwd_entry.bind("<Return>", lambda e: controller.login(
            self.acc_entry.get(), self.pwd_entry.get()))

        btn_row = ttk.Frame(body)
        btn_row.pack()
        ttk.Button(btn_row, text="登  录", style="Primary.TButton",
                   command=lambda: controller.login(
                       self.acc_entry.get(), self.pwd_entry.get())).pack(side="left", padx=5)
        ttk.Button(btn_row, text="注册新账户", style="Warning.TButton",
                   command=controller.show_register).pack(side="left", padx=5)


class MenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, padding=0)

        header = tk.Frame(self, bg="#1565C0", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="请选择服务内容", font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#1565C0").pack(pady=15)

        menu_area = ttk.Frame(self, padding=20)
        menu_area.pack(expand=True)

        buttons = [
            ("查 询 余 额", controller.show_balance, "Primary.TButton"),
            ("存 款 业 务", controller.show_deposit, "Success.TButton"),
            ("取 款 业 务", controller.show_withdraw, "Warning.TButton"),
            ("转 账 业 务", controller.show_transfer, "Purple.TButton"),
            ("修 改 密 码", controller.show_change_pwd, "Warning.TButton"),
            ("交 易 明 细", controller.show_transactions, "Primary.TButton"),
            ("退 出 登 录", controller.logout, "Danger.TButton"),
        ]

        for text, cmd, style in buttons:
            ttk.Button(menu_area, text=text, style="Menu.TButton",
                       command=cmd).pack(pady=4)


class BalanceFrame(ttk.Frame):
    def __init__(self, parent, balance, back_cmd):
        super().__init__(parent, padding=0)

        header = tk.Frame(self, bg="#2E7D32", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="账户余额", font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#2E7D32").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        ttk.Label(body, text="当前账户余额", style="Heading.TLabel").pack(pady=(20, 10))
        ttk.Label(body, text=f"¥ {balance:,.2f}", style="Balance.TLabel").pack(pady=20)

        ttk.Button(body, text="返回主菜单", style="Primary.TButton",
                   command=back_cmd).pack(pady=20)


class ActionFrame(ttk.Frame):
    def __init__(self, parent, title, label_text, submit_cmd, back_cmd):
        super().__init__(parent, padding=0)

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

        ttk.Button(body, text="提  交", style="Primary.TButton",
                   command=lambda: submit_cmd(self.entry.get())).pack(pady=10)
        ttk.Button(body, text="返回主菜单", style="Warning.TButton",
                   command=back_cmd).pack()


class TransferFrame(ttk.Frame):
    def __init__(self, parent, submit_cmd, back_cmd):
        super().__init__(parent, padding=0)

        header = tk.Frame(self, bg="#6A1B9A", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="转账业务", font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#6A1B9A").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        ttk.Label(body, text="目标账户", style="TLabel").pack(anchor="w", pady=(20, 2))
        self.target_entry = tk.Entry(body, font=("微软雅黑", 13), width=20,
                                     bd=1, relief="solid", justify="center")
        self.target_entry.pack(pady=(0, 12), ipady=4)

        ttk.Label(body, text="转账金额", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.amount_entry = tk.Entry(body, font=("微软雅黑", 13), width=20,
                                     bd=1, relief="solid", justify="center")
        self.amount_entry.pack(pady=(0, 15), ipady=4)

        ttk.Button(body, text="确认转账", style="Purple.TButton",
                   command=lambda: submit_cmd(
                       self.target_entry.get(), self.amount_entry.get())).pack(pady=5)
        ttk.Button(body, text="返回主菜单", style="Warning.TButton",
                   command=back_cmd).pack(pady=5)


class TransactionFrame(ttk.Frame):
    def __init__(self, parent, transactions, back_cmd):
        super().__init__(parent, padding=0)

        header = tk.Frame(self, bg="#1565C0", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="交易明细记录", font=("微软雅黑", 14, "bold"),
                 fg="white", bg="#1565C0").pack(pady=12)

        tree_frame = ttk.Frame(self, padding=(10, 5))
        tree_frame.pack(fill="both", expand=True)

        columns = ("序号", "类型", "金额", "时间", "操作后余额", "对方账户")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15,
                            selectmode="none")
        tree.heading("序号", text="序号")
        tree.heading("类型", text="类型")
        tree.heading("金额", text="金额")
        tree.heading("时间", text="时间")
        tree.heading("操作后余额", text="操作后余额")
        tree.heading("对方账户", text="对方账户")

        tree.column("序号", width=45, anchor="center", stretch=False)
        tree.column("类型", width=55, anchor="center", stretch=False)
        tree.column("金额", width=100, anchor="center", stretch=False)
        tree.column("时间", width=150, anchor="center", stretch=True)
        tree.column("操作后余额", width=115, anchor="center", stretch=True)
        tree.column("对方账户", width=85, anchor="center", stretch=False)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not transactions:
            tree.insert("", "end", values=("", "暂无交易记录", "", "", "", ""))

        for i, tx in enumerate(transactions, 1):
            amount_str = f"¥{tx['amount']:,.2f}"
            balance_str = f"¥{tx['balance_after']:,.2f}"
            target_str = tx.get("target", "") or ""
            tree.insert("", "end", values=(i, tx["type"], amount_str, tx["time"], balance_str, target_str))

        ttk.Button(self, text="返回主菜单", style="Primary.TButton",
                   command=back_cmd).pack(pady=5)


class RegisterFrame(ttk.Frame):
    def __init__(self, parent, submit_cmd, back_cmd):
        super().__init__(parent, padding=0)

        header = tk.Frame(self, bg="#E65100", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="注册新账户", font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#E65100").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        ttk.Label(body, text="设置密码", style="TLabel").pack(anchor="w", pady=(20, 2))
        self.pwd_entry = tk.Entry(body, font=("微软雅黑", 12), width=20,
                                  show="*", bd=1, relief="solid", justify="center")
        self.pwd_entry.pack(pady=(0, 12), ipady=3)

        ttk.Label(body, text="确认密码", style="TLabel").pack(anchor="w", pady=(0, 2))
        self.confirm_entry = tk.Entry(body, font=("微软雅黑", 12), width=20,
                                      show="*", bd=1, relief="solid", justify="center")
        self.confirm_entry.pack(pady=(0, 12), ipady=3)

        ttk.Label(body, text="密码长度不小于6位，不允许6位完全相同字符",
                  style="Hint.TLabel").pack(pady=(0, 10))

        ttk.Button(body, text="注  册", style="Warning.TButton",
                   command=lambda: submit_cmd(
                       self.pwd_entry.get(), self.confirm_entry.get())).pack(pady=5)
        ttk.Button(body, text="返回登录", style="Primary.TButton",
                   command=back_cmd).pack(pady=5)


class ChangePwdFrame(ttk.Frame):
    def __init__(self, parent, submit_cmd, back_cmd):
        super().__init__(parent, padding=0)

        header = tk.Frame(self, bg="#E65100", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="安全中心 - 修改密码", font=("微软雅黑", 15, "bold"),
                 fg="white", bg="#E65100").pack(pady=15)

        body = ttk.Frame(self, padding=30)
        body.pack(expand=True)

        fields = [
            ("当前旧密码", "old_entry"),
            ("输入新密码", "new_entry"),
            ("确认新密码", "confirm_entry"),
        ]

        for label_text, attr in fields:
            ttk.Label(body, text=label_text, style="TLabel").pack(anchor="w", pady=(8, 2))
            entry = tk.Entry(body, font=("微软雅黑", 12), width=20,
                             show="*", bd=1, relief="solid", justify="center")
            entry.pack(pady=(0, 6), ipady=3)
            setattr(self, attr, entry)

        ttk.Button(body, text="确认修改", style="Warning.TButton",
                   command=lambda: submit_cmd(
                       self.old_entry.get(), self.new_entry.get(),
                       self.confirm_entry.get())).pack(pady=12)
        ttk.Button(body, text="返回主菜单", style="Primary.TButton",
                   command=back_cmd).pack()
