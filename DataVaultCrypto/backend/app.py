from flask import Flask, render_template, request, jsonify
from backend.cryptoUtils import cryptoUtils  # On garde le nom de ta classe
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Chemin de `backend/`
TEMPLATE_DIR = os.path.join(BASE_DIR, "../frontend/templates")  # Aller dans `frontend/templates`
STATIC_DIR = os.path.join(BASE_DIR, "../frontend/static")  # Aller dans `frontend/static`

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)



crypto = cryptoUtils()
PRIVATE_KEY_PATH = "private_key.pem"
PUBLIC_KEY_PATH = "public_key.pem"

if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
    crypto.loadKeys(PRIVATE_KEY_PATH, PUBLIC_KEY_PATH)
    print("Clés existantes chargées automatiquement.")
else:
    print("Aucune clé trouvée. Vous devez les générer.")



@app.route("/")
def index():
    return render_template("index.html") 



@app.route("/generate_keys", methods=["POST"])
def generate_keys():
    crypto.generatekeys()
    return jsonify({"message": "Clés générées avec succès !"})


@app.route("/load_keys", methods=["POST"])
def load_keys():
    data = request.json
    private_path = data.get("private_path")
    public_path = data.get("public_path")

    if not private_path or not public_path:
        return jsonify({"error": "Veuillez spécifier les chemins des fichiers."}), 400

    message = crypto.loadKeys(private_path, public_path)
    return jsonify({"message": "Clés chargées avec succès !"})

@app.route("/encrypt", methods=["POST"])
def encrypt():
    data = request.json.get("content", "")
    if data == "":
        return jsonify({"error": "Aucune donnée à chiffrer"}), 400
    encrypted_data = crypto.encryptData(data)

    if encrypted_data:
        return jsonify({"encrypted_data": encrypted_data.hex()})
    else:
        return jsonify({"error": "Erreur de chiffrement"}), 500

@app.route("/decrypt", methods=["POST"])
def decrypt():
    try:
        encrypted_data = bytes.fromhex(request.json.get("content", ""))
        decrypted_data = crypto.decryptData(encrypted_data)

        if decrypted_data:
            return jsonify({"decrypted_data": decrypted_data})
        else:
            return jsonify({"error": "Erreur de déchiffrement"}), 500

    except Exception as e:
        return jsonify({"error": f"Erreur serveur : {e}"}), 500