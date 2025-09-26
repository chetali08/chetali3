import hashlib
import json
import time
import uuid
import os

class EduCoinBlockchain:
    def __init__(self, storage_file="educoin_chain.json"):
        self.storage_file = storage_file
        self.chain = self.load_chain()
        self.balances = self.load_balances()

    def load_chain(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as file:
                data = json.load(file)
                return data.get("chain", [])
        return []

    def load_balances(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as file:
                data = json.load(file)
                return data.get("balances", {})
        return {}

    def save_data(self):
        with open(self.storage_file, "w") as file:
            json.dump({"chain": self.chain, "balances": self.balances}, file, indent=4)

    def generate_hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def mine_coin(self, student_name, reward=1):
        block = {
            "id": str(uuid.uuid4()),
            "student": student_name,
            "reward": reward,
            "timestamp": time.time(),
            "type": "mined"
        }
        block["hash"] = self.generate_hash(block)
        self.chain.append(block)
        self.balances[student_name] = self.balances.get(student_name, 0) + reward
        self.save_data()
        return block

    def transfer_coin(self, sender, receiver, amount):
        if self.balances.get(sender, 0) < amount:
            return False  # insufficient funds
        transfer = {
            "id": str(uuid.uuid4()),
            "from": sender,
            "to": receiver,
            "amount": amount,
            "timestamp": time.time(),
            "type": "transfer"
        }
        transfer["hash"] = self.generate_hash(transfer)
        self.chain.append(transfer)
        self.balances[sender] -= amount
        self.balances[receiver] = self.balances.get(receiver, 0) + amount
        self.save_data()
        return True

    def check_balance(self, student_name):
        return self.balances.get(student_name, 0)

    def leaderboard(self):
        return sorted(self.balances.items(), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    system = EduCoinBlockchain()

    # Simulate mining rewards
    system.mine_coin("Alice")
    system.mine_coin("Bob")
    system.mine_coin("Alice")

    # Simulate a transfer
    success = system.transfer_coin("Alice", "Bob", 1)

    print("Transfer successful" if success else "Transfer failed - insufficient funds")

    # Show balances
    print("Balances:")
    for student, balance in system.balances.items():
        print(f"{student}: {balance} EduCoin")

    # Show leaderboard
    print("\nLeaderboard:")
    for rank, (student, balance) in enumerate(system.leaderboard(), start=1):
        print(f"{rank}. {student}: {balance} EduCoin")
