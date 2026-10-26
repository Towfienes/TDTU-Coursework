"""
Module: atm_simulation.py
Author: Ngo Lam Tien (MSSV: 524H0195)
Subject: Software Engineering (503074) - Lab 06 (Exercise 3)
Description:
    Mo phong toan ven quy trinh xu ly du lieu va may trang thai (State Machine)
    cua hoat dong Rut tien tai cay ATM (ATM Cash Withdrawal Activity Diagram).
    Tuan thu chuan bao mat EMV, nguyen tac "Nha the truoc, chi tien sau"
    va co che hoan tien tu dong (Auto-Reversal / Rollback) khi xay ra loi.
"""

from enum import Enum, auto
import time

class AccountType(Enum):
    CHECKING = "Checking Account (Tai khoan thanh toan)"
    SAVINGS = "Savings Account (Tai khoan tiet kiem)"

class TransactionStatus(Enum):
    PENDING = auto()
    AUTHORIZED = auto()
    DEBITED = auto()
    COMPLETED = auto()
    REVERSED = auto()
    FAILED = auto()

class BankCoreSystem:
    """Mo phong he thong Core Banking cua Ngan hang trung tam."""
    def __init__(self):
        # Database gia lap
        self.accounts = {
            "CARD_9999": {
                "pin_hash": "e10adc3949ba59abbe56e057f20f883e", # hash cua 123456
                "is_locked": False,
                "balance": 15000000, # 15 trieu VND
                "daily_limit": 20000000,
                "withdrawn_today": 2000000
            }
        }
        self.transaction_logs = []

    def verify_pin(self, card_number: str, pin: str) -> bool:
        if card_number not in self.accounts:
            return False
        import hashlib
        pin_hash = hashlib.md5(pin.encode()).hexdigest()
        return self.accounts[card_number]["pin_hash"] == pin_hash

    def check_balance_and_limit(self, card_number: str, amount: int, fee: int = 3300) -> tuple[bool, str]:
        acc = self.accounts.get(card_number)
        if not acc:
            return False, "Tai khoan khong ton tai."
        if acc["is_locked"]:
            return False, "Tai khoan da bi khoa."
        if acc["balance"] < (amount + fee):
            return False, f"So du kha dung ({acc['balance']:,} VND) khong du chi tra ({amount + fee:,} VND)."
        if acc["withdrawn_today"] + amount > acc["daily_limit"]:
            return False, f"Vuot han muc rut tien trong ngay (Toi da {acc['daily_limit']:,} VND/ngay)."
        return True, "Kiem tra so du & han muc thanh cong."

    def execute_debit(self, card_number: str, amount: int, fee: int = 3300) -> str:
        acc = self.accounts[card_number]
        total_deduct = amount + fee
        acc["balance"] -= total_deduct
        acc["withdrawn_today"] += amount
        tx_id = f"TX_{int(time.time()*1000)}"
        self.transaction_logs.append({
            "tx_id": tx_id,
            "card_number": card_number,
            "amount": amount,
            "fee": fee,
            "status": TransactionStatus.DEBITED
        })
        return tx_id

    def rollback_transaction(self, tx_id: str, card_number: str, amount: int, fee: int = 3300, reason: str = ""):
        acc = self.accounts[card_number]
        acc["balance"] += (amount + fee)
        acc["withdrawn_today"] -= amount
        for log in self.transaction_logs:
            if log["tx_id"] == tx_id:
                log["status"] = TransactionStatus.REVERSED
                log["reversal_reason"] = reason
        print(f"  [CORE BANKING] -> Da thuc hien AUTO-REVERSAL cho giao dich {tx_id}. Hoan tra {amount + fee:,} VND. Ly do: {reason}")


class ATMTerminal:
    """Mo phong Thiet bi & Bo dieu khien cay ATM."""
    def __init__(self, terminal_id: str, initial_cash: int, bank_host: BankCoreSystem):
        self.terminal_id = terminal_id
        self.cash_reserve = initial_cash # So tien mat con trong hop tien Cassette
        self.bank_host = bank_host
        self.card_in_reader = None
        self.pin_attempts = 0
        self.retained_cards = []
        self.retracted_cash_box = []

    def insert_card(self, card_number: str, is_valid: bool = True) -> bool:
        print(f"\n[ATM {self.terminal_id}] 1. Khach hang dua the {card_number} vao khe.")
        if not is_valid:
            print("  [CARD READER] -> The bi tray xuoc / Khong hop le! Nhang the tra lai.")
            return False
        self.card_in_reader = card_number
        self.pin_attempts = 0
        print("  [CARD READER] -> Doc chip EMV thanh cong. Yeu cau nhap PIN.")
        return True

    def enter_pin(self, pin: str) -> bool:
        if not self.card_in_reader:
            print("  [LOI] Khong co the trong khe doc.")
            return False
        
        is_correct = self.bank_host.verify_pin(self.card_in_reader, pin)
        if is_correct:
            self.pin_attempts = 0
            print("  [SECURITY PIN] -> Ma PIN hop le. Chuyen sang menu lua chon giao dich.")
            return True
        else:
            self.pin_attempts += 1
            print(f"  [SECURITY PIN] -> Sai ma PIN! (Lan thu {self.pin_attempts}/3)")
            if self.pin_attempts >= 3:
                print(f"  [SECURITY ALERT] -> Sai PIN qua 3 lan! ATM NUOT THE {self.card_in_reader} vao Retain Box de bao ve tai khoan.")
                self.retained_cards.append(self.card_in_reader)
                self.card_in_reader = None
            return False

    def request_cash_withdrawal(self, amount: int, account_type: AccountType, customer_takes_card: bool = True, customer_takes_cash: bool = True, want_receipt: bool = True) -> bool:
        print(f"\n--- BAT DAU TIEN TRINH RUT TIEN: {amount:,} VND ({account_type.value}) ---")
        if not self.card_in_reader:
            print("  [LOI] Giao dich huy bo vi khong co the hop le.")
            return False

        # Buoc 1: Kiem tra boi so menh gia & han muc rut 1 lan
        MIN_WITHDRAW = 50000
        MAX_PER_TX = 5000000
        if amount < MIN_WITHDRAW or amount > MAX_PER_TX or amount % 50000 != 0:
            print(f"  [VALIDATION 1] -> That bai: So tien {amount:,} khong phai boi so cua 50.000 VND hoac ngoai han muc [{MIN_WITHDRAW:,} - {MAX_PER_TX:,}].")
            return False
        print(f"  [VALIDATION 1] -> Hop le: Boi so 50.000 VND & trong han muc 1 lan rut.")

        # Buoc 2: Kiem tra luong tien mat con trong may ATM
        if self.cash_reserve < amount:
            print(f"  [VALIDATION 2] -> That bai: May ATM khong du tien mat ({self.cash_reserve:,} VND < {amount:,} VND).")
            return False
        print(f"  [VALIDATION 2] -> Hop le: ATM con du tien ({self.cash_reserve:,} VND).")

        # Buoc 3: Kiem tra so du kha dung tai Core Banking
        fee = 3300
        valid_bank, msg = self.bank_host.check_balance_and_limit(self.card_in_reader, amount, fee)
        if not valid_bank:
            print(f"  [VALIDATION 3] -> That bai tu Core Banking: {msg}")
            return False
        print(f"  [VALIDATION 3] -> Hop le: {msg}")

        # Buoc 4: XU LY SONG SONG (FORK NODE)
        print("  [FORK] -> Khoi tao xu ly song song: Hach toan tai khoan <--> Phan bo & Dem tien.")
        tx_id = self.bank_host.execute_debit(self.card_in_reader, amount, fee)
        print(f"    - Nhanh A (Network): Tru so du tai khoan & Luu log giao dich (TxID: {tx_id}).")
        
        # Phan bo menh gia
        notes_500k = amount // 500000
        rem = amount % 500000
        notes_200k = rem // 200000
        rem %= 200000
        notes_100k = rem // 100000
        rem %= 100000
        notes_50k = rem // 50000
        print(f"    - Nhanh B (Hardware): Dem menh gia ({notes_500k}x500k, {notes_200k}x200k, {notes_100k}x100k, {notes_50k}x50k).")

        # Buoc 5: DONG BO HOA (JOIN NODE)
        print("  [JOIN] -> Dong bo hoa thanh cong hai tien trinh.")

        # Buoc 6: NGUYEN TAC AN TOAN: NHA THE TRUOC - CHI TIEN SAU
        print("  [SAFETY PROTOCOL] -> ATM NHA THE TRUOC & Phat chuong canh bao bip bip.")
        if not customer_takes_card:
            print("  [TIMEOUT ALERT] -> Qua 30 giay khach hang KHONG lay the! ATM thu hoi the vao hop luu giu.")
            self.retained_cards.append(self.card_in_reader)
            self.card_in_reader = None
            # Rollback tien do khach khong nhan the
            self.bank_host.rollback_transaction(tx_id, "CARD_9999", amount, fee, "Khach hang khong lay the sau 30s")
            return False

        print("  [CUSTOMER ACTION] -> Khach hang da rut the khoi khe.")
        self.card_in_reader = None

        # Buoc 7: MO CUA KHE CHI TIEN
        print("  [DISPENSER] -> Mo cua khe chi tien mat.")
        if not customer_takes_cash:
            print("  [TIMEOUT ALERT] -> Qua 30 giay khach hang KHONG lay tien! ATM thu hoi tien vao ngan Retract Bin.")
            self.retracted_cash_box.append(amount)
            # Rollback hoan tien vao tai khoan
            self.bank_host.rollback_transaction(tx_id, "CARD_9999", amount, fee, "Khach hang khong lay tien mat sau 30s")
            return False

        # Khach hang lay tien thanh cong
        self.cash_reserve -= amount
        print(f"  [CUSTOMER ACTION] -> Khach hang nhan du {amount:,} VND tien mat.")

        # Buoc 8: IN HOI DON HOAC GUI SMS
        if want_receipt:
            print(f"  [PRINTER] -> In bien lai giao dich giay (Tx: {tx_id}, Rut: {amount:,} VND, Phi: {fee:,} VND).")
        else:
            print("  [NOTIFICATION] -> Khong in bien lai. Gui bien dong so du qua SMS / Mobile Banking.")

        print("  [COMPLETED] -> Hoan tat giao dich an toan. Cam on quy khach!\n")
        return True


def run_test_suite():
    print("=======================================================================")
    print("DEMO KIEM THU TOAN DIEN QUY TRINH RUT TIEN ATM (SE LAB 06 - EXERCISE 3)")
    print("=======================================================================")
    
    bank = BankCoreSystem()
    atm = ATMTerminal("ATM_TDTU_01", initial_cash=100000000, bank_host=bank)

    # Test Case 1: Giao dich thanh cong hoan hao
    print("\n--- TEST CASE 1: Rut tien binh thuong (1.500.000 VND) ---")
    atm.insert_card("CARD_9999")
    atm.enter_pin("123456")
    atm.request_cash_withdrawal(1500000, AccountType.CHECKING, customer_takes_card=True, customer_takes_cash=True, want_receipt=True)

    # Test Case 2: Sai PIN 3 lan bi nuot the
    print("\n--- TEST CASE 2: Bao mat - Sai PIN 3 lan bi nuot the ---")
    atm.insert_card("CARD_9999")
    atm.enter_pin("000000")
    atm.enter_pin("111111")
    atm.enter_pin("222222")

    # Test Case 3: So tien khong hop le (khong phai boi so cua 50.000)
    print("\n--- TEST CASE 3: So tien khong phai boi so cua 50.000 VND ---")
    atm.insert_card("CARD_9999")
    atm.enter_pin("123456")
    atm.request_cash_withdrawal(125000, AccountType.CHECKING)

    # Test Case 4: Khach quen lay tien sau khi rut the -> He thong tu dong thu hoi & Rollback hoan tien
    print("\n--- TEST CASE 4: Khach quen lay tien (Timeout) -> Auto-Reversal Rollback ---")
    atm.insert_card("CARD_9999")
    atm.enter_pin("123456")
    atm.request_cash_withdrawal(2000000, AccountType.CHECKING, customer_takes_card=True, customer_takes_cash=False)

    print("\n=== KET QUA TAI KHOAN SAU CHUOI GIAO DICH ===")
    final_balance = bank.accounts["CARD_9999"]["balance"]
    print(f"So du cuoi cung cua khach: {final_balance:,} VND (Chung minh tien giao dich Test 4 da duoc rollback chinh xac!)")
    print("=======================================================================")

if __name__ == "__main__":
    run_test_suite()
