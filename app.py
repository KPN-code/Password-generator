from flask import Flask, jsonify, render_template, request
import secrets
import string

app = Flask(__name__)

AMBIGUOUS = "{}[]()/\\'\"`~,;:.<>").
CONFUSING = "O0oIl1|"


def generate_password(length=16, use_lower=True, use_upper=True, use_digits=True, use_symbols=True, avoid_ambiguous=True):
    pools = []
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append("!@#$%^&*-_=+?" )

    if not pools:
        raise ValueError("Select at least one character set")

    # rakennus
    alphabet = "".join(pools)
    if avoid_ambiguous:
        # pois huonot
        for ch in AMBIGUOUS + CONFUSING:
            alphabet = alphabet.replace(ch, "")
        pools = ["".join([c for c in pool if c not in (AMBIGUOUS + CONFUSING)]) for pool in pools]

    # varmistus
    if length < len(pools):
        raise ValueError(f"Length must be at least {len(pools)} for the chosen options")

    # aloittaa yhdellä 
    password_chars = [secrets.choice(pool) for pool in pools]

    # lopun täyttö
    for _ in range(length - len(password_chars)):
        password_chars.append(secrets.choice(alphabet))

    # turvallinen sekoitus
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    try:
        data = request.get_json(force=True)
        length = int(data.get("length", 16))
        use_lower = bool(data.get("lower", True))
        use_upper = bool(data.get("upper", True))
        use_digits = bool(data.get("digits", True))
        use_symbols = bool(data.get("symbols", True))
        avoid_ambiguous = bool(data.get("avoidAmbiguous", True))

        pwd = generate_password(length, use_lower, use_upper, use_digits, use_symbols, avoid_ambiguous)
        return jsonify({"password": pwd}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
