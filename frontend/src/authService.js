// frontend/src/authService.js
import { PublicClientApplication } from '@azure/msal-browser';
import { msalConfig, loginRequest, tokenRequest } from './authConfig';

export const msalInstance = new PublicClientApplication(msalConfig);

// Diese Funktion muss aufgerufen werden, bevor die App startet
export const initializeMsal = async () => {
  try {
    await msalInstance.initialize();
    const accounts = msalInstance.getAllAccounts();
    if (accounts.length > 0) {
      msalInstance.setActiveAccount(accounts[0]);
    }
  } catch (err) {
    console.error("MSAL-Initialisierung fehlgeschlagen:", err);
  }
};

export const login = async () => {
  try {
    const loginResponse = await msalInstance.loginPopup(loginRequest);
    msalInstance.setActiveAccount(loginResponse.account);
    return loginResponse.account;
  } catch (err) {
    console.error(err);
    return null;
  }
};

export const logout = () => {
  const account = msalInstance.getActiveAccount();
  msalInstance.logoutPopup({
    account: account,
    postLogoutRedirectUri: "/",
  });
};

export const getAccount = () => {
  return msalInstance.getActiveAccount();
};

export const acquireToken = async () => {
  const account = getAccount();
  if (!account) return null;

  try {
    const response = await msalInstance.acquireTokenSilent({
      ...tokenRequest, // <-- WICHTIGE ÄNDERUNG: Benutze tokenRequest statt loginRequest
      account: account,
    });
    return response.accessToken;
  } catch (error) {
    console.error('Silent token acquisition failed. Trying popup.', error);
    const response = await msalInstance.acquireTokenPopup(tokenRequest); // <-- Auch hier tokenRequest
    return response.accessToken;
  }
}
