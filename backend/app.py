from flask import Flask, request, jsonify
from flask_cors import CORS
import your_existing_logic  # import your fetch/score functions

app = Flask(__name__)
CORS(app)  # allow React frontend to call backend

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    portfolio = your_existing_logic.generate_portfolio(data)
    return jsonify(portfolio)

if __name__ == "__main__":
    app.run(debug=True)
