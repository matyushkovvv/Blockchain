import hashlib
import time
from ecdsa import SigningKey, SECP256k1

class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.address = self.__generate_address()

    def __generate_address(self):
        sha256 = hashlib.sha256(self.public_key.to_string()).hexdigest()
        ripemd160 = hashlib.new("ripemd160", sha256.encode()).hexdigest()
        return f"0x{ripemd160}"

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

    def calculate_hash(self):
        return hashlib.sha256(f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}".encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.proof = 1
        self.reward = 12
        self.emisson = 21102592
        self.chain = [self.__create_genesis_block()]

    def __create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block", "0", 0) 
    
    def get_top_block(self):
        return self.chain[-1]
    
    def trigger(self):
        if len(self.chain) % 2024 == 0:
            self.proof += 1

        if len(self.chain) % 131072 == 0:
            self.reward /= 2

        if self.reward > self.emisson:
            self.reward = self.emission

    def mine(self):
        nonce = 0
        new_block = self.create_new_block("new block", nonce)

        while not new_block.hash.startswith("0" * self.proof):
            nonce += 1
            new_block = self.create_new_block("new block", nonce)

        self.add_block(new_block)
        self.trigger()
    
    def add_block(self, new_block):
        print(f"Found new block! Hash: {new_block.hash}")
        self.chain.append(new_block)

    def create_new_block(self, data, nonce):
        top_block = self.get_top_block()
        new_block = Block(top_block.index + 1, top_block.hash, time.time(), data, "", nonce)
        new_block.hash = new_block.calculate_hash()

        return new_block

    def get_chain(self):
        return self.chain
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
            
        return True