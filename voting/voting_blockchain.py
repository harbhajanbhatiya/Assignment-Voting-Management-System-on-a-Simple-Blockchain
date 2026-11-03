import hashlib
import time

class Candidate:
    def __init__(self, candidate_id, name):
        self.candidate_id = candidate_id
        self.name = name

    def __str__(self):
        return f"ID: {self.candidate_id} | Name: {self.name}"

class Voter:
    def __init__(self, voter_id, name):
        self.voter_id = voter_id
        self.name = name
        self.has_voted = False

    def __str__(self):
        return f"ID: {self.voter_id} | Name: {self.name} | Voted: {self.has_voted}"

class Transaction:
    def __init__(self, voter_id, candidate_id):
        self.voter_id = voter_id
        self.candidate_id = candidate_id

    def __str__(self):
        return f"Voter {self.voter_id} voted for Candidate {self.candidate_id}"

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Format block data into a string to hash
        tx_strings = "".join([str(tx) for tx in self.transactions])
        block_string = f"{self.index}{self.timestamp}{tx_strings}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hashint() if hasattr(hashlib.sha256(), 'hashint') else hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty=2):
        # Simple Proof of Work
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block(0, [Transaction("GENESIS", "GENESIS")], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, transactions):
        new_block = Block(len(self.chain), transactions, self.get_latest_block().hash)
        print("Mining block... Please wait.")
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        print(f"Block successfully mined and added! Hash: {new_block.hash}")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]

            # Verify current hash matches recalculated hash
            if current.hash != current.calculate_hash():
                print(f"Error: Block {current.index} has been tampered with.")
                return False

            # Verify cryptographic link
            if current.previous_hash != previous.hash:
                print(f"Error: Block {current.index} link to previous block broken.")
                return False
        return True

def main():
    system = Blockchain()
    candidates = {}
    voters = {}
    pending_votes = []

    while True:
        print("\n" + "="*30)
        print(" VOTING MANAGEMENT BLOCKCHAIN ")
        print("="*30)
        print("1. Add Candidate")
        print("2. Add Voter")
        print("3. Cast Vote")
        print("4. Print Blockchain")
        print("5. Validate Chain")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            c_id = input("Enter Candidate ID: ").strip()
            if not c_id:
                print("Error: Candidate ID cannot be empty.")
                continue
            if c_id in candidates:
                print("Error: Candidate ID already exists.")
                continue
            name = input("Enter Candidate Name: ").strip()
            candidates[c_id] = Candidate(c_id, name)
            print(f"Candidate '{name}' successfully registered.")

        elif choice == '2':
            v_id = input("Enter Voter ID: ").strip()
            if not v_id:
                print("Error: Voter ID cannot be empty.")
                continue
            if v_id in voters:
                print("Error: Voter ID already exists.")
                continue
            name = input("Enter Voter Name: ").strip()
            voters[v_id] = Voter(v_id, name)
            print(f"Voter '{name}' successfully registered.")

        elif choice == '3':
            v_id = input("Enter your Voter ID: ").strip()
            if v_id not in voters:
                print("Error: Voter ID not registered.")
                continue
            if voters[v_id].has_voted:
                print("Error: Double voting prevention! This voter has already voted.")
                continue

            print("\nAvailable Candidates:")
            for c in candidates.values():
                print(f" - {c}")
            
            c_id = input("Enter Candidate ID you want to vote for: ").strip()
            if c_id not in candidates:
                print("Error: Candidate ID does not exist.")
                continue

            # Cast the vote
            tx = Transaction(v_id, c_id)
            voters[v_id].has_voted = True
            
            # Immediately add to blockchain structure as a new block for clarity
            system.add_block([tx])
            print("Vote successfully recorded on the blockchain!")

        elif choice == '4':
            print("\n--- BLOCKCHAIN CONTENTS ---")
            for block in system.chain:
                print(f"\nBlock #{block.index}")
                print(f"Timestamp: {block.timestamp}")
                print(f"Previous Hash: {block.previous_hash}")
                print(f"Hash: {block.hash}")
                print("Transactions:")
                for tx in block.transactions:
                    print(f"  - {tx}")
            print("-"*27)

        elif choice == '5':
            if system.is_chain_valid():
                print("Success: The blockchain is completely valid and untampered.")
            else:
                print("Warning: The blockchain validation failed.")

        elif choice == '6':
            print("Exiting Voting Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please select from options 1-6.")

if __name__ == '__main__':
    main()