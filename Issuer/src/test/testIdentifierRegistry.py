import requests
import json

# Flask服务器的URL
base_url = 'http://127.0.0.1:5000'

# 测试数据
register_data = {
    "username": "testuser",
    "password": "testpass"
}

verify_did_data = {
  "@context": ["buptBlockTrust"],
  "id": "did:bbt:123456789abcdefghi", 
  "created": "2022-01-01T00:00:00Z",
  "updated": "2022-01-10T10:00:00Z", 
  "version": "1", 
  "verificationMethod": [{
    "id": "did:bbt:123456789abcdefghi#key-1",
    "type": "SM2VerificationKey2022", 
    "publicKeyPem": "-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoEcz1UBgi0DQgAEYbBKJ5xqkUaxYOoJlKkZIb2rhoVw\nZbjmyF9BRmOiBdp5Jde3QswKjicjMccB299I2n5UgQKdU8nPAY69Qiv5/w==\n-----END PUBLIC KEY-----",
    "address": "0x4e0b15cAF28fD201A6ff5C17B3ff8227095462aA" 
  }],
  "proof": {
    "type": "SM2Signature", 
    "created": "2022-01-01T00:00:00Z",
    "proofPurpose": "assertionMethod", 
    "verificationMethod": "did:bbt:123456789abcdefghi#key-1", 
    "proofValue": "eyJhbGciOiJFUzI1NksiLCJraWQiOiJkaWQ6ZXhhbXBsZToxMjM0NTY3ODlhYmNkZWZnaGlfa2V5LTEiLCJ0eXAiOiJKV1MifQ..Q9JYDNOU0oyJkXW5NcC1hR3U4SHN6U1RiY3pvYkUzam5vY3VtY2tjZERxY3dLd1Z0a1d0Z2pUa0dWY3A0bFZJZw" 
  }
}

verify_vc_data = {
    "vc": "example_verifiable_credential"
}

verify_vp_data = {
    "vp": "example_verifiable_presentation"
}

# 注册请求
# response = requests.post(f"{base_url}/register", json=register_data)
# print("Register response:", response.json())

# verifyDID请求
response = requests.post(f"{base_url}/verifyDID", json=verify_did_data)
print("verifyDID response:", response.text)

# # verifyVC请求
# response = requests.post(f"{base_url}/verifyVC", json=verify_vc_data)
# print("verifyVC response:", response.json())

# # verifyVP请求
# response = requests.post(f"{base_url}/verifyVP", json=verify_vp_data)
# print("verifyVP response:", response.json())
