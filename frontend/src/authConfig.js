// frontend/src/authConfig.js

// Ersetze diese Werte durch deine eigenen aus der neuen App-Registrierung
const CLIENT_ID = "168b7935-19c0-4a74-9df8-66f288175948";
const TENANT_ID = "3f27241d-d949-4cf1-a670-1c492efb689c";

export const msalConfig = {
  auth: {
    clientId: CLIENT_ID,
    authority: `https://login.microsoftonline.com/${TENANT_ID}`,
    redirectUri: "http://localhost:5173",
  },
  cache: {
    cacheLocation: "sessionStorage",
    storeAuthStateInCookie: false,
  },
};

export const loginRequest = {
  scopes: ["User.Read"]
};

export const tokenRequest = {
  scopes: ["api://168b7935-19c0-4a74-9df8-66f288175948/access_as_user"] // <-- 100% KORREKT HIER?
};
