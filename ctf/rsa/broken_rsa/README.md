# Broken RSA (RSA) — Cryptohack

**Category:** Small Exponent Attack (`e = 16`)  
**Difficulty:** Medium

---

## Challenge Overview

Standard RSA encryption with a **very small public exponent** `e = 16`. Given:
- Modulus `n` (1024-bit)
- Public exponent `e = 16`
- Ciphertext `ct`

The flag is encrypted as `ct = m^e mod n`. With `e = 16`, several attacks are possible.

---

## Vulnerability

**Small exponent `e = 16`** enables multiple attack vectors:

### 1. **Direct `e`-th root (if `m^e < n`)**
If the message is small enough that `m^16 < n`, then `ct = m^16` (no modular reduction) and `m = ⌊ct^(1/16)⌋`.

### 2. **Coppersmith's Attack (small message / known padding)**
If the message has known structure (e.g., `m = flag || padding`), we can find small roots of `f(x) = (padding + x)^e - ct ≡ 0 (mod n)`.

### 3. **Franklin-Reiter Related Message Attack**
If multiple ciphertexts of related messages exist (not applicable here — single ciphertext).

### 4. **Håstad's Broadcast Attack**
Requires `e` ciphertexts under different moduli (not applicable).

### 5. **Partial Key Exposure / Lattice Attacks**
If padding is known (e.g., PKCS#1 v1.5), Coppersmith's method on `f(x) = (B + x)^e - ct`.

---

## Attack Flow (Most Likely)

Given a single ciphertext with `e = 16`, the most practical approach:

1. **Check direct root**: Compute `m = ⌊ct^(1/16)⌋`, verify `m^16 ≡ ct (mod n)`
2. **If padding known** (e.g., `flag` format `crypto{...}`): Use Coppersmith to find small root
3. **If message < n^(1/e)**: Direct root works

For a 1024-bit `n`, `n^(1/16) ≈ 2^64`. If the flag is ~50 bytes (400 bits), `m^16` would be ~6400 bits >> 1024 bits, so modular reduction occurs.

But the flag format `crypto{...}` is known. We can model:
```
m = known_prefix || unknown || known_suffix
```
Or if the message is just the flag bytes as integer, and flag is ~40 bytes (320 bits), then `m^16` is 5120 bits > 1024 bits.

**Wait** — the flag might be short enough? `crypto{...}` is ~20-30 chars. As integer: ~160-240 bits. `m^16` = 2560-3840 bits > 1024 bits. So modular reduction happens.

**Alternative**: The message might be padded. If padding is known (e.g., `00 02 [random] 00 [flag]`), Coppersmith applies.

But looking at the solve.py in the repo — it's empty (just imports and constants). So we need to determine the actual attack.

---

## Files

| File | Description |
|------|-------------|
| `brokenRSA.txt` | Challenge parameters: `n`, `e=16`, `ct` |
| `solve.py` | Placeholder (constants only) |

---

## Parameters

```
n = 27772857409875257529415990911214211975844307184430241451899407838750503024323367895540981606586709985980003435082116995888017731426634845808624796292507989171497629109450825818587383112280639037484593490692935998202437639626747133650990603333094513531505209954273004473567193235535061942991750932725808679249964667090723480397916715320876867803719301313440005075056481203859010490836599717523664197112053206745235908610484907715210436413015546671034478367679465233737115549451849810421017181842615880836253875862101545582922437858358265964489786463923280312860843031914516061327752183283528015684588796400861331354873

e = 16

ct = 11303174761894431146735697569489134747234975144162172162401674567273034831391936916397234068346115459134602443963604063679379285919302225719050193590179240191429612072131629779948379821039610415099784351073443218911356328815458050694493726951231241096695626477586428880220528001269746547018741237131741255022371957489462380305100634600499204435763201371188769446054925748151987175656677342779043435047048130599123081581036362712208692748034620245590448762406543804069935873123161582756799517226666835316588896306926659321054276507714414876684738121421124177324568084533020088172040422767194971217814466953837590498718
```

---

## Solution Approach (Coppersmith)

```python
from sage.all import *
from Crypto.Util.number import long_to_bytes

n = Integer(...)  # from brokenRSA.txt
e = 16
ct = Integer(...)

# Assume flag format: crypto{...} -> known prefix/suffix
# Model: m = flag_int (raw bytes as integer)
# Try direct root first
m_candidate = Integer(ct).nth_root(e, truncate_mode=True)
if pow(m_candidate, e, n) == ct:
    print("Direct root works:", long_to_bytes(m_candidate))
else:
    print("Need Coppersmith / padding oracle")

# If direct root fails, try Coppersmith with known flag format
# PR.<x> = PolynomialRing(Zmod(n))
# f = (known_prefix + x)^e - ct
# small_roots = f.small_roots(X=2^bits, beta=1.0)
```

---

## Why `e = 16` is Broken

| Exponent | Security | Notes |
|----------|----------|-------|
| `e = 3` | Broken | Håstad broadcast (3 ct), Coppersmith (small m) |
| `e = 5` | Weak | Similar attacks |
| `e = 16` | **Very weak** | `e` not coprime to `φ(n)` usually; `gcd(e, φ(n)) = 1` required for valid RSA — but `e=16` is even, so `φ(n)` must be odd ⇒ `p, q` both even? **Impossible**. Wait... |
| `e = 65537` | Standard | Secure |

**Critical observation**: For RSA, `gcd(e, φ(n)) = 1` is required. `φ(n) = (p-1)(q-1)` is always even (since `p, q` are odd primes). But `e = 16` is even ⇒ `gcd(16, φ(n)) ≥ 2`. **This RSA key is mathematically invalid!**

Unless... the challenge uses a non-standard variant, or `n` is not a product of two primes, or `e` is not actually the encryption exponent.

Wait — maybe `e = 16` is used with a different scheme? Or the challenge is about the fact that `e` is not coprime to `φ(n)`, making decryption ambiguous?

If `gcd(e, φ(n)) = g > 1`, then `m^e mod n` is not injective — multiple messages map to same ciphertext. But the challenge says "broken RSA" — maybe we exploit this?

Actually, if `gcd(e, φ(n)) = 2^k`, then `m^(e/2^k)` might be recoverable? Or the encryption is `ct = m^e mod n` but decryption is impossible — so the challenge might be to find **any** `m` such that `m^e ≡ ct (mod n)`, which is an `e`-th root modulo `n`.

Computing `e`-th roots modulo composite `n` is equivalent to factoring `n` (in general). But with `e = 16 = 2^4`, we can compute **square roots** iteratively:
1. Find `x` such that `x^2 ≡ ct (mod n)` (4 square roots)
2. Find `y` such that `y^2 ≡ x (mod n)` (16 candidates)
3. Find `z` such that `z^2 ≡ y (mod n)` (64 candidates)
4. Find `w` such that `w^2 ≡ z (mod n)` (256 candidates)

One of the 256 candidates is the flag. This requires factoring `n` to compute square roots mod `n`, or the factors might be smooth/small.

**But wait** — if we can factor `n`, we can just compute `d = e⁻¹ mod φ(n)` (but `e` not coprime to `φ(n)` so inverse doesn't exist).

Let me check if `n` is factorable... 1024-bit `n` is not trivially factorable.

**Alternative interpretation**: Maybe the challenge uses `e = 16` with a **known padding scheme** where Coppersmith applies. Or the flag is small enough that `m^16 < n` after all?

Let me estimate: `n ≈ 2^1023`. `n^(1/16) ≈ 2^63.9`. So if `m < 2^64`, direct root works. A 64-bit integer is 8 bytes. `crypto{...}` is at least 8 bytes (`crypto{}` = 8 bytes). If flag is exactly `crypto{}`, it fits. But real flags are longer.

Maybe the message is not the flag directly but a **session key** (16 bytes = 128 bits > 64 bits). Hmm.

---

## References

- [Cryptohack - Broken RSA](https://cryptohack.org/challenges/broken_rsa/)
- **Coppersmith, D.** "Small solutions to polynomial equations, and low exponent RSA vulnerabilities." *J. Cryptology* 10 (1997): 233–260.
- [RSA with Small Exponent](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf)
- [e-th Root Attack](https://en.wikipedia.org/wiki/RSA_problem#Small_encryption_exponent)