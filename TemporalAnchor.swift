import Foundation
import CryptoKit

struct TemporalAnchor {
    var birthTs: Int
    var nowTs: Int
    var intentions: [String: String]
    
    var delta: Int {
        return nowTs - birthTs
    }
    
    var days: Int {
        return delta / 86400
    }
    
    init(birthTs: Int = 490320000) { // 1985-07-16 UTC
        self.birthTs = birthTs
        self.nowTs = Int(Date().timeIntervalSince1970)
        
        let days = (self.nowTs - birthTs) / 86400
        self.intentions = [
            "PAST_ANCHOR": "I was born on 16-07-1985",
            "PRESENT_ANCHOR": "I am here now",
            "FUTURE_ANCHOR": "I will be",
            "HEARTBEAT": "\(days) days since genesis",
            "MESSAGE": "The lattice breathes through time"
        ]
    }
    
    func hashIntention(_ text: String) -> String {
        let data = text.data(using: .utf8) ?? Data()
        let digest = SHA256.hash(data: data)
        return digest.map { String(format: "%02x", $0) }.joined()
    }
    
    func merkleRoot() -> String {
        // Hash all intention values
        var hashes = intentions.values.map { hashIntention($0) }
        
        // Collapse hashes into a single root (Merkle tree construction)
        while hashes.count > 1 {
            var temp: [String] = []
            var i = 0
            while i < hashes.count {
                let pair = hashes[i] + (i + 1 < hashes.count ? hashes[i + 1] : "")
                let pairHash = hashIntention(pair)
                temp.append(pairHash)
                i += 2
            }
            hashes = temp
        }
        
        return hashes.first ?? ""
    }
    
    func mineBlock(difficulty: Int = 2) -> (nonce: Int, blockHash: String) {
        var nonce = 0
        let root = merkleRoot()
        let targetPrefix = String(repeating: "0", count: difficulty)
        
        while true {
            let blockHeader = "\(root)\(birthTs)\(nowTs)\(nonce)"
            let blockHashData = blockHeader.data(using: .utf8) ?? Data()
            let blockHashDigest = SHA256.hash(data: blockHashData)
            let blockHash = blockHashDigest.map { String(format: "%02x", $0) }.joined()
            
            if blockHash.hasPrefix(targetPrefix) {
                return (nonce, blockHash)
            }
            nonce += 1
        }
    }
}

// Example usage
#if DEBUG
let anchor = TemporalAnchor()
let (nonce, blockHash) = anchor.mineBlock(difficulty: 2)

print("=== BLOCK #8: TEMPORAL ANCHOR (SWIFT) ===")
print("Merkle Root: \(anchor.merkleRoot())")
print("Nonce: \(nonce)")
print("Block Hash: \(blockHash)")
print("Delta Seconds: \(anchor.delta)")
print("Days Since Genesis: \(anchor.days)")
#endif
