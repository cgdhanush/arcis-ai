import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type DashboardData = {
  total_regulations: number;
  pending_maps: number;
  compliance_score: number;
  high_risk_alerts: number;
  department_compliance: Record<string, number>;
  map_status: Record<string, number>;
  risk_exposure: Record<string, number>;
};

type Regulation = {
  id: number;
  title: string;
  source: string;
  content: string;
  created_at: string;
};

type MapItem = {
  id: number;
  regulation_id: number;
  title: string;
  description: string;
  department: string;
  deadline: number;
  risk_level: string;
  priority_score: number;
  status: string;
  created_at: string;
};

type AuditRow = {
  id: number;
  timestamp: string;
  event: string;
  event_data: string;
  previous_hash: string;
  current_hash: string;
};

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
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [regulations, setRegulations] = useState<Regulation[]>([]);
  const [maps, setMaps] = useState<MapItem[]>([]);
  const [auditTrail, setAuditTrail] = useState<AuditRow[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (token) {
      api.defaults.headers.common.Authorization = `Bearer ${token}`;
      localStorage.setItem("arcis_token", token);
    }
  }, [token]);

  useEffect(() => {
    if (!token) return;

    async function load() {
      try {
        const [dashboardRes, regsRes, mapsRes, auditRes] = await Promise.all([
          api.get<DashboardData>("/dashboard"),
          api.get<Regulation[]>("/regulations"),
          api.get<MapItem[]>("/maps"),
          api.get<AuditRow[]>("/audit-log"),
        ]);
        setDashboard(dashboardRes.data);
        setRegulations(regsRes.data);
        setMaps(mapsRes.data);
        setAuditTrail(auditRes.data);
      } catch (err) {
        setError((err as Error).message);
      }
    }

    load();
  }, [token]);

  const departmentSeries = useMemo(
    () =>
      Object.entries(dashboard?.department_compliance ?? {}).map(
        ([name, value]) => ({
          name,
          value,
        }),
      ),
    [dashboard],
  );

  const statusSeries = useMemo(
    () =>
      Object.entries(dashboard?.map_status ?? {}).map(([name, value]) => ({
        name,
        value,
      })),
    [dashboard],
  );

  const exposureSeries = useMemo(
    () =>
      Object.entries(dashboard?.risk_exposure ?? {}).map(
        ([name, value], index) => ({
          name,
          value,
          fill: statusPalette[index % statusPalette.length],
        }),
      ),
    [dashboard],
  );

  async function handleLogin() {
    setError("");
    try {
      const response = await api.post("/auth/token", { username, role });
      setToken(response.data.access_token);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  if (!token) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
        <div className="w-full max-w-lg rounded-3xl border border-slate-700 bg-slate-900 p-8 shadow-2xl">
          <p className="text-sm uppercase tracking-[0.3em] text-blue-300">
            ARCIS
          </p>
          <h1 className="mt-3 text-3xl font-semibold">
            Compliance Command Center
          </h1>
          <p className="mt-2 text-slate-300">
            Sign in to review regulations, MAPs, evidence, and audit integrity.
          </p>
          <div className="mt-6 space-y-3">
            <input
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
            />
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            >
              <option value="compliance_officer">compliance_officer</option>
              <option value="department_owner">department_owner</option>
              <option value="management_viewer">management_viewer</option>
            </select>
            <button
              className="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold hover:bg-blue-500"
              onClick={handleLogin}
            >
              Enter Dashboard
            </button>
          </div>
          {error ? <p className="mt-4 text-sm text-red-300">{error}</p> : null}
        </div>
      </div>
    );
  }

  const mapStatusData = [
    { name: "Pending", value: dashboard?.map_status.Pending ?? 0 },
    { name: "Completed", value: dashboard?.map_status.Completed ?? 0 },
    { name: "Overdue", value: dashboard?.map_status.Overdue ?? 0 },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex">
        <aside className="hidden w-72 shrink-0 border-r border-slate-800 bg-slate-900/80 p-6 lg:block">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-blue-300">
              ARCIS
            </p>
            <h1 className="mt-2 text-2xl font-semibold">
              Enterprise Banking Platform
            </h1>
          </div>
          <nav className="mt-8 space-y-2">
            {navItems.map((item) => (
              <button
                key={item}
                className={`w-full rounded-xl px-4 py-3 text-left transition ${view === item ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-300 hover:bg-slate-700"}`}
                onClick={() => setView(item)}
              >
                {item}
              </button>
            ))}
          </nav>
        </aside>

        <main className="flex-1 p-6 lg:p-8">
          <header className="flex flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.3em] text-blue-300">
                Autonomous Regulatory Compliance Intelligence System
              </p>
              <h2 className="mt-2 text-3xl font-semibold">{view}</h2>
              <p className="mt-1 text-slate-400">
                Uploaded RBI circulars become measurable MAPs, tracked evidence,
                and auditable decisions.
              </p>
            </div>
            <button
              className="w-fit rounded-xl border border-slate-700 px-4 py-2 text-sm text-slate-300 hover:bg-slate-800"
              onClick={() => {
                localStorage.removeItem("arcis_token");
                setToken("");
              }}
            >
              Sign out
            </button>
          </header>

          {error ? (
            <p className="mt-4 rounded-xl border border-red-900 bg-red-950/60 px-4 py-3 text-red-200">
              {error}
            </p>
          ) : null}

          <section className="mt-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <Card
              title="Total Regulations"
              value={dashboard?.total_regulations ?? 0}
            />
            <Card title="Pending MAPs" value={dashboard?.pending_maps ?? 0} />
            <Card
              title="Compliance Score"
              value={Math.round((dashboard?.compliance_score ?? 0) * 100)}
              suffix="%"
            />
            <Card
              title="High Risk Alerts"
              value={dashboard?.high_risk_alerts ?? 0}
              tone="critical"
            />
          </section>

          <section className="mt-6 grid gap-6 xl:grid-cols-3">
            <ChartPanel title="Department Compliance" className="xl:col-span-1">
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={departmentSeries}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip />
                  <Bar dataKey="value" fill="#60a5fa" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </ChartPanel>

            <ChartPanel title="MAP Status" className="xl:col-span-1">
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie
                    data={mapStatusData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  >
                    {mapStatusData.map((entry, index) => (
                      <Cell
                        key={`status-${entry.name}`}
                        fill={statusPalette[index % statusPalette.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </ChartPanel>

            <ChartPanel title="Risk Exposure" className="xl:col-span-1">
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={exposureSeries}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                  <XAxis dataKey="name" stroke="#94a3b8" />
                  <YAxis stroke="#94a3b8" />
                  <Tooltip />
                  <Area
                    type="monotone"
                    dataKey="value"
                    stroke="#f97316"
                    fill="#fb923c"
                    fillOpacity={0.25}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </ChartPanel>
          </section>

          {view === "Regulations" ? (
            <DataPanel
              title="Regulations"
              rows={regulations.map((regulation) => [
                regulation.title,
                regulation.source,
                regulation.created_at,
              ])}
            />
          ) : null}

          {view === "MAP Management" ? (
            <DataPanel
              title="MAP Management"
              rows={maps.map((item) => [
                item.title,
                item.department,
                item.risk_level,
                item.status,
              ])}
            />
          ) : null}

          {view === "Evidence Validation" ? (
            <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-900 p-6">
              <h3 className="text-xl font-semibold">Evidence Validation</h3>
              <p className="mt-2 text-slate-400">
                Upload PDF, DOCX, or TXT evidence against MAP requirements and
                record the AI validation score.
              </p>
              <div className="mt-4 rounded-2xl border border-dashed border-slate-700 p-6 text-center text-slate-400">
                Evidence upload flow is connected in the backend via
                /upload-evidence and /validate-evidence.
              </div>
            </div>
          ) : null}

          {view === "Audit Trail" ? (
            <DataPanel
              title="Audit Trail"
              rows={auditTrail.map((row) => [
                row.timestamp,
                row.event,
                row.current_hash.slice(0, 16),
              ])}
            />
          ) : null}

          {view === "Dashboard" ? (
            <div className="mt-6 grid gap-6 xl:grid-cols-2">
              <DataPanel
                title="Recent Regulations"
                rows={regulations
                  .slice(0, 5)
                  .map((row) => [row.title, row.source, row.created_at])}
              />
              <DataPanel
                title="Recent MAPs"
                rows={maps
                  .slice(0, 5)
                  .map((row) => [
                    row.title,
                    row.department,
                    row.risk_level,
                    row.priority_score.toString(),
                  ])}
              />
            </div>
          ) : null}
        </main>
      </div>
    </div>
  );
}

function Card({
  title,
  value,
  suffix = "",
  tone = "default",
}: {
  title: string;
  value: number;
  suffix?: string;
  tone?: "default" | "critical";
}) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900 p-5 shadow-xl">
      <p className="text-sm text-slate-400">{title}</p>
      <div
        className={`mt-3 text-4xl font-semibold ${tone === "critical" ? "text-red-300" : "text-white"}`}
      >
        {value}
        {suffix}
      </div>
    </div>
  );
}

function ChartPanel({
  title,
  className,
  children,
}: {
  title: string;
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <div
      className={`rounded-3xl border border-slate-800 bg-slate-900 p-5 ${className ?? ""}`}
    >
      <h3 className="text-lg font-semibold">{title}</h3>
      <div className="mt-4">{children}</div>
    </div>
  );
}

function DataPanel({ title, rows }: { title: string; rows: string[][] }) {
  return (
    <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-900 p-6">
      <h3 className="text-lg font-semibold">{title}</h3>
      <div className="mt-4 overflow-hidden rounded-2xl border border-slate-800">
        <table className="min-w-full divide-y divide-slate-800 text-sm">
          <tbody className="divide-y divide-slate-800 bg-slate-950/40">
            {rows.map((row, index) => (
              <tr key={`${title}-${index}`}>
                {row.map((cell) => (
                  <td key={cell} className="px-4 py-3 text-slate-300">
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
