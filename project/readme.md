# Secure ATM Banking System

This project implements a secure ATM banking system using Python. The system features:

- **Client login and transaction interface (GUI)**
- **Mutual authentication with symmetric key protocol**
- **Encrypted and authenticated message exchange**
- **AES-encrypted audit logging**
- **Live balance tracking and transaction history view**

---

## 💼 Use Case Overview
A user logs into an ATM-like GUI with a username and password. Upon login, a secure session is established between the client and server. The user may perform:
- Deposit funds
- Withdraw funds
- Check balance
- View transaction history

All actions are encrypted, authenticated, and securely logged.

---

## 🔐 Security Features

### 1. **Authenticated Key Distribution Protocol**
- Client and server share a long-term key `K_SHARED`.
- Client sends a nonce `nonce_c`.
- Server replies with its nonce `nonce_s`.
- Both derive `Master Secret = HMAC(K_SHARED, nonce_c || nonce_s)`.

### 2. **Key Derivation**
From the master secret, two keys are derived:
- `k_enc` — used for AES-128 encryption (CBC mode).
- `k_mac` — used for HMAC-SHA256 integrity checks.

### 3. **Message Confidentiality + Integrity**
- Messages are encrypted with `k_enc` using AES-CBC.
- Each message includes a MAC tag generated using `k_mac`.
- Server/client verify MAC before decrypting any message.

### 4. **Audit Logging**
- Every user action is logged in encrypted form using a symmetric key `AUDIT_KEY`.
- Format: `CustomerID | Action taken | Timestamp`
- Failed actions (e.g., "withdraw $100.00 failed - insufficient funds") are also logged.

---

## 🧭 General Workflow

1. **Login**
   - User logs in with credentials on client GUI.

2. **Secure Handshake**
   - Client and server perform a nonce-based exchange.
   - Both sides derive session keys.

3. **Transactions**
   - Deposit / Withdraw / Check Balance are securely sent and responded to.
   - Each transaction is encrypted and MAC'd.
   - Audit logs are written securely.

4. **View History**
   - User can view their encrypted, decrypted, and filtered history securely from the server.

---

## 📁 Files
- `client.py` — GUI client with authentication, secure messaging, and transaction interface
- `server.py` — Secure server handling encrypted requests and logging
- `shared.py` — Shared encryption and utility functions (if separated)
- `audit_log_secure.txt` — Encrypted audit log file

---

## ✅ Requirements Met
- [x] Mutual authentication
- [x] Symmetric key session setup
- [x] Encrypted + authenticated messages
- [x] AES-encrypted audit logging
- [x] Full GUI support and transaction history

---

## 🛠️ Libraries Used
- `socket`, `threading` — Networking
- `hmac`, `hashlib` — Keyed authentication
- `pycryptodome` — AES encryption
- `customtkinter` — GUI framework

---

## 🚀 How to Run
1. Install dependencies: `pip install pycryptodome customtkinter`
2. Start server: `python server.py`
3. Launch client: `python client.py`

---

## 🙌 Contributors
- Developed by Dexter Floreza


