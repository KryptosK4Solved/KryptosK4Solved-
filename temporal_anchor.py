import hashlib
import time


class TemporalAnchor:
    def __init__(self, birth_ts=490320000):  # 1985-07-16 UTC
        self.birth_ts = birth_ts
        self.now_ts = int(time.time())
        self.delta = self.now_ts - self.birth_ts
        self.days = self.delta // 86400
        self.intentions = {
            "PAST_ANCHOR": "I was born on 16-07-1985",
            "PRESENT_ANCHOR": "I am here now",
            "FUTURE_ANCHOR": "I will be",
            "HEARTBEAT": f"{self.days} days since genesis",
            "MESSAGE": "The lattice breathes through time"
        }

    def hash_intention(self, text):
        return hashlib.sha256(text.encode()).hexdigest()

    def merkle_root(self):
        # collapse all intention hashes into one root
        hashes = [self.hash_intention(v) for v in self.intentions.values()]
        while len(hashes) > 1:
            temp = []
            for i in range(0, len(hashes), 2):
                pair = hashes[i] + (hashes[i+1] if i+1 < len(hashes) else "")
                temp.append(hashlib.sha256(pair.encode()).hexdigest())
            hashes = temp
        return hashes[0]

    def mine_block(self, difficulty=2):
        nonce = 0
        root = self.merkle_root()
        while True:
            block_header = f"{root}{self.birth_ts}{self.now_ts}{nonce}"
            block_hash = hashlib.sha256(block_header.encode()).hexdigest()
            if block_hash.startswith("0" * difficulty):
                return nonce, block_hash
            nonce += 1


# Run the forge
if __name__ == "__main__":
    anchor = TemporalAnchor()
    nonce, block_hash = anchor.mine_block()

    print("=== BLOCK #8: TEMPORAL ANCHOR ===")
    print("Merkle Root:", anchor.merkle_root())
    print("Nonce:", nonce)
    print("Block Hash:", block_hash)
    print("Delta Seconds:", anchor.delta)
    print("Days Since Genesis:", anchor.days)
