# ProSign3 (ECC) — Cryptohack

**Port:** 13381  
**Category:** ECDSA Nonce Reuse / Time-Based Signing  
**Difficulty:** Medium

---

## Challenge Overview

The server exposes two options via JSON API:

| Option | Description |
|--------|-------------|
| `sign_time` | Signs the current time (`"Current time is m:n"`) using ECDSA with a **random nonce** `k ∈ [1, n)` |
| `verify` | Verifies an ECDSA signature `(r, s)` on a given message hash; if valid and message is `"unlock"`, returns flag |

The private key `d` is fixed (unknown, ~192-bit). The public key is `Q = d * G` where `G` is the NIST P-192 generator.

---

## Vulnerability

The `sign_time` endpoint signs a **predictable message** (current time to minute precision) with a **fresh random nonce** each time. However:

1. The message format is known: `"Current time is M:S"` where `M` = minute, `S` = second
2. The attacker can request signatures repeatedly
3. **Nonce reuse** is not the issue — the issue is that the message space is small and predictable

Wait — re-reading the flow: the server uses a **random nonce** for each signature. So where's the vulnerability?

Looking at `flow.md`: the attacker notices "they reuse hsh key" and mentions "HNP" (Hidden Number Problem). But with fresh random nonces, standard ECDSA is secure.

Actually, the key insight from the flow:
- `sign_time` returns `(r, s)` for the current time
- `verify` checks a signature on a **chosen message**
- We need a valid signature on `"unlock"`

If we can get the **same `r` value** (which depends only on the nonce `k`), we can combine signatures. But `k` is random each time...

Wait, the flow says: "since d could be very big... we need the message to be 'unlock'... Same public_key, different msg... Has to be the same sig for 'unlock'... But i do notice that this one i can see that they reuse hsh key so what happened if i can spam sending the same payload?"

This suggests the server might be **reusing the same nonce `k`** for multiple signatures, or there's a flaw in the nonce generation. The solve script only calls `sign_time` once then `verify` with the same signature — which wouldn't work for a different message.

Let me re-read the solve script more carefully:

```python
payload1 = {'option': 'sign_time'}
io.sendline(json.dumps(payload1).encode())
h = io.recvuntil(b"}").decode()
data = json.loads(h[h.find("{"):])
msg = data['msg']
r = data['r']
s = data['s']
payload2 = {'option': 'verify', 'msg': msg, 'r': r, 's': s}
io.sendline(json.dumps(payload2).encode())
```

It just verifies the **same message** it got from `sign_time`. That would return `true` but not the flag (flag requires `msg == "unlock"`).

The challenge might require a different approach — possibly the server has a bug where the nonce is predictable or reused. The `flow.md` mentions HNP (Hidden Number Problem) which applies when nonces are biased or partially known.

---

## Files

| File | Description |
|------|-------------|
| `source.py` | Challenge server logic (reconstructed) |
| `solve.py` | Partial solve script (fetches signature) |
| `flow.md` | Attack analysis / work-in-progress |
| `13381.py` | Alternate solve script (port-specific) |

---

## Current Understanding

**What we have:**
- Access to signing oracle for time-based messages
- Verification oracle that returns flag for `"unlock"` message
- ECDSA over NIST P-192 (`generator_192` from `ecdsa` library)
- Private key `d` unknown, order `n ≈ 2¹⁹²`

**What we need:**
- Valid ECDSA signature `(r, s)` on message `"unlock"`

**Possible attack vectors (to investigate):**
1. **Nonce reuse** — If `sign_time` uses deterministic/reused `k`, two signatures give `d`
2. **Nonce bias / HNP** — If `k` has known structure (e.g., low bits), lattice attack
3. **Time prediction** — If we can predict the exact time the server signs, we know the message hash
4. **Signature malleability** — `(r, s)` and `(r, -s mod n)` are both valid; not useful here
5. **Key recovery from multiple signatures** — If nonces are related (e.g., `k₂ = k₁ + c`)

---

## Next Steps (for solver)

1. Connect to the live server and collect many `(msg, r, s)` tuples from `sign_time`
2. Analyze nonces: compute `k = s⁻¹ * (H(m) + r*d) mod n` — but we don't know `d`
3. Check for nonce patterns: same `r` values? `r` values with known structure?
4. If `k` is small or has known MSB/LSB → Hidden Number Problem → lattice attack
5. If same `k` used twice → trivial key recovery: `d = (s₁ - s₂)⁻¹ * (H(m₁) - H(m₂)) mod n`

---

## References

- [Cryptohack - ProSign3](https://cryptohack.org/challenges/prosign3/)
- [Hidden Number Problem](https://eprint.iacr.org/1996/002.pdf)
- [ECDSA Nonce Reuse Attacks](https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/)
- [NIST P-192 Parameters](https://csrc.nist.gov/projects/digital-signature-standard)