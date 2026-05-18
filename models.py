import json
import os
import time
from datetime import datetime

class ATMModel:
    MAX_FAILED_ATTEMPTS = 3
    LOCK_DURATION = 300

    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        self.initial_data = {
            "123456": {"password": "123456", "balance": 10000.0, "failed_attempts": 0, "locked_until": 0},
            "654321": {"password": "654321", "balance": 5000.0, "failed_attempts": 0, "locked_until": 0},
            "888888": {"password": "888888", "balance": 8000.0, "failed_attempts": 0, "locked_until": 0}
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
                if "failed_attempts" not in acc:
                    acc["failed_attempts"] = 0
                if "locked_until" not in acc:
                    acc["locked_until"] = 0
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
        if account not in self.accounts:
            return False, "账号不存在"
        acc = self.accounts[account]
        locked_until = acc.get("locked_until", 0)
        if locked_until > 0:
            remaining = locked_until - int(time.time())
            if remaining > 0:
                minutes = remaining // 60
                seconds = remaining % 60
                return False, f"账户已被锁定，请在 {minutes}分{seconds}秒 后重试"
            acc["locked_until"] = 0
            acc["failed_attempts"] = 0
        if acc["password"] == password:
            acc["failed_attempts"] = 0
            acc["locked_until"] = 0
            self._save_to_disk()
            self.current_account = account
            return True, "登录成功"
        acc["failed_attempts"] = acc.get("failed_attempts", 0) + 1
        remaining_attempts = self.MAX_FAILED_ATTEMPTS - acc["failed_attempts"]
        if acc["failed_attempts"] >= self.MAX_FAILED_ATTEMPTS:
            acc["locked_until"] = int(time.time()) + self.LOCK_DURATION
            acc["failed_attempts"] = 0
            self._save_to_disk()
            return False, "密码连续错误3次，账户已被锁定5分钟"
        self._save_to_disk()
        return False, f"账号或密码不正确，剩余尝试次数: {remaining_attempts}"

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

    def _generate_account(self):
        existing = sorted([int(k) for k in self.accounts.keys() if k.isdigit()])
        return str(existing[-1] + 1) if existing else "100001"

    def register(self, password, confirm_password):
        if password != confirm_password:
            return False, "两次输入的密码不一致"
        if len(password) < 6:
            return False, "密码长度至少需要6位"
        if len(set(password)) == 1:
            return False, "密码不能是完全相同的字符"
        new_account = self._generate_account()
        self.accounts[new_account] = {
            "password": password,
            "balance": 0.0,
            "failed_attempts": 0,
            "locked_until": 0
        }
        self._save_to_disk()
        return True, f"注册成功！您的账号为：{new_account}，请妥善保管"

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
