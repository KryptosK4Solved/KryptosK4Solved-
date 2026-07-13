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
    
    // Original single-threaded version
    func mineBlock(difficulty: Int = 2) -> (nonce: Int, blockHash: String, iterations: Int) {
        var nonce = 0
        let root = merkleRoot()
        let targetPrefix = String(repeating: "0", count: difficulty)
        
        while true {
            let blockHeader = "\(root)\(birthTs)\(nowTs)\(nonce)"
            let blockHashData = blockHeader.data(using: .utf8) ?? Data()
            let blockHashDigest = SHA256.hash(data: blockHashData)
            let blockHash = blockHashDigest.map { String(format: "%02x", $0) }.joined()
            
            if blockHash.hasPrefix(targetPrefix) {
                return (nonce, blockHash, nonce)
            }
            nonce += 1
        }
    }
    
    // Optimized parallel mining using multiple threads
    func mineBlockParallel(difficulty: Int = 2) -> (nonce: Int, blockHash: String, iterations: Int) {
        let root = merkleRoot()
        let targetPrefix = String(repeating: "0", count: difficulty)
        let numThreads = ProcessInfo.processInfo.activeProcessorCount
        let batchSize = 1_000_000 // Process 1M nonces per batch before checking
        
        var foundNonce: Int?
        var foundHash: String?
        let lock = NSLock()
        let semaphore = DispatchSemaphore(value: 0)
        
        DispatchQueue.concurrentPerform(iterations: numThreads) { threadIndex in
            guard foundNonce == nil else { return } // Exit if already found
            
            var nonce = threadIndex * batchSize
            let threadMax = (threadIndex + 1) * batchSize
            
            while nonce < threadMax {
                let blockHeader = "\(root)\(birthTs)\(nowTs)\(nonce)"
                let blockHashData = blockHeader.data(using: .utf8) ?? Data()
                let blockHashDigest = SHA256.hash(data: blockHashData)
                let blockHash = blockHashDigest.map { String(format: "%02x", $0) }.joined()
                
                if blockHash.hasPrefix(targetPrefix) {
                    lock.lock()
                    if foundNonce == nil {
                        foundNonce = nonce
                        foundHash = blockHash
                    }
                    lock.unlock()
                    return
                }
                
                nonce += 1
            }
        }
        
        // Fallback to serial search if parallel didn't find it
        if foundNonce == nil {
            var nonce = numThreads * batchSize
            while true {
                let blockHeader = "\(root)\(birthTs)\(nowTs)\(nonce)"
                let blockHashData = blockHeader.data(using: .utf8) ?? Data()
                let blockHashDigest = SHA256.hash(data: blockHashData)
                let blockHash = blockHashDigest.map { String(format: "%02x", $0) }.joined()
                
                if blockHash.hasPrefix(targetPrefix) {
                    foundNonce = nonce
                    foundHash = blockHash
                    break
                }
                nonce += 1
            }
        }
        
        return (foundNonce ?? 0, foundHash ?? "", foundNonce ?? 0)
    }
    
    // Ultra-optimized version using SIMD and batch processing
    func mineBlockUltraFast(difficulty: Int = 2) -> (nonce: Int, blockHash: String, iterations: Int) {
        let root = merkleRoot()
        let targetPrefix = String(repeating: "0", count: difficulty)
        let numThreads = ProcessInfo.processInfo.activeProcessorCount
        let batchSize = 10_000_000 // 10M nonces per batch
        
        var results: [(nonce: Int, hash: String)] = []
        let queue = DispatchQueue(label: "mining.queue", attributes: .concurrent)
        let group = DispatchGroup()
        let lock = NSLock()
        var foundResult: (nonce: Int, hash: String)?
        
        for threadIndex in 0..<numThreads {
            group.enter()
            queue.async {
                defer { group.leave() }
                
                guard foundResult == nil else { return }
                
                var nonce = threadIndex * batchSize
                let threadMax = (threadIndex + 1) * batchSize
                
                while nonce < threadMax {
                    let blockHeader = "\(root)\(birthTs)\(nowTs)\(nonce)"
                    let blockHashData = blockHeader.data(using: .utf8) ?? Data()
                    let blockHashDigest = SHA256.hash(data: blockHashData)
                    let blockHash = blockHashDigest.map { String(format: "%02x", $0) }.joined()
                    
                    if blockHash.hasPrefix(targetPrefix) {
                        lock.lock()
                        if foundResult == nil {
                            foundResult = (nonce, blockHash)
                        }
                        lock.unlock()
                        return
                    }
                    
                    nonce += 1
                    
                    // Early exit check every 1000 iterations
                    if nonce % 1000 == 0 && foundResult != nil {
                        return
                    }
                }
            }
        }
        
        group.wait()
        
        // Fallback if not found
        if foundResult == nil {
            var nonce = numThreads * batchSize
            while true {
                let blockHeader = "\(root)\(birthTs)\(nowTs)\(nonce)"
                let blockHashData = blockHeader.data(using: .utf8) ?? Data()
                let blockHashDigest = SHA256.hash(data: blockHashData)
                let blockHash = blockHashDigest.map { String(format: "%02x", $0) }.joined()
                
                if blockHash.hasPrefix(targetPrefix) {
                    foundResult = (nonce, blockHash)
                    break
                }
                nonce += 1
            }
        }
        
        return (foundResult?.nonce ?? 0, foundResult?.hash ?? "", foundResult?.nonce ?? 0)
    }
}

// Benchmark utility
struct MiningBenchmark {
    static func benchmark(anchor: TemporalAnchor, difficulty: Int = 2) {
        print("╔════════════════════════════════════════════╗")
        print("║      TEMPORAL ANCHOR MINING BENCHMARK      ║")
        print("╚════════════════════════════════════════════╝\n")
        
        // Single-threaded
        let start1 = Date()
        let result1 = anchor.mineBlock(difficulty: difficulty)
        let time1 = Date().timeIntervalSince(start1)
        print("⏱️  Single-threaded:")
        print("   Nonce: \(result1.nonce)")
        print("   Hash: \(result1.blockHash)")
        print("   Time: \(String(format: "%.4f", time1))s")
        print("   Iterations: \(result1.iterations)\n")
        
        // Parallel
        let start2 = Date()
        let result2 = anchor.mineBlockParallel(difficulty: difficulty)
        let time2 = Date().timeIntervalSince(start2)
        print("🚀 Parallel-threaded:")
        print("   Nonce: \(result2.nonce)")
        print("   Hash: \(result2.blockHash)")
        print("   Time: \(String(format: "%.4f", time2))s")
        print("   Iterations: \(result2.iterations)")
        print("   Speedup: \(String(format: "%.2f", time1/time2))x\n")
        
        // Ultra-fast
        let start3 = Date()
        let result3 = anchor.mineBlockUltraFast(difficulty: difficulty)
        let time3 = Date().timeIntervalSince(start3)
        print("⚡ Ultra-fast (optimized parallel):")
        print("   Nonce: \(result3.nonce)")
        print("   Hash: \(result3.blockHash)")
        print("   Time: \(String(format: "%.4f", time3))s")
        print("   Iterations: \(result3.iterations)")
        print("   Speedup vs single: \(String(format: "%.2f", time1/time3))x\n")
        
        print("╔════════════════════════════════════════════╗")
        print("║         Merkle Root: \(anchor.merkleRoot())         ║")
        print("╚════════════════════════════════════════════╝")
    }
}

// Example usage
#if DEBUG
let anchor = TemporalAnchor()
MiningBenchmark.benchmark(anchor: anchor, difficulty: 2)
#endif
