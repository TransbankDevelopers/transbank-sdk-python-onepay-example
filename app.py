from flask import Flask, render_template, jsonify, request
from transbank import onepay
from transbank.onepay.cart import ShoppingCart, Item
from transbank.onepay.transaction import Transaction, Channel

app = Flask(__name__)

onepay.api_key = "dKVhq1WGt_XapIYirTXNyUKoWTDFfxaEV63-O5jcsdw"
onepay.shared_secret = "?XW#WOLG##FBAGEAYSNQ5APD#JF@$AYZ"
onepay.integration_type = onepay.IntegrationType.TEST
onepay.callback_url = "http://localhost:5000/api/commit"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transaction', methods=['GET', 'POST'])
def transaction():
    shopping_cart = ShoppingCart()
    shopping_cart.add(Item("Fresh Strawberries", 1, 36000))
    shopping_cart.add(Item("Lightweight Jacket", 1, 16000))
    
    result = Transaction.create(shopping_cart, Channel(request.form["channel"]))
    
    response = {"occ": result.occ, "ott": result.ott, "externalUniqueNumber": result.external_unique_number, "qrCodeAsBase64": result.qr_code_as_base64, "issuedAt": result.issued_at, "amount": shopping_cart.total}
    
    return jsonify(response)

@app.route('/api/commit', methods=['GET'])
def callback():
    response = Transaction.commit(request.args.get('occ'), request.args.get('externalUniqueNumber'))
    return response.transaction_desc
