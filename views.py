import tkinter as tk
from tkinter import messagebox

class ATMView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("大学生软件工程项目 - ATM柜员机模拟程序")
        self.geometry("480x480")
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
                  command=lambda: controller.login(self.acc_entry.get(), self.pwd_entry.get())).pack(pady=20)

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
