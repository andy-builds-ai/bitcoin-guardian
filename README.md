# ₿ Bitcoin Guardian

Health check monitor for your Bitcoin full node via RPC API.

## Features

- Blockchain status: block height, sync progress, disk usage
- Network: peer connections (in/out), node version
- Mempool: transactions, size, RAM usage
- Node uptime
- Risk assessment (LOW / WARN / CRITICAL)

## Setup

### Requirements

- Python 3.10+
- Bitcoin full node with RPC enabled (e.g. Umbrel)
- Network access to your node

### Installation
```bash
git clone https://github.com/andy-builds-ai/bitcoin-guardian.git
cd bitcoin-guardian
pip install requests python-dotenv
```

### Configuration
```bash
cp .env.example .env
```

Edit `.env` with your RPC credentials:
```
BTC_RPC_HOST=192.168.2.102
BTC_RPC_PORT=8332
BTC_RPC_USER=your_user
BTC_RPC_PASS=your_password
```

### Run
```bash
python bitcoin_guardian.py
```

## Example Output
```
============================================================
  ₿ BITCOIN GUARDIAN - Health Check Report
  2026-02-26 13:58:00 UTC
============================================================

📊 BLOCKCHAIN
   Block Height:   938,435
   Sync:           100.0%
   Disk:           767.0 GB

🌐 NETWORK
   Peers Total:    37

📦 MEMPOOL
   Transactions:   18,182

⏱️  UPTIME:         1.0 hours

============================================================
   ✅ RISK: LOW - All good
============================================================
```

## Roadmap

- [ ] Log to file instead of terminal only
- [ ] Scheduled checks (cron / Task Scheduler)
- [ ] Alerts on WARN/CRITICAL
- [ ] Web dashboard

## Tech Stack

- Python 3 + requests + python-dotenv
- Bitcoin Core RPC API
- Tested with Umbrel on Raspberry Pi 5

## Author

**Andreas** - [andy-builds-ai](https://github.com/andy-builds-ai)

Aspiring AI Engineer | Bitcoin Node Operator