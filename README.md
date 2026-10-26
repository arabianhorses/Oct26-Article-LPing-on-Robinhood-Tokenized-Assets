# LPing on Robinhood Tokenized Assets (26 Oct 2026)

Data behind the article *LPing on Robinhood Tokenized Assets*: every asset Robinhood has tokenized on Robinhood Chain,
with its on-chain supply and value at the end of **25 October 2026** (block **97,984,802**).

## Headline numbers

- **203 tokenized assets.** Every Robinhood token is created through one registry contract,
  [`0x4783c67b63de2b358ac5951a7d41f47a38f3c046`](https://robin.etherscan.io/address/0x4783c67b63de2b358ac5951a7d41f47a38f3c046#events).
  Reading its creation events from genesis to the block above gives 204 tokens; one is a test token (`PEACH_DEFI_1`) and is left out.
- **$159.8M of combined on-chain value** (supply x price, summed over all 203).
- **SPY leads with $20.8M**, NVDA second with $18.7M.
- 9 assets have zero supply.

## Top 10 by on-chain value

| # | Symbol | Name | Token contract | Supply | Price | Value |
|---|---|---|---|---|---|---|
| 1 | SPY | SPDR S&P 500 ETF Trust | [`0x117cc2133c37b721f49de2a7a74833232b3b4c0c`](https://robin.etherscan.io/token/0x117cc2133c37b721f49de2a7a74833232b3b4c0c) | 27,362.98 | $761.11 | $20.83M |
| 2 | NVDA | NVIDIA | [`0xd0601ce157db5bdc3162bbac2a2c8af5320d9eec`](https://robin.etherscan.io/token/0xd0601ce157db5bdc3162bbac2a2c8af5320d9eec) | 88,540.45 | $211.11 | $18.69M |
| 3 | SPCX | SpaceX | [`0x4a0e65a3eccec6dbe60ae065f2e7bb85fae35eea`](https://robin.etherscan.io/token/0x4a0e65a3eccec6dbe60ae065f2e7bb85fae35eea) | 85,733.27 | $147.58 | $12.65M |
| 4 | CRCL | Circle Internet Group | [`0xdf0992e440dd0be65bd8439b609d6d4366bf1cb5`](https://robin.etherscan.io/token/0xdf0992e440dd0be65bd8439b609d6d4366bf1cb5) | 110,489.28 | $85.72 | $9.47M |
| 5 | GLD | SPDR Gold Trust | [`0xc9a981fee1f9dec688bb123ccdecc63d0debfc4e`](https://robin.etherscan.io/token/0xc9a981fee1f9dec688bb123ccdecc63d0debfc4e) | 22,098.26 | $366.33 | $8.10M |
| 6 | META | Meta Platforms | [`0xc0d6457c16cc70d6790dd43521c899c87ce02f35`](https://robin.etherscan.io/token/0xc0d6457c16cc70d6790dd43521c899c87ce02f35) | 10,771.89 | $640.10 | $6.90M |
| 7 | GOOGL | Alphabet Class A | [`0x2e0847e8910a9732eb3fb1bb4b70a580adad4fe3`](https://robin.etherscan.io/token/0x2e0847e8910a9732eb3fb1bb4b70a580adad4fe3) | 19,824.64 | $321.15 | $6.37M |
| 8 | MSTR | Strategy Inc. | [`0xec262a75e413fafd0df80480274532c79d42da09`](https://robin.etherscan.io/token/0xec262a75e413fafd0df80480274532c79d42da09) | 40,872.27 | $146.58 | $5.99M |
| 9 | QQQ | Invesco QQQ | [`0xd5f3879160bc7c32ebb4dc785f8a4f505888de68`](https://robin.etherscan.io/token/0xd5f3879160bc7c32ebb4dc785f8a4f505888de68) | 7,636.93 | $704.88 | $5.38M |
| 10 | MU | Micron Technology | [`0xff080c8ce2e5feadaca0da81314ae59d232d4afd`](https://robin.etherscan.io/token/0xff080c8ce2e5feadaca0da81314ae59d232d4afd) | 5,622.91 | $879.90 | $4.95M |

The full list of 203 is in [`data/rh_tokenized_assets_20261025.csv`](data/rh_tokenized_assets_20261025.csv).

## Method

| Column | Source |
|---|---|
| `token_address`, `created_block` | the registry's creation event |
| `supply` | `totalSupply()` / 10^`decimals()` on the token contract, at block 97,984,802 |
| `price_usd` | the last Yahoo Finance close before the block (markets were shut on 24-25 Oct, so Friday 23 Oct); the on-chain price feed where no stock price exists (`price_source`) |
| `value_usd` | `supply` x `price_usd` |

Supply counts every token in existence on Robinhood Chain, wherever it sits: wallets, Uniswap pools, other contracts.

## Reproduce

```
pip install requests
python3 supply.py                  # same block -> data/rh_tokenized_assets_97984802.csv, same totals
python3 supply.py --block <N>      # supply at any other block (prices from the CSV)
```

Free public RPCs only (the official Robinhood Chain RPC for logs, archive RPCs for past state). No keys.

Part of [decentralizedanalysis.com](https://decentralizedanalysis.com).
