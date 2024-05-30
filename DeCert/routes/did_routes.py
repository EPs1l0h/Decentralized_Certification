from flask import request, jsonify
from . import did_bp
from DeCert.scripts.get_did import register_did
from DeCert.scripts.verify_did import verify_did


@did_bp.route('/register', methods=['POST'])
def register_did_route():
    data = request.json
    account_name = data.get('account_name')
    context = data.get('context')
    version = data.get('version')
    public_key_pem = data.get('public_key_pem')
    type_of_key = data.get('type_of_key')
    add_proof_private_key_pem = data.get('add_proof_private_key_pem')

    if not all([account_name, context, version, public_key_pem, type_of_key, add_proof_private_key_pem]):
        return jsonify({"error": "Missing parameters"}), 400

    try:
        register_did(account_name, context, version, public_key_pem, type_of_key, add_proof_private_key_pem)
        return jsonify({"message": "DID registered successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@did_bp.route('/verify', methods=['POST'])
def verify_did_route():
    data = request.json
    did_document = data.get('did_document')

    if not did_document:
        return jsonify({"error": "Missing DID document"}), 400

    try:
        is_valid, message = verify_did(did_document)
        return jsonify({"is_valid": is_valid, "message": message}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
