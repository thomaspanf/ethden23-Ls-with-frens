This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Incorporated sponsors and tools

We used Wallet Connect for linking the Eth address associated to verify and sign permissions used later for calculating the
PnL. We used Lens Protocol API for signing in and fetching the social graphs (aka frens) associated, this is achieved by
running a graphQL query looking for id, address, and such. It then sorts by the highest loss after calculations are
done through the python heavy PnL scripts. We also deployed an erc721 token that is awarded to the biggest Loser of the
frens list. These are deployed on zk-based rollup Scroll & Coinbase L2 Base. We used covalent API to grab the previous transactional
data of each of the valid addresses and push those into a time series database. We used Infura inconjunction with Lens to retrieve
IPFS stored data.

Contract Deploymenent

Scroll:
https://blockscout.scroll.io/address/0x75F0eE60D788efE564165a7Af2815aED15076182

Base:
https://goerli.basescan.org/address/0x432d05f94f837dbe65b998678737231837b681c0


## Running the Data Analysis

API: Before running, copy `example.env` to `.env` and replace the value for ckey with your Covalent API key.


Files:
 - `pnl1.ipynb`: using change in balance to determine buys/sells
 - `pnl2.ipynb`: using DEX swaps to determine buy/sells
 - `best_traders.ipynb`: getting PnLs of accounts given a pool
