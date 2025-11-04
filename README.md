# HomeWork-12

simple_pow_blockchain.py
Реалізація простого блокчейна з Proof-of-Work на SHA-256.
Поля блоку: data, prev_hash, nonce, hash (а також службові index, timestamp — для надійності, входять у хеш).
Genesis Block створюється першим (prev_hash="") і теж майниться за тим самим правилом.

Функції:
hash_block(...) — рахує хеш блоку;
mine_block(...) — підбирає nonce, щоб хеш починався з x нулів (hex), де x = --difficulty;
add_block(...) — додає новий блок у кінець ланцюга;
verify_chain(...) — перевіряє цілісність ланцюга й PoW;
build_blockchain(values, difficulty, ...) — будує ланцюг: кожне значення з values записується в ОКРЕМИЙ блок (разом із Genesis дає 1 + len(values) блоків).

CLI-параметри:
--difficulty (складність, за замовчуванням 5), --out (шлях до JSON), --values (набір метрик), --print (вивід блоків у консоль).

simple_pow_blockchain.json

Експортований ланцюг у форматі JSON після запуску скрипту.
Містить масив об’єктів-блоків у порядку ланцюга (від Genesis до останнього): для кожного — index, timestamp, data (одне число з values), prev_hash, nonce, hash.
