import { useState } from "react";
import { Search, Filter, CheckCircle, AlertCircle, Info, Clock } from "lucide-react";

const logTypes = ["All", "Success", "Error", "Info"];

const logs = [
  { id: "1", time: "2025-04-04 14:32:01", type: "success", message: "Application submitted to Deloitte – SAP S/4HANA Program Manager", detail: "lead_id: LD-4521" },
  { id: "2", time: "2025-04-04 14:30:45", type: "success", message: "Resume tailored for SAP BTP Architect role", detail: "match_score: 87%" },
  { id: "3", time: "2025-04-04 14:28:12", type: "error", message: "LinkedIn rate limit exceeded – retrying in 15 min", detail: "platform: linkedin, error_code: 429" },
  { id: "4", time: "2025-04-04 14:25:00", type: "info", message: "Scraper started for LinkedIn – SAP jobs in India", detail: "filters: S/4HANA, BTP, FICO" },
  { id: "5", time: "2025-04-04 14:20:33", type: "success", message: "Application submitted to TCS – SAP FICO Lead", detail: "lead_id: LD-4519" },
  { id: "6", time: "2025-04-04 14:15:10", type: "error", message: "Naukri session expired – re-authentication required", detail: "platform: naukri, error_code: AUTH_EXPIRED" },
  { id: "7", time: "2025-04-04 14:10:22", type: "info", message: "Daily scraping quota: 847/2000 remaining", detail: "reset_at: 2025-04-05 00:00:00 UTC" },
  { id: "8", time: "2025-04-04 14:05:00", type: "success", message: "Recruiter email sent to Priya Sharma (Deloitte)", detail: "smtp: gmail, status: delivered" },
  { id: "9", time: "2025-04-04 13:55:44", type: "info", message: "New job matched: SAP Ariba Lead at IBM", detail: "relevance_score: 82%" },
  { id: "10", time: "2025-04-04 13:50:11", type: "error", message: "Resume generation failed – OpenAI timeout", detail: "model: gpt-4, timeout: 30s" },
];

const typeConfig: Record<string, { icon: typeof CheckCircle; className: string }> = {
  success: { icon: CheckCircle, className: "text-success" },
  error: { icon: AlertCircle, className: "text-destructive" },
  info: { icon: Info, className: "text-primary" },
};

export default function ActivityLogs() {
  const [activeFilter, setActiveFilter] = useState("All");

  const filtered = activeFilter === "All" ? logs : logs.filter(l => l.type === activeFilter.toLowerCase());

  return (
    <div className="space-y-6 animate-slide-up">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Activity Logs</h1>
          <p className="text-sm text-muted-foreground mt-1">System events and application history</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2 rounded-lg bg-secondary px-3 py-1.5">
            <Search className="h-3.5 w-3.5 text-muted-foreground" />
            <input type="text" placeholder="Search logs..." className="bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none w-40" />
          </div>
          <button className="p-2 rounded-lg bg-secondary text-muted-foreground hover:text-foreground transition-colors">
            <Filter className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex gap-2">
        {logTypes.map((f) => (
          <button
            key={f}
            onClick={() => setActiveFilter(f)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              activeFilter === f
                ? "bg-primary/15 text-primary"
                : "bg-secondary text-muted-foreground hover:text-foreground"
            }`}
          >
            {f}
          </button>
        ))}
      </div>

      {/* Log Table */}
      <div className="glass-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border/50">
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground w-10">Type</th>
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground w-44">Timestamp</th>
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">Event</th>
                <th className="text-left p-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground hidden lg:table-cell">Details</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((log) => {
                const config = typeConfig[log.type];
                const Icon = config.icon;
                return (
                  <tr key={log.id} className="border-b border-border/30 transition-colors hover:bg-secondary/30">
                    <td className="p-3"><Icon className={`h-4 w-4 ${config.className}`} /></td>
                    <td className="p-3">
                      <span className="flex items-center gap-1.5 text-xs text-muted-foreground">
                        <Clock className="h-3 w-3" />{log.time}
                      </span>
                    </td>
                    <td className="p-3 font-medium text-sm">{log.message}</td>
                    <td className="p-3 text-xs text-muted-foreground font-mono hidden lg:table-cell">{log.detail}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
