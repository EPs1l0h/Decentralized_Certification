// mock.ts
export const vcList = [
  {
    id: "1",
    type: ["VerifiableCredential", "UniversityDegreeCredential"],
    issuer: "did:example:beijing",
    issuanceDate: "2023-06-01T00:00:00Z",
    credentialSubject: {
      id: "did:example:student",
      degree: {
        type: "BachelorDegree",
        name: "计算机科学与技术",
      },
    },
  },
  {
    id: "2",
    type: ["VerifiableCredential", "SkillCertificateCredential"],
    issuer: "did:example:london",
    issuanceDate: "2023-06-02T00:00:00Z",
    credentialSubject: {
      id: "did:example:employee",
      certificate: {
        type: "SkillCertificate",
        name: "Java开发工程师",
      },
    },
  },
  {
    id: "3",
    type: ["VerifiableCredential", "MembershipCredential"],
    issuer: "did:example:seoul",
    issuanceDate: "2023-06-03T00:00:00Z",
    credentialSubject: {
      id: "did:example:member",
      membership: {
        type: "PremiumMembership",
        name: "优秀会员",
      },
    },
  },
];

export const vpRequestList = [
  {
    id: "1",
    verifier: "did:example:company",
    requestDate: "2023-06-04T00:00:00Z",
  },
  {
    id: "2",
    verifier: "did:example:government",
    requestDate: "2023-06-05T00:00:00Z",
  },
];
