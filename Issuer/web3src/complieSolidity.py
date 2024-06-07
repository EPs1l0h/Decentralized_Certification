import solcx
import json

# 安装指定版本的solc编译器
solcx.install_solc('0.8.0')
solcx.set_solc_version('0.8.0')
# 读取Solidity代码
contract_source_code = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DIDRegistry {
    struct VerificationMethod {
        string id;
        string typeOfKey;
        string publicKeyPem;
        address addr; // Address derived from the public key
    }

    struct Proof {
        string typeOfProof;
        string created;
        string proofPurpose;
        string verificationMethod;
        string proofValue;
    }

    struct DIDDocument {
        string context;
        string id;
        string created;
        string updated;
        string version;
        VerificationMethod[] verificationMethods;
        Proof proof;
    }

    mapping(string => DIDDocument) private didDocuments;
    mapping(address => string) private addressToDID;

    event DIDCreated(string did, address owner);
    function generateDID(
        string memory context,
        string memory created,
        string memory updated,
        string memory version,
        string[] memory publicKeyPems,
        string[] memory typesOfKey
    ) public returns (string memory) {
        require(bytes(addressToDID[msg.sender]).length == 0, "DID already exists for this address");
        require(publicKeyPems.length == typesOfKey.length, "Public keys and types of key arrays must have the same length");

        // Generate a unique DID
        string memory did = string(abi.encodePacked("did:dc:", toAsciiString(msg.sender)));

        // Create DID Document
        DIDDocument storage didDocument = didDocuments[did];
        didDocument.context = context;
        didDocument.id = did;
        didDocument.created = created;
        didDocument.updated = updated;
        didDocument.version = version;
        string[] memory key_id = new string[](10);
        key_id[0] = '1';
        key_id[1] = '2';
        key_id[2] = '3';
        key_id[3] = '4';
        key_id[4] = '5';
        key_id[5] = '6';
        key_id[6] = '7';
        key_id[7] = '8';
        key_id[8] = '9';
        key_id[9] = '10';
        // Loop through the public keys and types of key to create verification methods
        for (uint i = 0; i < publicKeyPems.length; i++) {
            // Generate VerificationMethod ID using the current index
            string memory verificationMethodId = string(abi.encodePacked(did, "#key-", key_id[i]));
            // Create VerificationMethod
            VerificationMethod memory verificationMethod = VerificationMethod({
                id: verificationMethodId,
                typeOfKey: typesOfKey[i],
                publicKeyPem: publicKeyPems[i],
                addr: msg.sender
            });

            // Add the verification method to the DID Document
            didDocument.verificationMethods.push(verificationMethod);
        }

        // Create Proof (initially empty, can be updated later)
        Proof memory proof = Proof({
            typeOfProof: "",
            created: "",
            proofPurpose: "",
            verificationMethod: "",
            proofValue: ""
        });

        didDocument.proof = proof;

        // Map address to DID
        addressToDID[msg.sender] = did;

        emit DIDCreated(did, msg.sender);

        return did;
    }

    function getDIDDocument(string memory did) public view returns (DIDDocument memory) {
        return didDocuments[did];
    }

    function addProof(
        string memory did,
        string memory typeOfProof,
        string memory created,
        string memory proofPurpose,
        string memory verificationMethod,
        string memory proofValue
    ) public {
        require(keccak256(abi.encodePacked(didDocuments[did].id)) == keccak256(abi.encodePacked(did)), "DID does not exist");

        DIDDocument storage didDocument = didDocuments[did];
        didDocument.proof = Proof({
            typeOfProof: typeOfProof,
            created: created,
            proofPurpose: proofPurpose,
            verificationMethod: verificationMethod,
            proofValue: proofValue
        });
    }

    function toAsciiString(address x) internal pure returns (string memory) {
        bytes memory s = new bytes(40);
        for (uint i = 0; i < 20; i++) {
            bytes1 b = bytes1(uint8(uint(uint160(x)) / (2**(8*(19 - i)))));
            bytes1 hi = bytes1(uint8(b) / 16);
            bytes1 lo = bytes1(uint8(b) - 16 * uint8(hi));
            s[2*i] = char(hi);
            s[2*i+1] = char(lo);
        }
        return string(s);
    }

    function char(bytes1 b) internal pure returns (bytes1 c) {
        if (uint8(b) < 10) return bytes1(uint8(b) + 0x30);
        else return bytes1(uint8(b) + 0x57);
    }
}
'''

# 编译Solidity代码
compiled_sol = solcx.compile_source(contract_source_code, output_values=['abi', 'bin'])

# 提取合约接口和字节码
contract_interface = compiled_sol['<stdin>:DIDRegistry']
abi = contract_interface['abi']
bytecode = contract_interface['bin']

# 将ABI和字节码保存到文件
with open('DIDRegistry_abi.json', 'w') as abi_file:
    json.dump(abi, abi_file)

with open('DIDRegistry_bytecode.txt', 'w') as bytecode_file:
    bytecode_file.write(bytecode)

print("ABI and Bytecode have been saved to DIDRegistry_abi.json and DIDRegistry_bytecode.txt")
