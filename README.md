# ⚖️ SmartEFD AI Bridge

**Tanzania Revenue Authority — Innovation Challenge 2026**

An AI-powered, blockchain-verified Electronic Fiscal Device (EFD) receipt system that detects tax evasion in real-time and stores permanent receipt records on the Avalanche blockchain.

---

## 🌍 Overview

SmartEFD AI Bridge combines Artificial Intelligence, Big Data analytics, and Blockchain technology to modernize Tanzania's EFD receipt infrastructure — addressing all 6 areas of the TRA Innovation Competition:

| # | TRA Area | How SmartEFD Addresses It |
|---|----------|--------------------------|
| 1 | Kupanua wigo wa kodi | USSD channel reaches informal sector |
| 2 | Kupunguza gharama za makusanyo | Automated AI scoring replaces manual audit selection |
| 3 | Kutumia AI kurahisisha huduma | Real-time 0–100 risk scoring engine |
| 4 | Kutatua migogoro ya kodi haraka | Blockchain provides immutable tamper-proof receipt records |
| 5 | Kuimarisha huduma za kodi kidijitali | Full bilingual Swahili/English web portal |
| 6 | Kurahisisha makadirio kwa biashara ndogo | Risk scoring designed for micro-transactions |

---

## ⚙️ Tech Stack

- **AI Engine** — Python risk scoring (4-factor, 0–100 score)
- **Backend** — Flask REST API (6 endpoints)
- **Blockchain** — Solidity smart contract on Avalanche C-Chain
- **Frontend** — Bilingual Swahili/English TRA-styled portal
- **Database** — JSON transaction history with gap detection

---

## 🔗 Smart Contract

- **Network:** Avalanche Fuji Testnet (Chain ID: 43113)
- **Contract:** `0x8F241Ab76e7aAB7B4D10711E9fEB650EC8c41f7F`
- **Explorer:** [View on SnowTrace](https://testnet.snowtrace.io/address/0x8F241Ab76e7aAB7B4D10711E9fEB650EC8c41f7F)

---

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install flask flask-cors web3 python-dotenv

# 2. Create .env file with your wallet key
echo "WALLET_PRIVATE_KEY=0xYourKey" > .env

# 3. Start the server
python app.py

# 4. Open browser
# http://localhost:5000
```

---

## 📁 Project Structure
smartefd-backend/data/
├── receipt.py           # Receipt data model
├── risk_engine.py       # AI risk scoring (0–100)
├── history_tracker.py   # Transaction history & gap detection
├── app.py               # Flask REST API (6 routes)
├── blockchain.py        # Avalanche C-Chain integration
├── index.html           # TRA portal (4 tabs, bilingual)
└── verify.html          # Public QR verification page

---

## 🎯 Risk Scoring Engine

| Factor | Max Points | Why |
|--------|-----------|-----|
| Transaction amount | 40 pts | Large sales are most common evasion method |
| Item category | 20 pts | Fuel & liquor have highest evasion rates in Tanzania |
| Time of transaction | 20 pts | Late-night transactions bypass normal oversight |
| Missing fields | 20 pts | No cashier ID = EFD may have been bypassed |

**Verdicts:** LOW ✅ (0–25) · MEDIUM ⚠️ (26–50) · HIGH 🔶 (51–75) · CRITICAL 🚨 (76–100)

---

## 🌐 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Server status check |
| POST | `/receipt` | Issue receipt + AI risk score |
| POST | `/receipt/onchain` | Store receipt hash on blockchain |
| GET | `/risk/<uin>` | Business risk profile |
| GET | `/summary` | All businesses risk dashboard |
| GET | `/verify/<receipt_id>` | Blockchain verification |

---

## 👨‍💻 Developer

**Godwin Erasmi (Imma Shirima)**
First-year Computer Science & Information Systems Engineering
St. Joseph University of Engineering and Technology (SJUIT), Dar es Salaam

- GitHub: [@imma-dotcom](https://github.com/imma-dotcom)
- Brand: [@imma__shirima](https://instagram.com/imma__shirima) — Tech ngumu, lugha rahisi

---

*Built for the TRA Innovation Challenge 2026 · Avalanche Blockchain · Pamoja Tunajenga Taifa Letu 🇹🇿*