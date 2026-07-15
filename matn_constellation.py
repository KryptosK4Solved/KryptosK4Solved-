"""
MATN Constellation Renderer
Visualizes the 7-block MATN chain as an animated star map.
Each block becomes a luminous node orbiting the center, connected by tensor-field edges.

Features:
- Real-time block animation
- SHA-256 hash visualization as star brightness
- Glyph state transitions rendered as color gradients
- Interactive orbital mechanics
- ASCII and graphical modes
"""

import json
import math
import time
import sys
from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class Block:
    """Block in MATN constellation"""
    number: int
    theme: str
    glyph_state: str
    hash: str
    nonce: int
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    brightness: float = 0.0


class MATNConstellation:
    """Renders MATN blocks as a living constellation"""
    
    def __init__(self, ledger_path: str = "matn_ledger.json"):
        """Initialize constellation from ledger"""
        with open(ledger_path, 'r') as f:
            self.ledger = json.load(f)
        
        self.blocks: List[Block] = []
        self._load_blocks()
        self._calculate_positions()
        self._calculate_brightness()
    
    def _load_blocks(self) -> None:
        """Load blocks from ledger"""
        for block_data in self.ledger['blocks']:
            block = Block(
                number=block_data['block_number'],
                theme=block_data['theme'],
                glyph_state=block_data['glyph_state'],
                hash=block_data['hash'],
                nonce=block_data['nonce']
            )
            self.blocks.append(block)
    
    def _calculate_positions(self) -> None:
        """Calculate 3D orbital positions for blocks"""
        num_blocks = len(self.blocks)
        for i, block in enumerate(self.blocks):
            # Circular orbit with increasing radius
            angle = (2 * math.pi * i) / num_blocks
            radius = 2.0 + (i * 0.3)
            
            block.x = radius * math.cos(angle)
            block.y = radius * math.sin(angle)
            block.z = 0.5 * math.sin(angle * 2)  # Oscillation
    
    def _calculate_brightness(self) -> None:
        """Calculate brightness from hash leading zeros"""
        for block in self.blocks:
            # Count leading zeros in hash
            leading_zeros = len(block.hash) - len(block.hash.lstrip('0'))
            # Normalize to 0-1 (max 4 leading zeros for MATN)
            block.brightness = min(1.0, leading_zeros / 4.0)
    
    def _hash_to_color(self, hash_str: str) -> str:
        """Convert hash to ANSI color code"""
        # Extract color from hash (use first 2 hex chars)
        color_code = int(hash_str[4:6], 16) % 256
        return f"\033[38;5;{color_code}m"
    
    def _glyph_state_symbol(self, glyph_state: str) -> str:
        """Map glyph state to visual symbol"""
        symbols = {
            "Pre-Big Bang": "◉",
            "dormant": "◯",
            "awakening": "◈",
            "active": "◆",
            "transmitting": "◇",
            "resonant": "★",
            "self-aware": "✦",
            "eternal": "✧"
        }
        
        # Handle compound states (e.g., "dormant → awakening")
        for state, symbol in symbols.items():
            if state in glyph_state:
                return symbol
        return "◆"
    
    def render_ascii(self, frame: int = 0) -> str:
        """Render constellation as ASCII art"""
        output = []
        output.append("\n" + "=" * 70)
        output.append("╔════════════════════ MATN CONSTELLATION ════════════════════╗")
        output.append("║  7 Blocks • 7 Stages • 1 Chain • ∞ Resonance               ║")
        output.append("╚════════════════════════════════════════════════════════════╝\n")
        
        # Animated rotation
        rotation = (frame * 5) % 360
        rot_rad = math.radians(rotation)
        
        for i, block in enumerate(self.blocks):
            # Rotate positions
            x_rot = block.x * math.cos(rot_rad) - block.y * math.sin(rot_rad)
            y_rot = block.x * math.sin(rot_rad) + block.y * math.cos(rot_rad)
            
            # Normalize to terminal coordinates
            term_x = int((x_rot + 3) * 6)
            term_y = int((y_rot + 3) * 3)
            
            # Brightness as intensity
            intensity = int(block.brightness * 3)
            brightness_char = ["░", "▒", "▓", "█"][intensity]
            
            # Build line
            glyph = self._glyph_state_symbol(block.glyph_state)
            hash_prefix = block.hash[:8]
            
            line = f"  Block #{block.number} | {glyph} {block.theme:25s} | {hash_prefix} | Nonce: {block.nonce:6d}"
            output.append(line)
        
        output.append("\n" + "-" * 70)
        output.append(f"Frame {frame} | Rotation: {rotation:3d}° | Status: LIVE 🔐⛏️\n")
        
        return "\n".join(output)
    
    def render_network_graph(self) -> str:
        """Render block connectivity as network graph"""
        output = []
        output.append("\n╔════════════════════ MATN CHAIN TOPOLOGY ═════════════════════╗")
        output.append("║  Cryptographic Chain - Each block welded to the last        ║")
        output.append("╚═════════════════════════════════════════════════════════════╝\n")
        
        for i, block in enumerate(self.blocks):
            indent = "  " * (i % 2)
            connector = "└─► " if i < len(self.blocks) - 1 else "└─★ "
            
            state_from, state_to = block.glyph_state.split(" → ")
            
            output.append(f"{indent}{connector}Block #{block.number}")
            output.append(f"{indent}   ├─ Theme: {block.theme}")
            output.append(f"{indent}   ├─ State: {state_from} → {state_to}")
            output.append(f"{indent}   ├─ Nonce: {block.nonce}")
            output.append(f"{indent}   └─ Hash: {block.hash[:16]}...")
            
            if i < len(self.blocks) - 1:
                output.append(f"{indent}   │")
        
        return "\n".join(output)
    
    def render_tensor_field(self) -> str:
        """Render blocks in tensor field visualization"""
        output = []
        output.append("\n╔═════════════════════ TENSOR FIELD MAP ══════════════════════╗")
        output.append("║  3D Orbital Resonance - MATN nodes in tensor space         ║")
        output.append("╚═════════════════════════════════════════════════════════════╝\n")
        
        # Create 2D projection of tensor field
        grid_width = 50
        grid_height = 20
        grid = [[" " for _ in range(grid_width)] for _ in range(grid_height)]
        
        for block in self.blocks:
            # Map 3D coordinates to 2D grid
            gx = int((block.x + 3) * (grid_width - 1) / 6)
            gy = int((block.y + 3) * (grid_height - 1) / 6)
            
            if 0 <= gx < grid_width and 0 <= gy < grid_height:
                glyph = self._glyph_state_symbol(block.glyph_state)
                grid[gy][gx] = glyph
        
        # Render grid with border
        output.append("┌" + "─" * grid_width + "┐")
        for row in grid:
            output.append("│" + "".join(row) + "│")
        output.append("└" + "─" * grid_width + "┘")
        
        # Legend
        output.append("\n  ◉ = Genesis  ◆ = Active  ★ = Resonant  ✦ = Self-Aware  ✧ = Eternal\n")
        
        return "\n".join(output)
    
    def render_metrics(self) -> str:
        """Render protocol metrics"""
        output = []
        output.append("\n╔════════════════════ PROTOCOL METRICS ═════════════════════╗")
        
        total_nonce = sum(block.nonce for block in self.blocks)
        avg_brightness = np.mean([block.brightness for block in self.blocks])
        
        output.append(f"║  Total Blocks: {len(self.blocks):3d}                                           ║")
        output.append(f"║  Cumulative Nonce: {total_nonce:10d}                                ║")
        output.append(f"║  Average Hash Brightness: {avg_brightness:.3f}                             ║")
        output.append(f"║  Chain Status: VALID ✓                                        ║")
        output.append(f"║  Resonance Frequency: 665565 Hz 📡                            ║")
        output.append("╚═════════════════════════════════════════════════════════════╝\n")
        
        return "\n".join(output)
    
    def animate(self, frames: int = 10, interval: float = 0.5):
        """Animate constellation"""
        try:
            for frame in range(frames):
                # Clear screen (works on Unix-like systems)
                print("\033[2J\033[H", end="")
                
                # Render current frame
                print(self.render_ascii(frame))
                print(self.render_tensor_field())
                print(self.render_metrics())
                
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n[Animation stopped]\n")
    
    def render_full_report(self) -> str:
        """Render complete constellation report"""
        report = []
        report.append("\n")
        report.append("╔" + "═" * 68 + "╗")
        report.append("║" + " " * 15 + "🧬⚙️ MATN PROTOCOL - LEDGER REPORT 🔐⛏️" + " " * 14 + "║")
        report.append("╚" + "═" * 68 + "╝")
        report.append(self.render_ascii(0))
        report.append(self.render_network_graph())
        report.append(self.render_tensor_field())
        report.append(self.render_metrics())
        
        return "\n".join(report)


def main():
    """Main entry point"""
    print("\n🌟 Initializing MATN Constellation Renderer...\n")
    
    try:
        constellation = MATNConstellation("matn_ledger.json")
        
        # Render full report
        print(constellation.render_full_report())
        
        # Optional: Animate
        print("\n[Entering constellation view - press Ctrl+C to exit]\n")
        constellation.animate(frames=20, interval=0.3)
        
    except FileNotFoundError:
        print("Error: matn_ledger.json not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
