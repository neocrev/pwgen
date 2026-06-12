"""pwgen core — password generation and CLI."""

import argparse
import math
import random
import sys
import secrets

# ─── character pools ───

LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"

# Pronounceable components (CVC = consonant-vowel-consonant)
CONSONANTS = "bcdfghjklmnpqrstvwxyz"
VOWELS = "aeiou"


def estimate_entropy(length: int, pool_size: int) -> float:
    """Calculate entropy in bits."""
    if pool_size <= 0 or length <= 0:
        return 0.0
    return length * math.log2(pool_size)


def generate_random(length: int = 20, pools: list[str] | None = None) -> str:
    """Generate a cryptographically random password from given character pools."""
    if not pools or not any(pools):
        pools = [LOWERCASE, UPPERCASE, DIGITS, SYMBOLS]

    all_chars = "".join(pools)
    if not all_chars:
        return ""

    # Ensure at least one character from each pool
    password = [secrets.choice(pool) for pool in pools if pool]

    # Fill the rest randomly
    remaining = length - len(password)
    if remaining > 0:
        password.extend(secrets.choice(all_chars) for _ in range(remaining))

    # Shuffle to avoid predictable prefix
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def generate_pronounceable(words: int = 3, separator: str = "-",
                           capitalize: bool = False, add_digit: bool = False) -> str:
    """Generate a memorable pronounceable password (CVC words)."""
    result = []
    for _ in range(words):
        word = ""
        # Ensure reasonable length per word: 2-3 syllables
        syllables = random.randint(2, 3)
        for _ in range(syllables):
            word += secrets.choice(CONSONANTS)
            word += secrets.choice(VOWELS)
            word += secrets.choice(CONSONANTS)
        if capitalize:
            word = word.capitalize()
        result.append(word)

    password = separator.join(result)
    if add_digit:
        password += secrets.choice(DIGITS)
    return password


def main() -> int:
    parser = argparse.ArgumentParser(
        description="pwgen — secure password generator",
        epilog="Examples:\n"
               "  pwgen                    # 20-char random password\n"
               "  pwgen --length 32        # 32-char random password\n"
               "  pwgen --no-symbols       # alphanumeric only\n"
               "  pwgen --pronounceable    # memorable password\n"
               "  pwgen --words 4 --caps   # 4-word memorable with caps\n"
               "  pwgen --count 5          # generate 5 passwords",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Random password options
    parser.add_argument("--length", "-l", type=int, default=20,
                        help="Password length (default: 20)")
    parser.add_argument("--no-upper", action="store_true",
                        help="Exclude uppercase letters")
    parser.add_argument("--no-lower", action="store_true",
                        help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_true",
                        help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true",
                        help="Exclude symbols")

    # Pronounceable options
    parser.add_argument("--pronounceable", "-p", action="store_true",
                        help="Generate pronounceable password instead of random")
    parser.add_argument("--words", "-w", type=int, default=3,
                        help="Number of words for pronounceable (default: 3)")
    parser.add_argument("--separator", "-s", type=str, default="-",
                        help="Word separator for pronounceable (default: '-')")
    parser.add_argument("--caps", "-c", action="store_true",
                        help="Capitalize each word in pronounceable")
    parser.add_argument("--add-digit", "-d", action="store_true",
                        help="Append a digit to pronounceable password")

    # PIN options
    parser.add_argument("--pin", action="store_true",
                        help="Generate numeric PIN instead of password")
    parser.add_argument("--pin-length", type=int, default=6,
                        help="PIN length (default: 6)")

    # Output options
    parser.add_argument("--count", "-n", type=int, default=1,
                        help="Number of passwords to generate (default: 1)")
    parser.add_argument("--entropy", "-e", action="store_true",
                        help="Show entropy estimate for each password")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON array (for scripting)")
    parser.add_argument("--clip", action="store_true",
                        help="Copy first password to clipboard")

    args = parser.parse_args()

    passwords = []
    if args.pin:
        for i in range(args.count):
            pwd = "".join(secrets.choice(DIGITS) for _ in range(args.pin_length))
            passwords.append(pwd)
        entropy = estimate_entropy(args.pin_length, len(DIGITS))
    elif args.pronounceable:
        for i in range(args.count):
            pwd = generate_pronounceable(
                words=args.words,
                separator=args.separator,
                capitalize=args.caps,
                add_digit=args.add_digit,
            )
            passwords.append(pwd)
    else:
        pools = []
        if not args.no_lower:
            pools.append(LOWERCASE)
        if not args.no_upper:
            pools.append(UPPERCASE)
        if not args.no_digits:
            pools.append(DIGITS)
        if not args.no_symbols:
            pools.append(SYMBOLS)

        pool_size = sum(len(p) for p in pools)
        entropy = estimate_entropy(args.length, pool_size)

        for i in range(args.count):
            pwd = generate_random(length=args.length, pools=pools)
            passwords.append(pwd)

    if args.clip and passwords:
        try:
            import pyperclip
            pyperclip.copy(passwords[0])
            print(passwords[0], end="")
            print("  (copied!)")
            return 0
        except Exception:
            try:
                import subprocess
                p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
                p.communicate(passwords[0].encode())
                print(passwords[0], end="")
                print("  (copied!)")
                return 0
            except Exception:
                print("pwgen: --clip requires a clipboard tool (pip install pyperclip or apt install xclip)",
                      file=sys.stderr)
                sys.exit(1)

    if args.json:
        import json as j
        print(j.dumps(passwords))
    else:
        for i, pwd in enumerate(passwords, 1):
            if args.count > 1:
                label = f"{i}. {pwd}"
                if args.entropy:
                    label += f"  ({entropy:.0f} bits)" if args.entropy else ""
                print(label)
            else:
                if args.entropy:
                    print(f"{pwd}  ({entropy:.0f} bits)")
                else:
                    print(pwd)

    return 0


if __name__ == "__main__":
    sys.exit(main())
