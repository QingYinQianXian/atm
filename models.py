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

    def _log_transaction(self, tx_key, amount, balance_after, target=None):
        if "transactions" not in self.accounts[self.current_account]:
            self.accounts[self.current_account]["transactions"] = []
        record = {
            "type_key": tx_key,
            "amount": amount,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": balance_after,
            "target": target
        }
        self.accounts[self.current_account]["transactions"].append(record)

    def check_login(self, account, password):
        if account not in self.accounts:
            return False, "msg_account_not_exist", {}
        acc = self.accounts[account]
        locked_until = acc.get("locked_until", 0)
        if locked_until > 0:
            remaining = locked_until - int(time.time())
            if remaining > 0:
                m = remaining // 60
                s = remaining % 60
                return False, "msg_locked_remaining", {"m": m, "s": s}
            acc["locked_until"] = 0
            acc["failed_attempts"] = 0
        if acc["password"] == password:
            acc["failed_attempts"] = 0
            acc["locked_until"] = 0
            self._save_to_disk()
            self.current_account = account
            return True, "msg_login_ok", {}
        acc["failed_attempts"] = acc.get("failed_attempts", 0) + 1
        remaining = self.MAX_FAILED_ATTEMPTS - acc["failed_attempts"]
        if acc["failed_attempts"] >= self.MAX_FAILED_ATTEMPTS:
            acc["locked_until"] = int(time.time()) + self.LOCK_DURATION
            acc["failed_attempts"] = 0
            self._save_to_disk()
            return False, "msg_locked", {}
        self._save_to_disk()
        return False, "msg_login_fail", {"n": remaining}

    def get_balance(self):
        return self.accounts[self.current_account]["balance"]

    def get_transactions(self):
        return self.accounts[self.current_account].get("transactions", [])

    def deposit(self, amount):
        if amount <= 0:
            return False, "msg_deposit_err", {}
        self.accounts[self.current_account]["balance"] += amount
        balance_after = self.accounts[self.current_account]["balance"]
        self._log_transaction("tx_deposit", amount, balance_after)
        self._save_to_disk()
        return True, "msg_deposit_ok", {"balance": f"{balance_after:.2f}"}

    def withdraw(self, amount):
        if amount <= 0:
            return False, "msg_withdraw_invalid", {}
        if amount % 100 != 0:
            return False, "msg_withdraw_mod", {}
        if amount > 5000:
            return False, "msg_withdraw_limit", {}
        if amount > self.accounts[self.current_account]["balance"]:
            return False, "msg_withdraw_overdraft", {}
        self.accounts[self.current_account]["balance"] -= amount
        balance_after = self.accounts[self.current_account]["balance"]
        self._log_transaction("tx_withdraw", amount, balance_after)
        self._save_to_disk()
        return True, "msg_withdraw_ok", {"balance": f"{balance_after:.2f}"}

    def transfer(self, target_account, amount):
        if amount <= 0:
            return False, "msg_transfer_positive", {}
        if target_account not in self.accounts:
            return False, "msg_transfer_no_target", {}
        if target_account == self.current_account:
            return False, "msg_transfer_self", {}
        if amount > self.accounts[self.current_account]["balance"]:
            return False, "msg_transfer_overdraft", {}
        self.accounts[self.current_account]["balance"] -= amount
        self.accounts[target_account]["balance"] += amount
        balance_after = self.accounts[self.current_account]["balance"]
        self._log_transaction("tx_transfer_out", amount, balance_after, target_account)
        if "transactions" not in self.accounts[target_account]:
            self.accounts[target_account]["transactions"] = []
        target_balance_after = self.accounts[target_account]["balance"]
        self.accounts[target_account]["transactions"].append({
            "type_key": "tx_transfer_in",
            "amount": amount,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": target_balance_after,
            "target": self.current_account
        })
        self._save_to_disk()
        return True, "msg_transfer_ok", {
            "target": target_account,
            "amount": f"{amount:.2f}",
            "balance": f"{balance_after:.2f}"
        }

    def _generate_account(self):
        existing = sorted([int(k) for k in self.accounts.keys() if k.isdigit()])
        return str(existing[-1] + 1) if existing else "100001"

    def register(self, password, confirm_password):
        if password != confirm_password:
            return False, "msg_pwd_mismatch", {}
        if len(password) < 6:
            return False, "msg_pwd_short", {}
        if len(set(password)) == 1:
            return False, "msg_pwd_same_chars", {}
        new_account = self._generate_account()
        self.accounts[new_account] = {
            "password": password,
            "balance": 0.0,
            "failed_attempts": 0,
            "locked_until": 0
        }
        self._save_to_disk()
        return True, "msg_register_ok", {"account": new_account}

    def change_password(self, old_pwd, new_pwd, confirm_pwd):
        if old_pwd != self.accounts[self.current_account]["password"]:
            return False, "msg_pwd_old_wrong", {}
        if new_pwd != confirm_pwd:
            return False, "msg_pwd_mismatch", {}
        if len(new_pwd) < 6:
            return False, "msg_pwd_short", {}
        if len(set(new_pwd)) == 1:
            return False, "msg_pwd_same_chars", {}
        self.accounts[self.current_account]["password"] = new_pwd
        self._save_to_disk()
        return True, "msg_pwd_ok", {}
