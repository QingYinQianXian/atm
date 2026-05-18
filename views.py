import tkinter as tk
from tkinter import messagebox, ttk

class ATMView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("大学生软件工程项目 - ATM柜员机模拟程序")
        self.geometry("620x560")
        self.resizable(False, False)
        self.main_container = tk.Frame(self)
        self.main_container.pack(fill="both", expand=True)
        self.current_frame = None

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

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="欢迎使用ATM模拟系统", font=("微软雅黑", 16, "bold")).pack(pady=30)

        tk.Label(self, text="账号:").pack()
        self.acc_entry = tk.Entry(self)
        self.acc_entry.pack(pady=5)
        self.acc_entry.insert(0, "123456")

        tk.Label(self, text="密码:").pack()
        self.pwd_entry = tk.Entry(self, show="*")
        self.pwd_entry.pack(pady=5)
        self.pwd_entry.insert(0, "123456")

        tk.Button(self, text="登录", width=15, bg="#4CAF50", fg="white",
                  command=lambda: controller.login(self.acc_entry.get(), self.pwd_entry.get())).pack(pady=10)
        tk.Button(self, text="注册新账户", width=15, bg="#FF9800", fg="white",
                  command=controller.show_register).pack()

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="请选择服务内容", font=("微软雅黑", 14)).pack(pady=20)

        buttons = [
            ("查询余额", controller.show_balance),
            ("存款业务", controller.show_deposit),
            ("取款业务", controller.show_withdraw),
            ("转账业务", controller.show_transfer),
            ("修改密码", controller.show_change_pwd),
            ("交易明细", controller.show_transactions),
            ("退出登录", controller.logout)
        ]

        for text, cmd in buttons:
            tk.Button(self, text=text, width=20, pady=5, command=cmd).pack(pady=5)

class BalanceFrame(tk.Frame):
    def __init__(self, parent, balance, back_cmd):
        super().__init__(parent)
        tk.Label(self, text="账户当前余额", font=("微软雅黑", 14)).pack(pady=20)
        tk.Label(self, text=f"¥ {balance:.2f}", font=("Consolas", 24, "bold"), fg="blue").pack(pady=20)
        tk.Button(self, text="返回主菜单", command=back_cmd).pack(pady=20)

class ActionFrame(tk.Frame):
    def __init__(self, parent, title, label_text, submit_cmd, back_cmd):
        super().__init__(parent)
        tk.Label(self, text=title, font=("微软雅黑", 14)).pack(pady=20)
        tk.Label(self, text=label_text).pack()
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.pack(pady=10)
        tk.Button(self, text="提交", width=15, bg="#2196F3", fg="white",
                  command=lambda: submit_cmd(self.entry.get())).pack(pady=10)
        tk.Button(self, text="返回", width=15, command=back_cmd).pack()

class TransferFrame(tk.Frame):
    def __init__(self, parent, submit_cmd, back_cmd):
        super().__init__(parent)
        tk.Label(self, text="转账业务", font=("微软雅黑", 14)).pack(pady=15)

        tk.Label(self, text="目标账户:").pack()
        self.target_entry = tk.Entry(self, font=("Arial", 14))
        self.target_entry.pack(pady=5)

        tk.Label(self, text="转账金额:").pack()
        self.amount_entry = tk.Entry(self, font=("Arial", 14))
        self.amount_entry.pack(pady=5)

        tk.Button(self, text="确认转账", width=15, bg="#9C27B0", fg="white",
                  command=lambda: submit_cmd(self.target_entry.get(), self.amount_entry.get())).pack(pady=15)
        tk.Button(self, text="返回", width=15, command=back_cmd).pack()

class TransactionFrame(tk.Frame):
    def __init__(self, parent, transactions, back_cmd):
        super().__init__(parent)
        tk.Label(self, text="交易明细记录", font=("微软雅黑", 14)).pack(pady=5)

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("序号", "类型", "金额", "时间", "操作后余额", "对方账户")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=14)
        tree.heading("序号", text="序号")
        tree.heading("类型", text="类型")
        tree.heading("金额", text="金额")
        tree.heading("时间", text="时间")
        tree.heading("操作后余额", text="操作后余额")
        tree.heading("对方账户", text="对方账户")

        tree.column("序号", width=45, anchor="center", stretch=False)
        tree.column("类型", width=55, anchor="center", stretch=False)
        tree.column("金额", width=95, anchor="center", stretch=False)
        tree.column("时间", width=145, anchor="center", stretch=True)
        tree.column("操作后余额", width=110, anchor="center", stretch=True)
        tree.column("对方账户", width=80, anchor="center", stretch=False)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        if not transactions:
            tree.insert("", "end", values=("", "暂无交易记录", "", "", "", ""))

        for i, tx in enumerate(transactions, 1):
            amount_str = f"¥{tx['amount']:.2f}"
            balance_str = f"¥{tx['balance_after']:.2f}"
            target_str = tx.get("target", "") or ""
            tree.insert("", "end", values=(i, tx["type"], amount_str, tx["time"], balance_str, target_str))

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="返回主菜单", width=15, command=back_cmd).pack()

class RegisterFrame(tk.Frame):
    def __init__(self, parent, submit_cmd, back_cmd):
        super().__init__(parent)
        tk.Label(self, text="注册新账户", font=("微软雅黑", 14)).pack(pady=15)

        tk.Label(self, text="设置密码:").pack()
        self.pwd_entry = tk.Entry(self, show="*")
        self.pwd_entry.pack(pady=5)

        tk.Label(self, text="确认密码:").pack()
        self.confirm_entry = tk.Entry(self, show="*")
        self.confirm_entry.pack(pady=5)

        tk.Label(self, text="密码长度不小于6位\n不允许6位完全相同字符", fg="gray").pack(pady=5)

        tk.Button(self, text="注册", width=15, bg="#4CAF50", fg="white",
                  command=lambda: submit_cmd(self.pwd_entry.get(), self.confirm_entry.get())).pack(pady=15)
        tk.Button(self, text="返回登录", width=15, command=back_cmd).pack()

class ChangePwdFrame(tk.Frame):
    def __init__(self, parent, submit_cmd, back_cmd):
        super().__init__(parent)
        tk.Label(self, text="安全中心 - 修改密码", font=("微软雅黑", 14)).pack(pady=15)

        tk.Label(self, text="当前旧密码:").pack()
        self.old_entry = tk.Entry(self, show="*")
        self.old_entry.pack()

        tk.Label(self, text="输入新密码:").pack()
        self.new_entry = tk.Entry(self, show="*")
        self.new_entry.pack()

        tk.Label(self, text="确认新密码:").pack()
        self.confirm_entry = tk.Entry(self, show="*")
        self.confirm_entry.pack()

        tk.Button(self, text="确认修改", width=15, bg="#FF9800", fg="white",
                  command=lambda: submit_cmd(self.old_entry.get(), self.new_entry.get(), self.confirm_entry.get())).pack(pady=15)
        tk.Button(self, text="返回", width=15, command=back_cmd).pack()
