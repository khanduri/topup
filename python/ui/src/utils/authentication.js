// import API from "./xhr";

// rename PROJECT_SKELETON_ to your custom project

function _getFromStorage(key) {
  return localStorage.getItem("PROJECT_SKELETON_" + key);
}

function _setToStorage(key, data) {
  localStorage.setItem("PROJECT_SKELETON_" + key, data);
}

function _removeFromStorage(key) {
  localStorage.removeItem("PROJECT_SKELETON_" + key);
}

export function hasStoredToken() {
  return !!_getFromStorage("token");
}

export function getStoredToken() {
  return _getFromStorage("token");
}

export function saveToken(token) {
  _setToStorage("token", token);
  // API.defaults.headers["Authorization"] = "Bearer " + token;
}

export function deleteToken() {
  _removeFromStorage("token");
  clearLoginMeta();
}

export function saveLoginMeta(meta) {
  _setToStorage("user_xid", meta.user_xid);
}

export function clearLoginMeta(meta) {
  _removeFromStorage("user_xid");
}

export function getUserId() {
  return _getFromStorage("user_xid") || "NO_USER_SET";
}
