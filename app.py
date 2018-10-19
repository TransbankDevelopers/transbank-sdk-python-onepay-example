import os

from flask import Flask, render_template, jsonify, request
from transbank import onepay
from transbank.onepay.cart import ShoppingCart, Item
from transbank.onepay.transaction import Transaction, Channel
from transbank.onepay.refund import Refund

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transaction/create', methods=['GET', 'POST'])
def transaction():
    onepay.callback_url = request.url_root + "transaction/commit"

    shopping_cart = ShoppingCart()
    shopping_cart.add(Item("Fresh Strawberries", 1, 36000))
    shopping_cart.add(Item("Lightweight Jacket", 1, 16000))
    
    channel = Channel(request.form.get("channel")) if request.form.get("channel") else None

    result = Transaction.create(shopping_cart, channel)
    
    response = {"occ": result.occ, "ott": result.ott, "externalUniqueNumber": result.external_unique_number, "qrCodeAsBase64": result.qr_code_as_base64, "issuedAt": result.issued_at, "amount": shopping_cart.total}
    
    return jsonify(response)

@app.route('/transaction/commit', methods=['GET'])
def callback():
    status = request.args.get('status')
    occ = request.args.get('occ')
    external_unique_number = request.args.get('externalUniqueNumber')

    if (status and status != "PRE_AUTHORIZED"):
        return render_template('commit-error.html', occ=occ, external_unique_number=external_unique_number, status=status)

    response = Transaction.commit(occ, external_unique_number)
    return render_template('commit.html', response=response, external_unique_number=external_unique_number)

@app.route('/transaction/refund', methods=['GET'])
def refund():
    amount = request.args.get('amount')
    occ = request.args.get('occ')
    external_unique_number = request.args.get('externalUniqueNumber')
    authorization_code = request.args.get('authorizationCode')

    response = Refund.create(amount, occ, external_unique_number, authorization_code)
    return render_template('refund.html', response=response)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
