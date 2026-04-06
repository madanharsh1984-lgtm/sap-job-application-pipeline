import { ShieldCheck, Linkedin, Globe, Mail, Power, RefreshCw, Lock } from "lucide-react";

const platforms = [
  {
    name: "LinkedIn",
    icon: Linkedin,
    status: "connected",
    lastSync: "5 min ago",
    details: "madan.harsh@email.com",
    color: "text-primary",
  },
  {
    name: "Naukri",
    icon: Globe,
    status: "connected",
    lastSync: "12 min ago",
    details: "madan_harsh_84",
    color: "text-success",
  },
  {
    name: "Gmail SMTP",
    icon: Mail,
    status: "disconnected",
    lastSync: "Never",
    details: "Not configured",
    color: "text-muted-foreground",
  },
];

export default function Credentials() {
  return (
    <div className="space-y-6 animate-slide-up">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Platform Credentials</h1>
        <p className="text-sm text-muted-foreground mt-1">Manage your connected platforms securely</p>
      </div>

      {/* Security Vault Banner */}
      <div className="glass-card p-5 border-primary/20">
        <div className="flex items-start gap-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
            <ShieldCheck className="h-5 w-5 text-primary" />
          </div>
          <div>
            <h2 className="font-semibold text-sm">Security Vault</h2>
            <p className="text-xs text-muted-foreground mt-1 max-w-xl">
              All credentials are encrypted using <span className="text-foreground font-medium">AES-256</span> and stored in <span className="text-foreground font-medium">AWS Secrets Manager</span>. Credentials are never stored in plain text and are only decrypted at runtime within isolated containers.
            </p>
            <div className="flex items-center gap-4 mt-3">
              <div className="flex items-center gap-1.5 text-xs text-success">
                <Lock className="h-3 w-3" />
                Vault Status: Sealed
              </div>
              <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                <RefreshCw className="h-3 w-3" />
                Last audit: 2 hours ago
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Platform Cards */}
      <div className="bento-grid grid-cols-1 md:grid-cols-3">
        {platforms.map((p) => (
          <div key={p.name} className="glass-card-hover p-5 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-secondary">
                  <p.icon className={`h-4 w-4 ${p.color}`} />
                </div>
                <div>
                  <h3 className="text-sm font-semibold">{p.name}</h3>
                  <p className="text-xs text-muted-foreground">{p.details}</p>
                </div>
              </div>
              <div className={`h-2 w-2 rounded-full ${p.status === "connected" ? "bg-success" : "bg-muted-foreground"}`} />
            </div>

            <div className="text-xs text-muted-foreground">
              Last sync: {p.lastSync}
            </div>

            <div className="flex items-center gap-2 mt-auto">
              {p.status === "connected" ? (
                <>
                  <button className="flex-1 rounded-lg bg-secondary px-3 py-2 text-xs font-medium text-secondary-foreground transition-colors hover:bg-secondary/80">
                    Update Connection
                  </button>
                  <button className="p-2 rounded-lg bg-destructive/10 text-destructive transition-colors hover:bg-destructive/20">
                    <Power className="h-3.5 w-3.5" />
                  </button>
                </>
              ) : (
                <button className="flex-1 rounded-lg bg-primary/15 px-3 py-2 text-xs font-semibold text-primary transition-colors hover:bg-primary/25">
                  Connect Account
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
