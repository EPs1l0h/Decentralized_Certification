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

        // Loop through the public keys and types of key to create verification methods
        for (uint i = 0; i < publicKeyPems.length; i++) {
            // Generate VerificationMethod ID using the current index
            string memory verificationMethodId = string(abi.encodePacked(did, "#key-", uintToString(i)));

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

    function uintToString(uint v) internal pure returns (string memory str) {
        uint maxlength = 100;
        bytes memory reversed = new bytes(maxlength);
        uint i = 0;
        while (v != 0) {
            uint remainder = v % 10;
            v = v / 10;
            reversed[i++] = bytes1(uint8(48 + remainder));
        }
        bytes memory s = new bytes(i);
        for (uint j = 0; j < i; j++) {
            s[j] = reversed[i - j - 1];
        }
        str = string(s);
    }
}
