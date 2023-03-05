import { ethers } from "ethers";
import React, { useState, useEffect } from "react";
import {
  init,
  useConnectWallet,
  useSetChain,
  useWallets,
} from "@web3-onboard/react";

import { Button } from "@mui/material";

import injectedModule from "@web3-onboard/injected-wallets";
// import coinbaseModule from '@web3-onboard/coinbase'
// import trezorModule from '@web3-onboard/trezor'
// import ledgerModule from '@web3-onboard/ledger'
import walletConnectModule from "@web3-onboard/walletconnect";
// import portisModule from '@web3-onboard/portis'
// import fortmaticModule from '@web3-onboard/fortmatic'
// import torusModule from '@web3-onboard/torus'
// import keepkeyModule from '@web3-onboard/keepkey'
// import dcentModule from '@web3-onboard/dcent'

const injected = injectedModule();
//const coinbase = coinbaseModule()
const walletConnect = walletConnectModule();

const web3Onboard = init({
  wallets: [injected, walletConnect],
  chains: [
    {
      id: "0x1",
      token: "ETH",
      label: "Ethereum Mainnet",
      rpcUrl:
        "https://eth-mainnet.alchemyapi.io/v2/hA2ONXLuakmXgxSTdhzyGU3-hZC6339Z",
    },
    {
      id: "0x3",
      token: "tROP",
      label: "Ethereum Ropsten Testnet",
      rpcUrl: "https://ropsten.infura.io/v3/ababf9811fd845d0a167825f97eeb12b",
    },
    {
      id: "0x4",
      token: "rETH",
      label: "Ethereum Rinkeby Testnet",
      rpcUrl: "https://rinkeby.infura.io/v3/ababf9811fd845d0a167825f97eeb12b",
    },
    {
      id: "0x89",
      token: "MATIC",
      label: "Matic Mainnet",
      rpcUrl: "https://matic-mainnet.chainstacklabs.com",
    },
  ],
  appMetadata: {
    name: "LsWithFrens",
    icon: "<svg><svg/>",
    description: "See how bad your losses are with frens",
    recommendedInjectedWallets: [
      { name: "MetaMask", url: "https://metamask.io" },
      { name: "Coinbase", url: "https://wallet.coinbase.com/" },
    ],
  },
  accountCenter: {
    desktop: {
      position: "topRight",
      enabled: true,
      minimal: true,
    },
    mobile: {
      position: "topRight",
      enabled: true,
      minimal: true,
    },
  },
});

function ConnectWallet({ setProvider, setAddress }) {
  const [{ wallet, connecting }, connect, disconnect] = useConnectWallet();
  const [{ chains, connectedChain, settingChain }, setChain] = useSetChain();
  const connectedWallets = useWallets();
  let provider;

  useEffect(() => {
    if (!wallet?.provider) {
      provider = null;
    } else {
      // After this is set you can use the provider to sign or transact
      provider = new ethers.providers.Web3Provider(wallet.provider, "any");
      setProvider(provider);
      setAddress(wallet.accounts[0].address);
    }
  }, [wallet]);

  return (
    <div>
      {!wallet && (
        <Button color="secondary" variant="contained" onClick={() => connect()}>
          {connecting ? "connecting" : "connect"}
        </Button>
      )}
    </div>
  );
}

export default ConnectWallet;
