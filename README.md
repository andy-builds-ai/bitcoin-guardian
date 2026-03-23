# Bitcoin Guardian 🛡️

> A real-time health check monitor for Bitcoin full node infrastructure — built by a construction worker learning Python.

---

## What This Is

Bitcoin Guardian connects directly to a live Bitcoin full node via the Bitcoin Core RPC interface and checks what matters: is the node synced, are peers connected, is the mempool healthy?

This is not a toy project. This monitors real infrastructure on a real network — a Raspberry Pi 5 running Umbrel in a home lab.

---

## The Story Behind This

I'm Andreas — 43, professional road construction worker (asphalt, heavy machinery), now teaching myself Python and building toward a career in AI engineering.

Bitcoin Guardian started as my first real Python project. I wanted something that wasn't a tutorial exercise — something that actually runs, talks to real hardware, and does something useful. My Bitcoin node is always on. The question is whether it's healthy. Now I know.

This project is **Module 2 of Jarvis** — my long-term vision for a modular, local-first AI system that runs on edge hardware and stays under human control.

---

## What It Monitors

| Check | Source | Description |
|-------|--------|-------------|
| Block height | Bitcoin Core RPC | Current blockchain tip |
| Sync status | Bitcoin Core RPC | Is the node fully synced? |
| Peer connections | Bitcoin Core RPC | Total, inbound and outbound peers |
| Mempool | Bitcoin Core RPC | Transaction count and size |
| Disk usage | Bitcoin Core RPC | Blockchain size on disk |
| Node uptime | Bitcoin Core RPC | How long the node has been running |
| Risk assessment | Local logic | LOW / WARN / CRITICAL with reasons |

---

## Stack

- **Language**: Python 3
- **Node interface**: Bitcoin Core JSON-RPC (via `requests`)
- **Hardware**: Raspberry Pi 5 running Umbrel
- **Network**: Local only — no external exposure

---

## Setup

```bash
git clone https://github.com/andy-builds-ai/bitcoin-guardian.git
cd bitcoin-guardian
pip install requests python-dotenv
```

Create your `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your node credentials:

```env
BTC_RPC_HOST=192.168.x.x
BTC_RPC_PORT=8332
BTC_RPC_USER=your_rpc_user
BTC_RPC_PASS=your_rpc_password
```

Run:

```bash
python bitcoin_guardian.py
```

---

## Output Example

```
============================================================
  ₿ BITCOIN GUARDIAN - Health Check Report
  2026-03-24 21:00:00 UTC
============================================================

📊 BLOCKCHAIN
   Chain:          mainnet
   Block Height:   893,412
   Headers:        893,412
   Sync:           100.0%
   Disk:           643.2 GB
   Pruned:         No

🌐 NETWORK
   Version:        /Satoshi:27.0.0/
   Peers Total:    12
   Peers In:       3
   Peers Out:      9

📦 MEMPOOL
   Transactions:  4,821
   Size:          2.1 MB
   RAM-Usage:     18.3 MB

⏱️  UPTIME:         3.2 days

============================================================
   ✅ RISK: LOW - All good
============================================================
```

---

## Risk Assessment

| Level | Condition |
|-------|-----------|
| 🚨 CRITICAL | Node not synced, or fewer than 3 peers |
| ⚠️ WARN | Few peers, no inbound connections, mempool too large, or disk > 600 GB |
| ✅ LOW | Everything looks good |

---

## Roadmap

- [x] RPC connection and health checks
- [x] Risk assessment (LOW / WARN / CRITICAL)
- [x] Node uptime display
- [ ] Miner monitoring (Nerdaxe Gamma via AxeOS API)
- [ ] Scheduled monitoring loop (runs every N minutes)
- [ ] Telegram / email alerts when something is wrong
- [ ] n8n webhook integration (Jarvis pipeline)
- [ ] Agent mode: autonomous 24/7 monitoring

---

## Open Issues

- [#3 connections_in default value](https://github.com/andy-builds-ai/bitcoin-guardian/issues/3)

---

## Part of Jarvis

Bitcoin Guardian is Module 2 in **Jarvis** — a modular, local AI platform built on edge hardware.

> *"Not selling the dog — selling the intelligent system for the dog."*

---

## Author

**Andreas** — Road worker. Bitcoin node operator. Python beginner. AI engineering student.
📍 Garbsen, Germany
🔗 [GitHub: andy-builds-ai](https://github.com/andy-builds-ai)

---

*Built on a Raspberry Pi 5. Watched over by a guy who used to drive asphalt rollers for a living.*
