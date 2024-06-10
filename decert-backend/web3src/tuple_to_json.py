import json

def did_document_to_json(data):
    # 构建verificationMethods的JSON结构
    verification_methods = [
        {
            "id": method[0],
            "type": method[1],
            "publicKeyPem": method[2],
            "address": method[3]
        }
        for method in data[5]
    ]

    # 构建JSON结构
    json_data = {
        "@context": [data[0]],
        "id": data[1],
        "created": data[2],
        "updated": data[3],
        "version": data[4],
        "verificationMethod": verification_methods,
        "proof": {
            "type": data[6][0],
            "created": data[6][1],
            "proofPurpose": data[6][2],
            "verificationMethod": data[6][3],
            "proofValue": data[6][4]
        }
    }
    return json_data
