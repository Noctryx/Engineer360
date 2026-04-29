window.ENGINEER360_API_BASE_URL = window.ENGINEER360_API_BASE_URL || "";

function getStoredApiBaseUrl() {
  const stored = localStorage.getItem("engineer360ApiBaseUrl");
  return stored ? stored.trim().replace(/\/$/, "") : "";
}

function getConfiguredApiBaseUrl() {
  const injected = window.ENGINEER360_API_BASE_URL;

  if (typeof injected === "string" && injected.trim()) {
    return injected.trim().replace(/\/$/, "");
  }

  return getStoredApiBaseUrl();
}

function setConfiguredApiBaseUrl(baseUrl) {
  const normalized = (baseUrl || "").trim().replace(/\/$/, "");

  if (normalized) {
    localStorage.setItem("engineer360ApiBaseUrl", normalized);
  } else {
    localStorage.removeItem("engineer360ApiBaseUrl");
  }

  return normalized;
}

function isRemoteFrontend() {
  return window.location.hostname.includes("github.io");
}

function ensureApiBaseUrl() {
  const configured = getConfiguredApiBaseUrl();

  if (configured) {
    return configured;
  }

  if (!isRemoteFrontend()) {
    return "";
  }

  const entered = window.prompt(
    "Enter the Engineer360 backend URL deployed on Replit.",
    "https://your-replit-app.replit.app",
  );

  return setConfiguredApiBaseUrl(entered || "");
}

function buildApiUrl(path) {
  const baseUrl = ensureApiBaseUrl();

  if (!baseUrl) {
    return path;
  }

  return `${baseUrl}${path}`;
}

async function engineer360Fetch(path, options = {}) {
  return fetch(buildApiUrl(path), options);
}
