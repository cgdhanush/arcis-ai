const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";
function getHeaders() {
    const token = localStorage.getItem("arcis_token");
    if (!token) {
        return {};
    }
    return { Authorization: `Bearer ${token}` };
}
export async function getJson(path) {
    const response = await fetch(`${API_BASE}${path}`, {
        headers: getHeaders(),
    });
    if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
    }
    return (await response.json());
}
export async function postJson(path, payload) {
    const response = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...getHeaders(),
        },
        body: JSON.stringify(payload),
    });
    if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
    }
    return (await response.json());
}
