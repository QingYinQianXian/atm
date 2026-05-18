from views import LoginFrame, MenuFrame, BalanceFrame, ActionFrame, TransferFrame, TransactionFrame, ChangePwdFrame

class ATMController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.switch_frame(LoginFrame, self)

    def login(self, acc, pwd):
        if self.model.check_login(acc, pwd):
            self.show_menu()
        else:
            self.view.show_message("错误", "账号或密码不正确", is_error=True)

    def logout(self):
        self.model.current_account = None
        self.view.switch_frame(LoginFrame, self)

    def show_menu(self):
        self.view.switch_frame(MenuFrame, self)

    def show_balance(self):
        balance = self.model.get_balance()
        self.view.switch_frame(BalanceFrame, balance, self.show_menu)

    def show_deposit(self):
        self.view.switch_frame(ActionFrame, "存款业务", "请输入存款金额:",
                                self.handle_deposit, self.show_menu)

    def handle_deposit(self, amount_str):
        try:
            amount = float(amount_str)
            success, msg = self.model.deposit(amount)
            if success:
                self.view.show_message("成功", msg)
                self.show_menu()
            else:
                self.view.show_message("错误", msg, is_error=True)
        except ValueError:
            self.view.show_message("错误", "请输入有效的数字金额", is_error=True)

    def show_withdraw(self):
        self.view.switch_frame(ActionFrame, "取款业务", "请输入取款金额 (100的倍数):",
                                self.handle_withdraw, self.show_menu)

    def handle_withdraw(self, amount_str):
        try:
            amount = int(float(amount_str))
            success, msg = self.model.withdraw(amount)
            if success:
                self.view.show_message("成功", msg)
                self.show_menu()
            else:
                self.view.show_message("错误", msg, is_error=True)
        except ValueError:
            self.view.show_message("错误", "请输入有效的数字金额", is_error=True)

    def show_transfer(self):
        self.view.switch_frame(TransferFrame, self.handle_transfer, self.show_menu)

    def handle_transfer(self, target_account, amount_str):
        try:
            amount = float(amount_str)
            success, msg = self.model.transfer(target_account, amount)
            if success:
                self.view.show_message("成功", msg)
                self.show_menu()
            else:
                self.view.show_message("错误", msg, is_error=True)
        except ValueError:
            self.view.show_message("错误", "请输入有效的数字金额", is_error=True)

    def show_transactions(self):
        transactions = self.model.get_transactions()
        self.view.switch_frame(TransactionFrame, transactions, self.show_menu)

    def show_change_pwd(self):
        self.view.switch_frame(ChangePwdFrame, self.handle_change_pwd, self.show_menu)

    def handle_change_pwd(self, old, new, confirm):
        success, msg = self.model.change_password(old, new, confirm)
        if success:
            self.view.show_message("成功", msg)
            self.logout()
        else:
            self.view.show_message("错误", msg, is_error=True)
