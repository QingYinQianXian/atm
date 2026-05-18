import json
import os
from datetime import datetime

class ATMModel:
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        self.initial_data = {
            "123456": {"password": "123456", "balance": 10000.0},
            "654321": {"password": "654321", "balance": 5000.0},
            "888888": {"password": "888888", "balance": 8000.0}
        }
        self.accounts = self._load_data()
        self.current_account = None

    def _load_data(self):
        if not os.path.exists(self.data_file):
            self._save_to_disk(self.initial_data)
            return self.initial_data
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not data:
                return self.initial_data
            for acc in data.values():
                if "transactions" not in acc:
                    acc["transactions"] = []
            return data
        except (json.JSONDecodeError, IOError):
            return self.initial_data

    def _save_to_disk(self, data=None):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data or self.accounts, f, ensure_ascii=False, indent=4)

    def _log_transaction(self, tx_type, amount, balance_after, target=None):
        if "transactions" not in self.accounts[self.current_account]:
            self.accounts[self.current_account]["transactions"] = []
        record = {
            "type": tx_type,
            "amount": amount,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": balance_after,
            "target": target
        }
        self.accounts[self.current_account]["transactions"].append(record)

    def check_login(self, account, password):
        if account in self.accounts and self.accounts[account]["password"] == password:
            self.current_account = account
            return True
        return False

    def get_balance(self):
        return self.accounts[self.current_account]["balance"]

    def get_transactions(self):
        return self.accounts[self.current_account].get("transactions", [])

    def deposit(self, amount):
        if amount <= 0:
            return False, "存款金额必须大于0"
        self.accounts[self.current_account]["balance"] += amount
        balance_after = self.accounts[self.current_account]["balance"]
        self._log_transaction("存款", amount, balance_after)
        self._save_to_disk()
        return True, f"存款成功，当前余额: {balance_after:.2f}元"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "金额无效"
        if amount % 100 != 0:
            return False, "取款金额必须是100的倍数"
        if amount > 5000:
            return False, "单次取款不能超过5000元"
        if amount > self.accounts[self.current_account]["balance"]:
            return False, "余额不足，不可透支"
        self.accounts[self.current_account]["balance"] -= amount
        balance_after = self.accounts[self.current_account]["balance"]
        self._log_transaction("取款", amount, balance_after)
        self._save_to_disk()
        return True, f"取款成功，当前余额: {balance_after:.2f}元"

    def transfer(self, target_account, amount):
        if amount <= 0:
            return False, "转账金额必须大于0"
        if target_account not in self.accounts:
            return False, "目标账户不存在"
        if target_account == self.current_account:
            return False, "不能转账给自己"
        if amount > self.accounts[self.current_account]["balance"]:
            return False, "余额不足，不可透支"
        self.accounts[self.current_account]["balance"] -= amount
        self.accounts[target_account]["balance"] += amount
        balance_after = self.accounts[self.current_account]["balance"]
        self._log_transaction("转出", amount, balance_after, target_account)
        if "transactions" not in self.accounts[target_account]:
            self.accounts[target_account]["transactions"] = []
        target_balance_after = self.accounts[target_account]["balance"]
        self.accounts[target_account]["transactions"].append({
            "type": "转入",
            "amount": amount,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": target_balance_after,
            "target": self.current_account
        })
        self._save_to_disk()
        return True, (f"转账成功！向账户 {target_account} 转出 {amount:.2f}元，"
                      f"当前余额: {balance_after:.2f}元")

    def change_password(self, old_pwd, new_pwd, confirm_pwd):
        if old_pwd != self.accounts[self.current_account]["password"]:
            return False, "旧密码输入错误"
        if new_pwd != confirm_pwd:
            return False, "两次输入的新密码不一致"
        if len(new_pwd) < 6:
            return False, "新密码长度至少需要6位"
        if len(set(new_pwd)) == 1:
            return False, "新密码不能是完全相同的字符"
        self.accounts[self.current_account]["password"] = new_pwd
        self._save_to_disk()
        return True, "密码修改成功，请重新登录"
