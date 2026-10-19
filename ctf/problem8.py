from sage.all import *

hex_blocks = [
    "69cac604f3f6", "0037e3e277d0", "5bf4286560fd", 
    "7a78ae829dee", "1160d891335b", "660301648837",
    "7a8d796a70ab", "5c40bf50d20b", "788f5bae6242", 
    "3932ff60773e", "1d5a29213b82", "25aa4a80579b", 
    "465d1f5ae113", "3f268417e1bd", "751fb3515b44", "44a174ad7278"
]

key = [3, 1, 7] # from x=3, y=1, z=7

print("--- Testing Vigenere Decryption on Hex-to-ASCII strings ---")
full_message = []

for h in hex_blocks:
    # 1. Convert hex to bytes, then to ASCII string
    b = bytes.fromhex(h)
    text = b.decode('latin1', errors='ignore')
    
    # 2. Apply Vigenere inverse shift (subtracting key from character ordinals)
    decrypted_chars = []
    for idx, char in enumerate(text):
        shift = key[idx % len(key)]
        # Shift within printable/alphabet range or general byte range
        new_val = (ord(char) - shift) % 256
        decrypted_chars.append(chr(new_val))
    
    decoded_chunk = "".join(decrypted_chars)
    full_message.append(decoded_chunk)
    print(f"Hex: {h} -> Text: {decoded_chunk}")

print("\nCombined string:", "".join(full_message))