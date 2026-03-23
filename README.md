# Bitcoin Guardian 🛡️

> A real-time monitoring agent for Bitcoin full node infrastructure — built by a construction worker learning Python.

## What This Is

Bitcoin Guardian watches over a live Bitcoin full node running on a Raspberry Pi 5 via Umbrel, plus a Nerdaxe Gamma solo miner. It connects directly to the Bitcoin Core RPC interface and checks what matters: is the node synced, are peers connected, is the mempool healthy, is the miner hashing?

This is not a toy project. This monitors real infrastructure on a real network.

## The Story Behind This

I'm Andreas — 43, professional road construction worker (asphalt, heavy machinery), now teaching myself Python and building toward a career in AI engineering.

Bitcoin Guardian started as my first real Python project. I wanted something that wasn't a tutorial exercise — something that actually runs, talks to real hardware, and does something useful. My Bitcoin node is always on. The question is whether it's healthy. Now I know.

This project is **Module 2 of Jarvis** — my long-term vision for a modular, local-first AI system that runs on edge hardware and stays under human control.

## What It Monitors

| Check | Source | Description |
|-------|--------|-------------|
| Block height | Bitcoin Core RPC | Current blockchain tip |
| Sync status | Bitcoin Core RPC | Is the node fully synced? |
| Peer connections | Bitcoin Core RPC | Active inbound + outbound peers |
| Mempool | Bitcoin Core RPC | Transaction count and size |
| Chain | Bitcoin Core RPC | Mainnet verification |
| Miner status | AxeOS API | Nerdaxe Gamma hashrate and uptime |

## Stack

- **Language**: Python 3
- **Node interface**: Bitcoin Core JSON-RPC (`python-bitcoinrpc`)
- **Miner interface**: Nerdaxe AxeOS REST API
- **Hardware**: Raspberry Pi 5 running Umbrel, Nerdaxe Gamma (BM1370, ~1.2 TH/s)
- **Network**: Local only — no external exposure

## Setup
```bash
git clone https://github.com/andy-builds-ai/bitcoin-guardian.git
cd bitcoin-guardian
pip install -r requirements.txt
```

Configure your node credentials in `.env`:
```env
RPC_HOST=192.168.x.x
RPC_PORT=8332
RPC_USER=your_rpc_user
RPC_PASSWORD=your_rpc_password
MINER_HOST=192.168.x.x
```

Run:
```bash
python bitcoin_guardian.py
```

## Roadmap

- [x] RPC connection and health checks
- [x] Miner monitoring via AxeOS
- [ ] Scheduled monitoring loop
- [ ] Telegram / email alerts
- [ ] n8n webhook integration
- [ ] Agent mode: autonomous 24/7 monitoring

## Open Issues

- [#1 relay_fee unused variable](https://github.com/andy-builds-ai/bitcoin-guardian/issues/1)
- [#2 inconsistent guard logic](https://github.com/andy-builds-ai/bitcoin-guardian/issues/2)
- [#3 connections_in default value](https://github.com/andy-builds-ai/bitcoin-guardian/issues/3)

## Part of Jarvis

Bitcoin Guardian is Module 2 in **Jarvis** — a modular, local AI platform built on edge hardware.

> *"Not selling the dog — selling the intelligent system for the dog."*

## Author

**Andreas** — Road worker. Bitcoin node operator. Python beginner. AI engineering student.
📍 Garbsen, Germany
🔗 [GitHub: andy-builds-ai](https://github.com/andy-builds-ai)

---
*Built on a Raspberry Pi 5. Watched over by a guy who used to drive asphalt rollers for a living.*
