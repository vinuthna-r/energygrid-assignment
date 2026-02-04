# EnergyGrid API Client Assignment

## Overview
This repository contains a **Python client application** that fetches data for **500 solar inverter devices** from a mock EnergyGrid API. The solution strictly adheres to the given API constraints, including **rate limiting**, **batch size limits**, and **custom request authentication**.

The focus of this project is **correctness**, **reliability**, and **clean implementation** without relying on external rate-limiting libraries.

---

## Tech Stack
- Python 3.11+
- `requests` library (HTTP client)

---

## Requirements
- Python 3.11 or higher
- Mock EnergyGrid server running locally on `localhost:3000`

> **Note:** The mock server is provided as part of the assignment and is used only for local testing. It is **not included** in this repository as per the instructions.

---

## Setup & Execution

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the mock server
Navigate to the folder containing the provided `server.js` file and run:
```bash
npm install
node server.js
```
The server should start on:
```
http://localhost:3000
```

### 3. Run the client application
From this repository:
```bash
python client.py
```

---

## Implementation Details

### Serial Number Generation
- Generates **500 device serial numbers**
- Format: `SN-000` to `SN-499`

### Batching Strategy
- Maximum **10 serial numbers per request**
- Total requests sent: **50**
- Ensures compliance with API batch size constraints

### Rate Limiting
- Enforces **1 request per second**
- Implemented using `time.sleep(1)`
- Prevents API throttling and HTTP 429 errors

### Authentication & Signature Generation
Each request includes a custom `Signature` header.

**Signature format:**
```
MD5("/device/real/query" + TOKEN + TIMESTAMP)
```

**Headers sent with each request:**
- `Authorization`
- `Timestamp`
- `Signature`
- `Content-Type: application/json`

### Request Payload Format
```json
{
  "sn_list": ["SN-000", "SN-001", "..."]
}
```

### Error Handling
- Retries up to **3 times** for:
  - Network failures
  - Rate limit errors (HTTP 429)
- Logs API errors without crashing the program
- Continues processing remaining batches even if a batch fails

### Output
- Logs progress for each batch request
- Displays request status codes
- Confirms successful completion after all batches are processed
- Reports total successful responses

---

## Assumptions
- The mock server follows the API contract described in the assignment
- Server enforces strict rate limits and batch size constraints
- Localhost access is available during execution

---

## Notes
- This repository contains **only the client-side solution**
- The mock server code is **intentionally excluded**
- No external rate-limiting libraries are used, as required

---

## Conclusion
This project demonstrates:
- ✅ API integration under strict constraints
- ✅ Custom authentication handling
- ✅ Controlled request batching and rate limiting
- ✅ Clean and readable Python implementation
