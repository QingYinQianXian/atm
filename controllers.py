import json
from lang import TRANSLATIONS
from views import LoginFrame, MenuFrame, BalanceFrame, ActionFrame, TransferFrame, TransactionFrame, RegisterFrame, ChangePwdFrame

class ATMController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self._load_lang()
        self.view.switch_frame(LoginFrame, self)

    def _load_lang(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            self.lang = data.get("_lang", "zh")
        except (FileNotFoundError, json.JSONDecodeError):
            self.lang = "zh"

    def _save_lang(self):
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data["_lang"] = self.lang
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @property
    def tr(self):
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["zh"])

    def _t(self, key, **kwargs):
        template = self.tr.get(key, key)
        if kwargs:
            template = template.format(**kwargs)
        return template

    def toggle_language(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self._save_lang()
        self.view.title(self._t("app_title"))
        self.view.refresh_frame()

    def login(self, acc, pwd):
        success, key, kwargs = self.model.check_login(acc, pwd)
        if success:
            self.view.title(self._t("app_title"))
            self.show_menu()
        else:
            self.view.show_message(self._t("msg_error"), self._t(key, **kwargs), is_error=True)

    def logout(self):
        self.model.current_account = None
        self.view.title(self._t("app_title"))
        self.view.switch_frame(LoginFrame, self)

    def show_menu(self):
        self.view.switch_frame(MenuFrame, self)

    def show_balance(self):
        balance = self.model.get_balance()
        self.view.switch_frame(BalanceFrame, self, balance, self.show_menu)

    def show_deposit(self):
        tr = self.tr
        self.view.switch_frame(ActionFrame, self, tr["deposit_title"],
                                tr["deposit_label"], self.handle_deposit, self.show_menu)

    def handle_deposit(self, amount_str):
        try:
            amount = float(amount_str)
            success, key, kwargs = self.model.deposit(amount)
            if success:
                self.view.show_message(self._t("msg_success"), self._t(key, **kwargs))
                self.show_menu()
            else:
                self.view.show_message(self._t("msg_error"), self._t(key, **kwargs), is_error=True)
        except ValueError:
            self.view.show_message(self._t("msg_error"), self._t("msg_number_invalid"), is_error=True)

    def show_withdraw(self):
        tr = self.tr
        self.view.switch_frame(ActionFrame, self, tr["withdraw_title"],
                                tr["withdraw_label"], self.handle_withdraw, self.show_menu)

    def handle_withdraw(self, amount_str):
        try:
            amount = int(float(amount_str))
            success, key, kwargs = self.model.withdraw(amount)
            if success:
                self.view.show_message(self._t("msg_success"), self._t(key, **kwargs))
                self.show_menu()
            else:
                self.view.show_message(self._t("msg_error"), self._t(key, **kwargs), is_error=True)
        except ValueError:
            self.view.show_message(self._t("msg_error"), self._t("msg_number_invalid"), is_error=True)

    def show_transfer(self):
        self.view.switch_frame(TransferFrame, self, self.handle_transfer, self.show_menu)

    def handle_transfer(self, target_account, amount_str):
        try:
            amount = float(amount_str)
            success, key, kwargs = self.model.transfer(target_account, amount)
            if success:
                self.view.show_message(self._t("msg_success"), self._t(key, **kwargs))
                self.show_menu()
            else:
                self.view.show_message(self._t("msg_error"), self._t(key, **kwargs), is_error=True)
        except ValueError:
            self.view.show_message(self._t("msg_error"), self._t("msg_number_invalid"), is_error=True)

    def show_transactions(self):
        transactions = self.model.get_transactions()
        self.view.switch_frame(TransactionFrame, self, transactions, self.show_menu)

    def show_register(self):
        self.view.switch_frame(RegisterFrame, self, self.handle_register, self.show_login)

    def handle_register(self, password, confirm_password):
        success, key, kwargs = self.model.register(password, confirm_password)
        if success:
            self.view.show_message(self._t("msg_success"), self._t(key, **kwargs))
            self.show_login()
        else:
            self.view.show_message(self._t("msg_error"), self._t(key, **kwargs), is_error=True)

    def show_login(self):
        self.view.switch_frame(LoginFrame, self)

    def show_change_pwd(self):
        self.view.switch_frame(ChangePwdFrame, self, self.handle_change_pwd, self.show_menu)

    def handle_change_pwd(self, old, new, confirm):
        success, key, kwargs = self.model.change_password(old, new, confirm)
        if success:
            self.view.show_message(self._t("msg_success"), self._t(key, **kwargs))
            self.logout()
        else:
            self.view.show_message(self._t("msg_error"), self._t(key, **kwargs), is_error=True)
