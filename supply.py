"""Robinhood tokenized assets on Robinhood Chain: count, on-chain supply and value.

  python3 supply.py [--block N]   -> data/rh_tokenized_assets_<block>.csv   (free, public RPC only)

1. Every Robinhood token is created through one registry contract, 0x4783c67b63de2b358ac5951a7d41f47a38f3c046.
   Its creation event (topic0 below) carries the new token's address. We read all of them from genesis.
2. For each token: totalSupply() and decimals() at the chosen block (default: last block of 2026-10-25).
3. Value = supply x price. Prices are not fetched here; they are taken from data/rh_tokenized_assets_20261025.csv
   (last Yahoo Finance close before the block, or our on-chain price feed where no stock price exists).
"""
import csv, sys, requests

# eth_getLogs: the official RPC; eth_call at a past block needs an archive node (the official RPC prunes old state)
RPC = "https://rpc.mainnet.chain.robinhood.com"
ARCHIVE = ["https://robinhood.api.pocket.network", "https://rpc-robinhood.blockmachine.io"]
REGISTRY = "0x4783c67b63de2b358ac5951a7d41f47a38f3c046"
TOPIC0 = "0xd9b0c6a1c0de228715ad0fa09f3259686ee84f8cc675e03ef7e47a9cdafa76d6"
BLOCK = int(sys.argv[sys.argv.index("--block") + 1]) if "--block" in sys.argv else 97_984_802
EXCLUDE = {"PEACH_DEFI_1"}          # a test token in the registry, not an asset


def rpc(method, params, url=RPC):
    r = requests.post(url, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=120).json()
    if "error" in r:
        raise RuntimeError(r["error"])
    return r["result"]


def call(to, data):
    for url in ARCHIVE:
        try:
            out = rpc("eth_call", [{"to": to, "data": data}, hex(BLOCK)], url)
            return int(out, 16) if out not in (None, "0x") else None
        except Exception as e:
            err = e
    raise err


# 1. registry events, 1M blocks per request (larger ranges can come back empty on this RPC)
logs, a = [], 0
while a <= BLOCK:
    b = min(a + 999_999, BLOCK)
    logs += rpc("eth_getLogs", [{"address": REGISTRY, "topics": [TOPIC0], "fromBlock": hex(a), "toBlock": hex(b)}])
    a = b + 1
prices = {r["token_address"]: r for r in csv.DictReader(open("data/rh_tokenized_assets_20261025.csv"))}
print(f"{len(logs)} registry events up to block {BLOCK:,} ({len(logs) - len(EXCLUDE)} assets + {len(EXCLUDE)} test token)")

# 2. supply at the block for every published token, 3. value
rows, total = [], 0.0
for addr, p in prices.items():
    sup, dec = call(addr, "0x18160ddd"), call(addr, "0x313ce567")
    s = sup / 10 ** dec
    v = s * float(p["price_usd"])
    total += v
    rows.append({**p, "supply": s, "value_usd": v})
rows.sort(key=lambda r: -r["value_usd"])
out = f"data/rh_tokenized_assets_{BLOCK}.csv"
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"{len(rows)} assets, total ${total/1e6:,.2f}M -> {out}")
for r in rows[:5]:
    print(f"  {r['symbol']:6} {r['token_address']}  {r['supply']:>14,.4f} x ${float(r['price_usd']):,.2f} = ${r['value_usd']/1e6:,.2f}M")
