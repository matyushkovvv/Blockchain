from chain import Blockchain

if __name__ == "__main__":
    blockchain = Blockchain()
    for index in range(30000000):
        blockchain.mine()

    print(blockchain.is_chain_valid())

    for block in blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Data: {block.data}, Timestamp: {block.timestamp}")