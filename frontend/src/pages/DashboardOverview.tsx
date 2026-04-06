import { 
  Briefcase, Send, TrendingUp, ArrowUpRight, ArrowDownRight,
  Clock, CheckCircle, AlertCircle, Zap
} from "lucide-react";

const stats = [
  { label: "Jobs Scraped", value: "1,245", change: "+12%", up: true, icon: Briefcase, color: "text-primary" },
  { label: "Apps Sent", value: "89", change: "+8%", up: true, icon: Send, color: "text-success" },
  { label: "Success Rate", value: "14%", change: "+2.1%", up: true, icon: TrendingUp, color: "text-warning" },
  { label: "Active Pipelines", value: "3", change: "Stable", up: true, icon: Zap, color: "text-primary" },
];

const activities = [
  { time: "2 min ago", title: "Applied to SAP S/4HANA Program Manager", company: "Deloitte", status: "sent", icon: CheckCircle },
  { time: "15 min ago", title: "Resume tailored for SAP BTP Architect", company: "Accenture", status: "tailoring", icon: Clock },
  { time: "1 hr ago", title: "New job scraped: SAP FICO Lead", company: "TCS", status: "new", icon: Briefcase },
  { time: "2 hr ago", title: "Application failed: rate limit", company: "Infosys", status: "failed", icon: AlertCircle },
  { time: "3 hr ago", title: "Applied to SAP MM/SD Consultant", company: "Capgemini", status: "sent", icon: CheckCircle },
  { time: "5 hr ago", title: "Resume tailored for SAP ABAP Developer", company: "Wipro", status: "tailoring", icon: Clock },
];

const statusStyles: Record<string, string> = {
  sent: "text-success",
  tailoring: "text-warning",
  new: "text-primary",
  failed: "text-destructive",
};

export default function DashboardOverview() {
  return (
    <div className="space-y-6 animate-slide-up">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Command Center</h1>
          <p className="text-sm text-muted-foreground mt-1">Your SAP career pipeline at a glance</p>
        </div>
        
        {/* Giveaway Banner */}
        <div className="flex items-center gap-3 px-4 py-2 rounded-xl bg-primary/10 border border-primary/30 animate-pulse-glow">
          <div className="p-1.5 rounded-lg bg-primary/20 text-primary">
            <Zap className="h-4 w-4" />
          </div>
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-primary">Limited Time Offer</p>
            <p className="text-sm font-semibold">GIVEAWAY: 1-Month PRO Membership</p>
          </div>
        </div>
      </div>

      {/* Stats Bento Grid */}
      <div className="bento-grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div key={stat.label} className="glass-card-hover p-5 stat-glow">
            <div className="flex items-center justify-between mb-3">
              <stat.icon className={`h-5 w-5 ${stat.color}`} />
              <div className="flex items-center gap-1 text-xs">
                {stat.up ? (
                  <ArrowUpRight className="h-3 w-3 text-success" />
                ) : (
                  <ArrowDownRight className="h-3 w-3 text-destructive" />
                )}
                <span className="text-muted-foreground">{stat.change}</span>
              </div>
            </div>
            <div className="text-3xl font-bold tracking-tight">{stat.value}</div>
            <div className="text-xs text-muted-foreground mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      {/* Bento: Activity + Quick Actions */}
      <div className="bento-grid grid-cols-1 lg:grid-cols-3">
        {/* Recent Activity */}
        <div className="lg:col-span-2 glass-card p-5">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">Recent Activity</h2>
          <div className="space-y-1">
            {activities.map((a, i) => (
              <div key={i} className="flex items-start gap-3 rounded-lg p-3 transition-colors hover:bg-secondary/50">
                <a.icon className={`h-4 w-4 mt-0.5 shrink-0 ${statusStyles[a.status]}`} />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{a.title}</p>
                  <p className="text-xs text-muted-foreground">{a.company} · {a.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="glass-card p-5">
          <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <button className="w-full flex items-center gap-3 rounded-lg bg-primary/10 p-3 text-sm font-medium text-primary transition-colors hover:bg-primary/20">
              <Zap className="h-4 w-4" />
              Run Scraper Now
            </button>
            <button className="w-full flex items-center gap-3 rounded-lg bg-success/10 p-3 text-sm font-medium text-success transition-colors hover:bg-success/20">
              <Send className="h-4 w-4" />
              Batch Apply (Top 10)
            </button>
            <button className="w-full flex items-center gap-3 rounded-lg bg-secondary p-3 text-sm font-medium text-secondary-foreground transition-colors hover:bg-secondary/80">
              <Briefcase className="h-4 w-4" />
              View All Jobs
            </button>
          </div>

          <div className="mt-6 rounded-lg border border-border/50 p-4">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">Pipeline Health</h3>
            <div className="space-y-2">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-muted-foreground">LinkedIn</span>
                  <span className="text-success">Active</span>
                </div>
                <div className="h-1.5 rounded-full bg-secondary">
                  <div className="h-full w-3/4 rounded-full bg-success" />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-muted-foreground">Naukri</span>
                  <span className="text-warning">Throttled</span>
                </div>
                <div className="h-1.5 rounded-full bg-secondary">
                  <div className="h-full w-1/2 rounded-full bg-warning" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
