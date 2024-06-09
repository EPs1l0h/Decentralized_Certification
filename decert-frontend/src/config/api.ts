// src/config/api.ts
const API_BASE_URL = "http://127.0.0.1:5000"; // 根据实际情况修改

export default {
  register: `${API_BASE_URL}/register`,
  login: `${API_BASE_URL}/login`,
  getHolderInfo: `${API_BASE_URL}/get_holder_info`,
  requestAuthenticateDID: `${API_BASE_URL}/requestAuthenticateDID`,
  holderRequestVC: `${API_BASE_URL}/holderRequestVC`,
  getBeAskedVPList: `${API_BASE_URL}/getBeAskedVPList`,
  holderToVerifier: `${API_BASE_URL}/holderToVerifier`,
  recVerifyRequest: `${API_BASE_URL}/recVerifyRequest`,
  getVP: `${API_BASE_URL}/getVP`,
  checkVP: `${API_BASE_URL}/checkVP`,
  verifyVP: `${API_BASE_URL}/verifyVP`,
  askHolder: `${API_BASE_URL}/askHolder`,
  recDID: `${API_BASE_URL}/recDID`,
  getWhoRequestVerifyDID: `${API_BASE_URL}/getWhoRequestVerifyDID`,
  registerDID: `${API_BASE_URL}/registerDID`,
  reqeustVerifyDID: `${API_BASE_URL}/requestVerifyDID`,
  giveVCToHolder: `${API_BASE_URL}/giveVCToHolder`,
  checkUserName: `${API_BASE_URL}/checkUserName`,
};
