cat > utils.py << 'EOF'
BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62_ALPHABET[0]

    result = ""
    base = len(BASE62_ALPHABET)

    while num > 0:
        num, remainder = divmod(num, base)
        result = BASE62_ALPHABET[remainder] + result

    return result
EOF