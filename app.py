# Tuodaan tarvittavat kirjastot
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from generator.password_generator import password_generator  # Tuodaan salasanojen generointifunktio omasta tiedostosta

# Luodaan Flask-sovellus
app = Flask(__name__)

# Sallitaan CORS eli pyynnöt front-endistä GitHub Pages käyttäjältä KPN-code
CORS(app, origins=["https://KPN-code.github.io"])

# Palautetaan front-endin index.html
@app.route("/")
def index():
    return render_template("index.html")

# Salasanan generointi JSON POST-pyynnöllä
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

        pwd = password_generator(
            length=length,
            use_lower=use_lower,
            use_upper=use_upper,
            use_digits=use_digits,
            use_symbols=use_symbols,
            avoid_ambiguous=avoid_ambiguous
        )
        return jsonify({"password": pwd}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Unexpected server error"}), 500

if __name__ == "__main__":
    # Lokaali testaus
    app.run(debug=True)
