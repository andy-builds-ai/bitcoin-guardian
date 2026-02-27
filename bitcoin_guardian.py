"""
Bitcoin Guardian v1 - Health Check
Überwacht deine Bitcoin Full Node via RPC-API.
"""

import requests
import json
import os
import sys
from datetime import datetime, timezone

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

RPC_HOST = os.getenv("BTC_RPC_HOST", "192.168.2.102")
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
        print(f"[CONNECTION ERROR] Kann {RPC_URL} nicht erreichen.")
        print("Prüfe: Läuft Bitcoin Core? Ist die IP korrekt?")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"[TIMEOUT] {RPC_URL} antwortet nicht.")
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
        "connections_in": data.get("connections_in", 0),
        "connections_out": data.get("connections_out", 0),
        "connections_total": data["connections"],
        "relay_fee": data["relayfee"]
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
        return f"{days:.1f} Tage"
    return f"{hours:.1f} Stunden"


def assess_risk(blockchain, network, mempool):
    risks = []
    risk_level = "LOW"

    if blockchain["sync_progress"] < 99.9:
        risks.append(f"Node nicht vollständig synchronisiert ({blockchain['sync_progress']}%)")
        risk_level = "CRITICAL"

    if network["connections_total"] < 3:
        risks.append(f"Sehr wenige Peers ({network['connections_total']})")
        risk_level = "CRITICAL"
    elif network["connections_total"] < 8:
        risks.append(f"Wenige Peers ({network['connections_total']})")
        if risk_level != "CRITICAL":
            risk_level = "WARN"

    if network["connections_in"] == 0:
        risks.append("Keine eingehenden Verbindungen (Port 8333 offen?)")
        if risk_level == "LOW":
            risk_level = "WARN"

    if mempool["size_mb"] > 300:
        risks.append(f"Mempool sehr groß ({mempool['size_mb']} MB)")
        if risk_level == "LOW":
            risk_level = "WARN"

    if blockchain["size_on_disk_gb"] > 600:
        risks.append(f"Blockchain belegt {blockchain['size_on_disk_gb']} GB Speicher")
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
    print(f"   Pruned:         {'Ja' if blockchain['pruned'] else 'Nein'}")

    print(f"\n🌐 NETZWERK")
    print(f"   Version:        {network['version']}")
    print(f"   Peers Total:    {network['connections_total']}")
    print(f"   Peers In:       {network['connections_in']}")
    print(f"   Peers Out:      {network['connections_out']}")

    print(f"\n📦 MEMPOOL")
    print(f"   Transaktionen:  {mempool['tx_count']:,}")
    print(f"   Größe:          {mempool['size_mb']} MB")
    print(f"   RAM-Nutzung:    {mempool['memory_mb']} MB")

    if uptime:
        print(f"\n⏱️  UPTIME:         {uptime}")

    print(f"\n{'=' * 60}")
    if risk_level == "LOW":
        print(f"   ✅ RISK: {risk_level} - Alles in Ordnung")
    elif risk_level == "WARN":
        print(f"   ⚠️  RISK: {risk_level}")
    else:
        print(f"   🚨 RISK: {risk_level}")

    if risks:
        for r in risks:
            print(f"   → {r}")
    else:
        print("   Keine Auffälligkeiten.")

    print("=" * 60)


def main():
    if not RPC_USER or not RPC_PASS:
        print("[ERROR] BTC_RPC_USER oder BTC_RPC_PASS nicht gesetzt.")
        print("Erstelle eine .env Datei oder setze die Umgebungsvariable.")
        print("Siehe README.md für Details.")
        sys.exit(1)

    print("₿ Bitcoin Guardian startet...\n")

    blockchain = get_blockchain_info()
    network = get_network_info()
    mempool = get_mempool_info()
    uptime = get_uptime()

    if not all([blockchain, network, mempool]):
        print("[ERROR] Konnte nicht alle Daten abrufen.")
        sys.exit(1)

    risk_level, risks = assess_risk(blockchain, network, mempool)
    print_report(blockchain, network, mempool, uptime, risk_level, risks)


if __name__ == "__main__":
    main()