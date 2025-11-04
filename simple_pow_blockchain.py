# -*- coding: utf-8 -*-
"""
Simple PoW Blockchain (CLI)
Usage:
  python simple_pow_blockchain.py
  python simple_pow_blockchain.py --difficulty 5 --out out/chain.json --print
  python simple_pow_blockchain.py --values 1 2 3 4 --print
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from hashlib import sha256
from time import time
from typing import List, Any
from pathlib import Path
import argparse, json

@dataclass
class Block:
    index: int
    timestamp: float
    data: Any
    prev_hash: str
    nonce: int = 0
    hash: str = ""

def hash_block(index: int, timestamp: float, data: Any, prev_hash: str, nonce: int) -> str:
    payload = f"{index}|{timestamp:.6f}|{str(data)}|{prev_hash}|{nonce}"
    return sha256(payload.encode("utf-8")).hexdigest()

def mine_block(block: Block, difficulty: int) -> Block:
    target = "0" * difficulty
    nonce = 0
    while True:
        h = hash_block(block.index, block.timestamp, block.data, block.prev_hash, nonce)
        if h.startswith(target):
            block.nonce = nonce
            block.hash = h
            return block
        nonce += 1

def create_genesis_block(difficulty: int, data: Any = "GENESIS") -> Block:
    genesis = Block(index=0, timestamp=time(), data=data, prev_hash="")
    return mine_block(genesis, difficulty)

def add_block(chain: List[Block], data: Any, difficulty: int) -> Block:
    prev = chain[-1]
    block = Block(index=prev.index + 1, timestamp=time(), data=data, prev_hash=prev.hash)
    return mine_block(block, difficulty)

def verify_chain(chain: List[Block], difficulty: int) -> bool:
    if not chain:
        return False
    prefix = "0" * difficulty
    for i, b in enumerate(chain):
        if not b.hash.startswith(prefix):
            return False
        if hash_block(b.index, b.timestamp, b.data, b.prev_hash, b.nonce) != b.hash:
            return False
        if i > 0 and b.prev_hash != chain[i - 1].hash:
            return False
    return True

def build_blockchain(values: List[Any], difficulty: int, genesis_data: Any = "GENESIS") -> List[Block]:
    chain: List[Block] = [create_genesis_block(difficulty, genesis_data)]
    for v in values:
        chain.append(add_block(chain, v, difficulty))
    return chain

def main():
    parser = argparse.ArgumentParser(description="Simple PoW Blockchain")
    parser.add_argument("--difficulty", "-d", type=int, default=5,
                        help="Сложность PoW: сколько нулей в начале hex-хеша (по умолчанию 5)")
    parser.add_argument("--out", "-o", type=str, default="out/simple_pow_blockchain.json",
                        help="Путь сохранения JSON-цепочки (по умолчанию out/simple_pow_blockchain.json)")
    parser.add_argument("--values", "-v", type=int, nargs="*",
                        default=[91911, 90954, 95590, 97390, 96578, 97211, 95090],
                        help="Значения для записи в блоки")
    parser.add_argument("--genesis-data", type=str, default="GENESIS",
                        help="Данные для Genesis-блока")
    parser.add_argument("--print", action="store_true", help="Печатать блоки после майнинга")
    args = parser.parse_args()

    t0 = time()
    chain = build_blockchain(args.values, args.difficulty, args.genesis_data)
    t1 = time()
    ok = verify_chain(chain, args.difficulty)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump([asdict(b) for b in chain], f, ensure_ascii=False, indent=2)

    print(f"Создано блоков (включая Genesis): {len(chain)}")
    print(f"Время майнинга: {t1 - t0:.2f} сек")
    print(f"Проверка цепочки: {'OK' if ok else 'FAIL'}")
    print(f"Файл сохранен: {out_path}")

    if args.print:
        for b in chain:
            print(f"""
--- Блок #{b.index} ---
timestamp : {b.timestamp:.6f}
data      : {b.data}
prev_hash : {b.prev_hash}
nonce     : {b.nonce}
hash      : {b.hash}
""".strip())

if __name__ == "__main__":
    main()
