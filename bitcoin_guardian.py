"""
Bitcoin Guardian v1 - Health Check
Monitors your Bitcoin full node via RPC API.
"""

import requests
import os
import sys
from datetime import datetime, timezone

import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

RPC_HOST = os.getenv("BTC_RPC_HOST", "127.0.0.1")
RPC_PORT = os.getenv("BTC_RPC_PORT", "8332")
RPC_USER = os.getenv("BTC_RPC_USER", "")
RPC_PASS = os.getenv("BTC_RPC_PASS", "")

RPC_URL = f"http://{RPC_HOST}:{RPC_PORT}"


def rpc_call(method, params=None):
    payload = {
        "jsonrpc": "2.0",
        "id": "bitcoin-guardian",
        "method": method,
        "params": params or []
    }
    try:
        response = requests.post(
            RPC_URL,
            json=payload,
            auth=(RPC_USER, RPC_PASS),
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        if result.get("error"):
            print(f"[RPC ERROR] {method}: {result['error']}")
            return None
        return result["result"]
    except requests.exceptions.ConnectionError:
        print(f"[CONNECTION ERROR] Cannot reach {RPC_URL}.")
        print("Check: Is Bitcoin Core running? Is the IP correct?")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {RPC_URL} did not respond.")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {method}: {e}")
        return None


def get_blockchain_info():
    data = rpc_call("getblockchaininfo")
    if not data:
        return None
    return {
        "chain": data["chain"],
        "blocks": data["blocks"],
        "headers": data["headers"],
        "sync_progress": round(data["verificationprogress"] * 100, 4),
        "size_on_disk_gb": round(data["size_on_disk"] / (1024**3), 2),
        "pruned": data["pruned"]
    }


def get_network_info():
    data = rpc_call("getnetworkinfo")
    if not data:
        return None
    return {
        "version": data["subversion"],
        "connections_in": data.get("connections_in"),
        "connections_out": data.get("connections_out"),
        "connections_total": data["connections"]
    }


def get_mempool_info():
    data = rpc_call("getmempoolinfo")
    if not data:
        return None
    return {
        "tx_count": data["size"],
        "size_mb": round(data["bytes"] / (1024**2), 2),
        "memory_mb": round(data["usage"] / (1024**2), 2)
    }


def get_uptime():
    seconds = rpc_call("uptime")
    if seconds is None:
        return None
    hours = seconds / 3600
    days = seconds / 86400
    if days >= 1:
        return f"{days:.1f} days"
    return f"{hours:.1f} hours"


def assess_risk(blockchain, network, mempool):
    risks = []
    risk_level = "LOW"

    if blockchain["sync_progress"] < 99.9:
        risks.append(f"Node not fully synced ({blockchain['sync_progress']}%)")
        risk_level = "CRITICAL"

    if network["connections_total"] < 3:
        risks.append(f"Very few peers ({network['connections_total']})")
        risk_level = "CRITICAL"
    elif network["connections_total"] < 8:
        risks.append(f"Few Peers ({network['connections_total']})")
        if risk_level == "LOW":
            risk_level = "WARN"

    if network["connections_in"] == 0:
        risks.append("No incoming connections (check port 8333)")
        if risk_level == "LOW":
            risk_level = "WARN"

    if mempool["size_mb"] > 300:
        risks.append(f"Mempool very large ({mempool['size_mb']} MB)")
        if risk_level == "LOW":
            risk_level = "WARN"

    if blockchain["size_on_disk_gb"] > 600:
        risks.append(f"Blockchain using {blockchain['size_on_disk_gb']} GB disk space")
        if risk_level == "LOW":
            risk_level = "WARN"

    return risk_level, risks


def print_report(blockchain, network, mempool, uptime, risk_level, risks):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    print("=" * 60)
    print("  ₿ BITCOIN GUARDIAN - Health Check Report")
    print(f"  {timestamp}")
    print("=" * 60)

    print(f"\n📊 BLOCKCHAIN")
    print(f"   Chain:          {blockchain['chain']}")
    print(f"   Block Height:   {blockchain['blocks']:,}")
    print(f"   Headers:        {blockchain['headers']:,}")
    print(f"   Sync:           {blockchain['sync_progress']}%")
    print(f"   Disk:           {blockchain['size_on_disk_gb']} GB")
    print(f"   Pruned:         {'Yes' if blockchain['pruned'] else 'No'}")

    print(f"\n🌐 NETWORK")
    print(f"   Version:        {network['version']}")
    print(f"   Peers Total:    {network['connections_total']}")
    print(f"   Peers In:       {network['connections_in'] if network['connections_in'] is not None else 'N/A'}")
    print(f"   Peers Out:      {network['connections_out'] if network['connections_out'] is not None else 'N/A'}")

    print(f"\n📦 MEMPOOL")
    print(f"   Transactions:  {mempool['tx_count']:,}")
    print(f"   Size:          {mempool['size_mb']} MB")
    print(f"   RAM-Usage:     {mempool['memory_mb']} MB")

    if uptime:
        print(f"\n⏱️  UPTIME:         {uptime}")

    print(f"\n{'=' * 60}")
    if risk_level == "LOW":
        print(f"   ✅ RISK: {risk_level} - All good")
    elif risk_level == "WARN":
        print(f"   ⚠️  RISK: {risk_level}")
    else:
        print(f"   🚨 RISK: {risk_level}")

    if risks:
        for r in risks:
            print(f"   → {r}")
    else:
        print("   No issues found.")

    print("=" * 60)


def build_prompt(blockchain, network, mempool, uptime, risk_level, risks):
    risks_text = "\n".join(f"- {r}" for r in risks) if risks else "- none"
    uptime_display = uptime if uptime else "unknown"

    return f"""You are a Bitcoin node monitoring assistant. Analyze the following node status and provide a brief health assessment in 3-4 sentences.

NODE STATUS:
- Block height: {blockchain['blocks']}
- Headers: {blockchain['headers']}
- Sync progress: {blockchain['sync_progress']}%
- Connections (total): {network['connections_total']}
- Mempool transactions: {mempool['tx_count']}
- Uptime: {uptime_display}
- Risk level (rule-based): {risk_level}

DETECTED ISSUES:
{risks_text}

Give a calm, factual assessment. Do not invent numbers. Reference only the values above."""


def save_report(llm_text, hallucinated, risk_level):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    filepath = reports_dir / f"{timestamp}.md"

    hallucination_text = "clean" if not hallucinated else f"flagged: {hallucinated}"

    content = f"""# Bitcoin Guardian Agent Report

**Timestamp:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")}
**Risk level (rule-based):** {risk_level}
**Hallucination check:** {hallucination_text}

---

## LLM Analysis

{llm_text}
"""

    filepath.write_text(content, encoding="utf-8")
    print(f"\n📄 Report saved: {filepath}")


def run_agent_mode(blockchain, network, mempool, uptime, risk_level, risks, provider="anthropic"):
    from llm_providers import call_llm
    from validators import validate_response, extract_numbers

    print(f"\n🤖 Agent mode active ({provider}) - generating LLM analysis...")

    prompt = build_prompt(blockchain, network, mempool, uptime, risk_level, risks)
    llm_text = call_llm(prompt, provider=provider)

    uptime_value = float(uptime.split()[0]) if uptime else 0

    real_data = {
        "blocks": blockchain["blocks"],
        "headers": blockchain["headers"],
        "connections": network["connections_total"],
        "mempool_tx": mempool["tx_count"],
        "sync_progress": blockchain["sync_progress"],
        "disk_gb": blockchain["size_on_disk_gb"],
        "uptime_value": uptime_value,
    }

    hallucinated = validate_response(real_data, llm_text, prompt_numbers=extract_numbers(prompt))

    save_report(llm_text, hallucinated, risk_level)

    print(llm_text)
    if hallucinated:
        print(f"\n⚠️ Hallucination check: numbers not in source data: {hallucinated}")
    else:
        print("\n✅ Hallucination check: clean")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", action="store_true", help="Run with LLM analysis")
    parser.add_argument(
        "--provider",
        choices=["anthropic", "ollama"],
        default="anthropic",
        help="LLM provider for agent mode (default: anthropic)"
    )
    args = parser.parse_args()

    if not RPC_USER or not RPC_PASS:
        print("[ERROR] BTC_RPC_USER or BTC_RPC_PASS not set.")
        print("Create a .env file or set the environment variable.")
        print("See README.md for details.")
        sys.exit(1)

    print("₿ Bitcoin Guardian starting...\n")

    blockchain = get_blockchain_info()
    network = get_network_info()
    mempool = get_mempool_info()
    uptime = get_uptime()

    if not all([blockchain, network, mempool]):
        print("[ERROR] Could not retrieve all data.")
        sys.exit(1)

    risk_level, risks = assess_risk(blockchain, network, mempool)
    print_report(blockchain, network, mempool, uptime, risk_level, risks)

    if args.agent:
        run_agent_mode(blockchain, network, mempool, uptime, risk_level, risks, provider=args.provider)


if __name__ == "__main__":
    main()