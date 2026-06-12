<p align="center">
  <h1 align="center">pwgen</h1>
  <p align="center"><i>Secure password generator — random, memorable, and everything in between.</i></p>
  <p align="center">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/pwgen?style=flat">
    <img alt="Python" src="https://img.shields.io/pypi/pyversions/pwgen?style=flat">
    <img alt="License" src="https://img.shields.io/github/license/neocrev/pwgen?style=flat">
  </p>
</p>

```bash
pip install pwgen
```

## Usage

```bash
# Random 20-character password (default)
pwgen
# → K16]r_$bJlTu2QjTZI2n

# Memorable pronounceable password
pwgen --pronounceable --words 4 --caps
# → Xiwcaddis-Joxyos-Nupsismev-Kajyef

# 32-char alphanumeric with entropy display
pwgen --length 32 --no-symbols --entropy
# → e7eClt1tEvOoA72AOUfQPe3yGeWP6Amh  (191 bits)

# Generate 5 passwords at once
pwgen --count 5

# Numeric PIN code
pwgen --pin
# → 481230

# 4-digit PIN with entropy
pwgen --pin --pin-length 4 --entropy
# → 9865  (13 bits)
```

## Options

| Option | Description |
|--------|-------------|
| `--length`, `-l` | Password length (default: 20) |
| `--no-upper` | Exclude uppercase letters |
| `--no-lower` | Exclude lowercase letters |
| `--no-digits` | Exclude digits |
| `--no-symbols` | Exclude symbols |
| `--pronounceable`, `-p` | Generate memorable (CVC-based) password |
| `--words`, `-w` | Number of words for pronounceable (default: 3) |
| `--separator`, `-s` | Word separator (default: `-`) |
| `--caps`, `-c` | Capitalize each word |
| `--add-digit`, `-d` | Append a digit |
| `--pin` | Generate numeric PIN |
| `--pin-length` | PIN length (default: 6) |
| `--count`, `-n` | Number of passwords (default: 1) |
| `--entropy`, `-e` | Show entropy estimate in bits |
| `--json`, `-j` | Output as JSON array for scripting |
| `--clip` | Copy first password to clipboard |

## Security

pwgen uses `secrets` (Python's cryptographically secure random module). No passwords are logged, stored, or transmitted — everything happens locally.

## License

MIT
