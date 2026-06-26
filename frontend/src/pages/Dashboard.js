import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis, } from "recharts";
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1",
});
const navItems = [
    "Dashboard",
    "Regulations",
    "MAP Management",
    "Evidence Validation",
    "Audit Trail",
];
const statusPalette = ["#60a5fa", "#10b981", "#f59e0b", "#ef4444"];
export function Dashboard() {
    const [view, setView] = useState("Dashboard");
    const [token, setToken] = useState(localStorage.getItem("arcis_token") ?? "");
    const [username, setUsername] = useState("compliance.user");
    const [role, setRole] = useState("compliance_officer");
    const [dashboard, setDashboard] = useState(null);
    const [regulations, setRegulations] = useState([]);
    const [maps, setMaps] = useState([]);
    const [auditTrail, setAuditTrail] = useState([]);
    const [error, setError] = useState("");
    useEffect(() => {
        if (token) {
            api.defaults.headers.common.Authorization = `Bearer ${token}`;
            localStorage.setItem("arcis_token", token);
        }
    }, [token]);
    useEffect(() => {
        if (!token)
            return;
        async function load() {
            try {
                const [dashboardRes, regsRes, mapsRes, auditRes] = await Promise.all([
                    api.get("/dashboard"),
                    api.get("/regulations"),
                    api.get("/maps"),
                    api.get("/audit-log"),
                ]);
                setDashboard(dashboardRes.data);
                setRegulations(regsRes.data);
                setMaps(mapsRes.data);
                setAuditTrail(auditRes.data);
            }
            catch (err) {
                setError(err.message);
            }
        }
        load();
    }, [token]);
    const departmentSeries = useMemo(() => Object.entries(dashboard?.department_compliance ?? {}).map(([name, value]) => ({
        name,
        value,
    })), [dashboard]);
    const statusSeries = useMemo(() => Object.entries(dashboard?.map_status ?? {}).map(([name, value]) => ({
        name,
        value,
    })), [dashboard]);
    const exposureSeries = useMemo(() => Object.entries(dashboard?.risk_exposure ?? {}).map(([name, value], index) => ({
        name,
        value,
        fill: statusPalette[index % statusPalette.length],
    })), [dashboard]);
    async function handleLogin() {
        setError("");
        try {
            const response = await api.post("/auth/token", { username, role });
            setToken(response.data.access_token);
        }
        catch (err) {
            setError(err.message);
        }
    }
    if (!token) {
        return (_jsx("div", { className: "min-h-screen bg-slate-950 text-white flex items-center justify-center p-6", children: _jsxs("div", { className: "w-full max-w-lg rounded-3xl border border-slate-700 bg-slate-900 p-8 shadow-2xl", children: [_jsx("p", { className: "text-sm uppercase tracking-[0.3em] text-blue-300", children: "ARCIS" }), _jsx("h1", { className: "mt-3 text-3xl font-semibold", children: "Compliance Command Center" }), _jsx("p", { className: "mt-2 text-slate-300", children: "Sign in to review regulations, MAPs, evidence, and audit integrity." }), _jsxs("div", { className: "mt-6 space-y-3", children: [_jsx("input", { className: "w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3", value: username, onChange: (e) => setUsername(e.target.value), placeholder: "Username" }), _jsxs("select", { className: "w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3", value: role, onChange: (e) => setRole(e.target.value), children: [_jsx("option", { value: "compliance_officer", children: "compliance_officer" }), _jsx("option", { value: "department_owner", children: "department_owner" }), _jsx("option", { value: "management_viewer", children: "management_viewer" })] }), _jsx("button", { className: "w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold hover:bg-blue-500", onClick: handleLogin, children: "Enter Dashboard" })] }), error ? _jsx("p", { className: "mt-4 text-sm text-red-300", children: error }) : null] }) }));
    }
    const mapStatusData = [
        { name: "Pending", value: dashboard?.map_status.Pending ?? 0 },
        { name: "Completed", value: dashboard?.map_status.Completed ?? 0 },
        { name: "Overdue", value: dashboard?.map_status.Overdue ?? 0 },
    ];
    return (_jsx("div", { className: "min-h-screen bg-slate-950 text-slate-100", children: _jsxs("div", { className: "flex", children: [_jsxs("aside", { className: "hidden w-72 shrink-0 border-r border-slate-800 bg-slate-900/80 p-6 lg:block", children: [_jsxs("div", { children: [_jsx("p", { className: "text-xs uppercase tracking-[0.3em] text-blue-300", children: "ARCIS" }), _jsx("h1", { className: "mt-2 text-2xl font-semibold", children: "Enterprise Banking Platform" })] }), _jsx("nav", { className: "mt-8 space-y-2", children: navItems.map((item) => (_jsx("button", { className: `w-full rounded-xl px-4 py-3 text-left transition ${view === item ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-300 hover:bg-slate-700"}`, onClick: () => setView(item), children: item }, item))) })] }), _jsxs("main", { className: "flex-1 p-6 lg:p-8", children: [_jsxs("header", { className: "flex flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl lg:flex-row lg:items-center lg:justify-between", children: [_jsxs("div", { children: [_jsx("p", { className: "text-sm uppercase tracking-[0.3em] text-blue-300", children: "Autonomous Regulatory Compliance Intelligence System" }), _jsx("h2", { className: "mt-2 text-3xl font-semibold", children: view }), _jsx("p", { className: "mt-1 text-slate-400", children: "Uploaded RBI circulars become measurable MAPs, tracked evidence, and auditable decisions." })] }), _jsx("button", { className: "w-fit rounded-xl border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800", onClick: () => {
                                        localStorage.removeItem("arcis_token");
                                        setToken("");
                                    }, children: "Sign out" })] }), error ? (_jsx("p", { className: "mt-4 rounded-xl border border-red-900 bg-red-950/60 px-4 py-3 text-red-200", children: error })) : null, _jsxs("section", { className: "mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4", children: [_jsx(Card, { title: "Total Regulations", value: dashboard?.total_regulations ?? 0 }), _jsx(Card, { title: "Pending MAPs", value: dashboard?.pending_maps ?? 0 }), _jsx(Card, { title: "Compliance Score", value: Math.round((dashboard?.compliance_score ?? 0) * 100), suffix: "%" }), _jsx(Card, { title: "High Risk Alerts", value: dashboard?.high_risk_alerts ?? 0, tone: "critical" })] }), _jsxs("section", { className: "mt-6 grid gap-6 xl:grid-cols-3", children: [_jsx(ChartPanel, { title: "Department Compliance", className: "xl:col-span-1", children: _jsx(ResponsiveContainer, { width: "100%", height: 280, children: _jsxs(BarChart, { data: departmentSeries, children: [_jsx(CartesianGrid, { strokeDasharray: "3 3", stroke: "#1f2937" }), _jsx(XAxis, { dataKey: "name", stroke: "#94a3b8" }), _jsx(YAxis, { stroke: "#94a3b8" }), _jsx(Tooltip, {}), _jsx(Bar, { dataKey: "value", fill: "#60a5fa", radius: [8, 8, 0, 0] })] }) }) }), _jsx(ChartPanel, { title: "MAP Status", className: "xl:col-span-1", children: _jsx(ResponsiveContainer, { width: "100%", height: 280, children: _jsxs(PieChart, { children: [_jsx(Pie, { data: mapStatusData, dataKey: "value", nameKey: "name", cx: "50%", cy: "50%", outerRadius: 100, label: true, children: mapStatusData.map((entry, index) => (_jsx(Cell, { fill: statusPalette[index % statusPalette.length] }, `status-${entry.name}`))) }), _jsx(Tooltip, {})] }) }) }), _jsx(ChartPanel, { title: "Risk Exposure", className: "xl:col-span-1", children: _jsx(ResponsiveContainer, { width: "100%", height: 280, children: _jsxs(AreaChart, { data: exposureSeries, children: [_jsx(CartesianGrid, { strokeDasharray: "3 3", stroke: "#1f2937" }), _jsx(XAxis, { dataKey: "name", stroke: "#94a3b8" }), _jsx(YAxis, { stroke: "#94a3b8" }), _jsx(Tooltip, {}), _jsx(Area, { type: "monotone", dataKey: "value", stroke: "#f97316", fill: "#fb923c", fillOpacity: 0.25 })] }) }) })] }), view === "Regulations" ? (_jsx(DataPanel, { title: "Regulations", rows: regulations.map((regulation) => [
                                regulation.title,
                                regulation.source,
                                regulation.created_at,
                            ]) })) : null, view === "MAP Management" ? (_jsx(DataPanel, { title: "MAP Management", rows: maps.map((item) => [
                                item.title,
                                item.department,
                                item.risk_level,
                                item.status,
                            ]) })) : null, view === "Evidence Validation" ? (_jsxs("div", { className: "mt-6 rounded-3xl border border-slate-800 bg-slate-900 p-6", children: [_jsx("h3", { className: "text-xl font-semibold", children: "Evidence Validation" }), _jsx("p", { className: "mt-2 text-slate-400", children: "Upload PDF, DOCX, or TXT evidence against MAP requirements and record the AI validation score." }), _jsx("div", { className: "mt-4 rounded-2xl border border-dashed border-slate-700 p-6 text-center text-slate-400", children: "Evidence upload flow is connected in the backend via /upload-evidence and /validate-evidence." })] })) : null, view === "Audit Trail" ? (_jsx(DataPanel, { title: "Audit Trail", rows: auditTrail.map((row) => [
                                row.timestamp,
                                row.event,
                                row.current_hash.slice(0, 16),
                            ]) })) : null, view === "Dashboard" ? (_jsxs("div", { className: "mt-6 grid gap-6 xl:grid-cols-2", children: [_jsx(DataPanel, { title: "Recent Regulations", rows: regulations
                                        .slice(0, 5)
                                        .map((row) => [row.title, row.source, row.created_at]) }), _jsx(DataPanel, { title: "Recent MAPs", rows: maps
                                        .slice(0, 5)
                                        .map((row) => [
                                        row.title,
                                        row.department,
                                        row.risk_level,
                                        row.priority_score.toString(),
                                    ]) })] })) : null] })] }) }));
}
function Card({ title, value, suffix = "", tone = "default", }) {
    return (_jsxs("div", { className: "rounded-3xl border border-slate-800 bg-slate-900 p-5 shadow-xl", children: [_jsx("p", { className: "text-sm text-slate-400", children: title }), _jsxs("div", { className: `mt-3 text-4xl font-semibold ${tone === "critical" ? "text-red-300" : "text-white"}`, children: [value, suffix] })] }));
}
function ChartPanel({ title, className, children, }) {
    return (_jsxs("div", { className: `rounded-3xl border border-slate-800 bg-slate-900 p-5 ${className ?? ""}`, children: [_jsx("h3", { className: "text-lg font-semibold", children: title }), _jsx("div", { className: "mt-4", children: children })] }));
}
function DataPanel({ title, rows }) {
    return (_jsxs("div", { className: "mt-6 rounded-3xl border border-slate-800 bg-slate-900 p-6", children: [_jsx("h3", { className: "text-lg font-semibold", children: title }), _jsx("div", { className: "mt-4 overflow-hidden rounded-2xl border border-slate-800", children: _jsx("table", { className: "min-w-full divide-y divide-slate-800 text-sm", children: _jsx("tbody", { className: "divide-y divide-slate-800 bg-slate-950/40", children: rows.map((row, index) => (_jsx("tr", { children: row.map((cell) => (_jsx("td", { className: "px-4 py-3 text-slate-300", children: cell }, cell))) }, `${title}-${index}`))) }) }) })] }));
}
