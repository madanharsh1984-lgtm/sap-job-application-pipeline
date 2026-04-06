import { Upload, FileText, Download, Eye, Clock, CheckCircle, Sparkles } from "lucide-react";

const tailoredResumes = [
  { id: "1", target: "SAP S/4HANA Program Manager – Deloitte", created: "2h ago", status: "ready", matchScore: 92 },
  { id: "2", target: "SAP BTP Solutions Architect – Accenture", created: "5h ago", status: "ready", matchScore: 87 },
  { id: "3", target: "SAP FICO Lead – TCS", created: "1d ago", status: "generating", matchScore: 0 },
  { id: "4", target: "SAP MM/SD Senior Consultant – Capgemini", created: "1d ago", status: "ready", matchScore: 85 },
  { id: "5", target: "SAP ABAP Development Lead – Wipro", created: "2d ago", status: "ready", matchScore: 78 },
];

export default function ResumeManager() {
  return (
    <div className="space-y-6 animate-slide-up">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Resume Manager</h1>
        <p className="text-sm text-muted-foreground mt-1">Upload your master resume and manage AI-tailored versions</p>
      </div>

      {/* Upload Zone */}
      <div className="glass-card-hover p-8 border-dashed border-2 border-border/50">
        <div className="flex flex-col items-center text-center gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
            <Upload className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h2 className="font-semibold text-sm">Upload Master Resume</h2>
            <p className="text-xs text-muted-foreground mt-1">Drag & drop your .docx file or click to browse</p>
          </div>
          <button className="mt-2 rounded-lg bg-primary/15 px-4 py-2 text-xs font-semibold text-primary transition-colors hover:bg-primary/25">
            Select File
          </button>
          <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
            <FileText className="h-3 w-3" />
            Current: master_resume_v3.docx (Updated 2 days ago)
          </div>
        </div>
      </div>

      {/* Tailored Resumes */}
      <div>
        <h2 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-3">
          AI-Tailored Resumes ({tailoredResumes.length})
        </h2>
        <div className="space-y-2">
          {tailoredResumes.map((resume) => (
            <div key={resume.id} className="glass-card-hover p-4 flex items-center gap-4">
              <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-secondary">
                {resume.status === "ready" ? (
                  <CheckCircle className="h-4 w-4 text-success" />
                ) : (
                  <Sparkles className="h-4 w-4 text-warning animate-pulse-glow" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">{resume.target}</p>
                <div className="flex items-center gap-3 text-xs text-muted-foreground mt-0.5">
                  <span className="flex items-center gap-1"><Clock className="h-3 w-3" />{resume.created}</span>
                  {resume.status === "ready" && (
                    <span className="text-success font-medium">Match: {resume.matchScore}%</span>
                  )}
                  {resume.status === "generating" && (
                    <span className="text-warning font-medium">Generating...</span>
                  )}
                </div>
              </div>
              {resume.status === "ready" && (
                <div className="flex items-center gap-1 shrink-0">
                  <button className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors">
                    <Eye className="h-4 w-4" />
                  </button>
                  <button className="p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors">
                    <Download className="h-4 w-4" />
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
