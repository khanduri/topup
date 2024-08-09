import axios from "axios";

import { getStoredToken, deleteToken } from "utils/authentication";

// export const BASE_URL = "http://localhost:5000";
export const BASE_URL = process.env.REACT_APP_API_DOMAIN;

let API = generateAPIInstance(getStoredToken());
function generateAPIInstance(jwt_token) {
  let instance = axios.create({
    baseURL: process.env.REACT_APP_API_DOMAIN + "/api/v1",
    // baseURL: "http://divshow-api.bytebeacon.com" + "/api/v1",
    headers: {
      Authorization: "Bearer " + jwt_token,
    },
  });
  return instance;
}

export function handleError(error, history) {
  if (error.response === undefined) {
    console.log("Something went wrong! Error response came back undefined.");
    console.log(error);
    return;
  }

  const status_code = error.response.status;
  if (status_code === 401) {
    alert("Login Expired! Please login again.");
    deleteToken();
    history.push("/");
  } else if (status_code === 500) {
    console.log(error.response);
    alert(error.response.data.data.message);
  } else {
    console.log(error.response);
    alert(error.response.data.data.message);
  }
}

// export function handleError(error, history, from_location, alert_error){
//   if (error.response === undefined){
//     console.log("Something went wrong! Error response came back undefined.");
//     console.log(error);
//     return;
//   }

//   const status_code = error.response.status;
//   if (status_code === 401){
//     deleteToken();
//     if (from_location !== undefined){
//       const query = { dest: from_location};
//       const searchString = qs.stringify(query);
//       const login_url = "/login?" + searchString;
//       history.push(login_url);
//     } else {
//       history.push('/login');
//     }

//   } else if (status_code === 403){
//     deleteToken();
//     alert(error.response.data.data.message);
//     if (from_location !== undefined){
//       const query = { dest: from_location};
//       const searchString = qs.stringify(query);
//       const login_url = "/login?" + searchString;
//       history.push(login_url);
//     } else {
//       history.push('/login');
//     }

//   } else if (status_code === 500){
//     console.log(error.response);
//     Track.exception(true, error.response.data.data.message);
//     if (alert_error === undefined || alert_error){
//       alert(error.response.data.data.message);
//     }

//   } else {
//     console.log(error.response);
//     Track.exception(false, error.response.data.data.message);
//     alert(error.response.data.data.message);
//     // window.location.reload();
//   }
// }

export default API;
