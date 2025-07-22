// frontend/src/authConfig.js

// Lese die Konfiguration aus den Umgebungsvariablen, die Vite bereitstellt
const CLIENT_ID = import.meta.env.VITE_AZURE_CLIENT_ID;
const TENANT_ID = import.meta.env.VITE_AZURE_TENANT_ID;

export const msalConfig = {
  auth: {
    clientId: CLIENT_ID,
    authority: `https://login.microsoftonline.com/${TENANT_ID}`,
    redirectUri: "http://localhost:5173",
  },
  cache: {
    cacheLocation: import.meta.env.VITE_MSAL_CACHE || "sessionStorage",
    storeAuthStateInCookie: false,
  },
};

export const loginRequest = {
  scopes: ["User.Read"]
};

export const tokenRequest = {
  // Baue den Scope-String dynamisch mit der Client ID zusammen
  scopes: [`api://${CLIENT_ID}/access_as_user`]
};
