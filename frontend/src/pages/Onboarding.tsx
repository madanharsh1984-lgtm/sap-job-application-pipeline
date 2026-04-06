import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { useAuth } from "@/context/AuthContext";
import { CheckCircle, Mail, Phone, Linkedin, ArrowRight, Loader2, Sparkles, User, Zap, Rocket } from "lucide-react";

const getDisplayStep = (currentUser: {
  is_email_verified?: boolean;
  is_phone_verified?: boolean;
  onboarding_step?: number;
} | null) => {
  if (!currentUser) {
    return 0;
  }

  if (!currentUser.is_email_verified || !currentUser.is_phone_verified) {
    return 0;
  }

  if ((currentUser.onboarding_step ?? 0) < 2) {
    return 1;
  }

  if ((currentUser.onboarding_step ?? 0) < 3) {
    return 2;
  }

  return 3;
};

export default function Onboarding() {
  const { user, token, refreshUser } = useAuth();
  const [step, setStep] = useState(getDisplayStep(user));
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Step 0: Basic Details
  const [name, setName] = useState(user?.name || "");
  const [phone, setPhone] = useState(user?.phone || "");

  // Step 1: Verification
  const [emailOtp, setEmailOtp] = useState("");
  const [phoneOtp, setPhoneOtp] = useState("");
  const [emailVerified, setEmailVerified] = useState(user?.is_email_verified || false);
  const [phoneVerified, setPhoneVerified] = useState(user?.is_phone_verified || false);
  const [useManual, setUseManual] = useState(false);

  // Step 2: LinkedIn
  const [linkedinUrl, setLinkedinUrl] = useState(user?.linkedin_id || "");
  const [score, setScore] = useState<number | null>(user?.linkedin_profile_score || null);
  const [optimizing, setOptimizing] = useState(false);

  useEffect(() => {
    const handleFyltrMessage = (event: MessageEvent) => {
      // Security: Check origin if needed
      // if (event.origin !== "https://www.fyltr.co") return;
      
      if (event.data === "fyltr_form_submitted" || event.data.type === "FORM_SUBMITTED") {
        toast.success("Profile data extracted!");
        // Refresh user data from backend to sync step
        setTimeout(() => refreshUser(), 1500);
      }
    };

    window.addEventListener("message", handleFyltrMessage);
    return () => window.removeEventListener("message", handleFyltrMessage);
  }, []);

  useEffect(() => {
    if (user) {
      setStep(getDisplayStep(user));
      setName(user.name || "");
      setPhone(user.phone || "");
      setEmailVerified(user.is_email_verified);
      setPhoneVerified(user.is_phone_verified);
      setLinkedinUrl(user.linkedin_id || "");
      setScore(user.linkedin_profile_score);
    }
  }, [user]);

  const updateOnboardingStep = async (nextStep: number) => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/user/me`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ onboarding_step: nextStep })
      });
      if (response.ok) {
        setStep(nextStep);
        await refreshUser();
      }
    } catch (error) {
      toast.error("Failed to update progress");
    }
  };

  const handleSaveDetails = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/user/me`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, phone })
      });
      if (response.ok) {
        toast.success("Details saved");
        await updateOnboardingStep(2);
      }
    } finally {
      setLoading(false);
    }
  };

  const verifyEmail = async () => {
    if (!emailOtp) return toast.error("Please enter the verification code");
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/verify-email`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: user?.email, code: emailOtp })
      });
      if (response.ok) {
        setEmailVerified(true);
        toast.success("Email verified");
        await refreshUser();
      } else {
        const error = await response.json();
        toast.error(error.detail || "Verification failed");
      }
    } finally {
      setLoading(false);
    }
  };

  const verifyPhone = async () => {
    if (!phoneOtp) return toast.error("Please enter the verification code");
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/verify-phone`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ phone, code: phoneOtp })
      });
      if (response.ok) {
        setPhoneVerified(true);
        toast.success("Phone verified");
        await refreshUser();
      } else {
        const error = await response.json();
        toast.error(error.detail || "Verification failed");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/resend-otp`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        toast.success("Verification codes resent via Email & WhatsApp");
      }
    } catch (error) {
      toast.error("Failed to resend OTP");
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluateLinkedin = async () => {
    if (!linkedinUrl) return toast.error("Please enter LinkedIn URL");
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/user/linkedin/evaluate`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setScore(data.score);
        toast.info(`Profile Score: ${data.score}%`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleOptimizeLinkedin = async () => {
    setOptimizing(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/user/linkedin/optimize`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setScore(data.score);
        toast.success("Profile Optimized to 98%!");
        setTimeout(() => {
          void updateOnboardingStep(3);
        }, 2000);
      }
    } finally {
      setOptimizing(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4 futuristic-bg">
      <div className="scanline"></div>
      <Card className="w-full max-w-2xl glass-card cyber-border cyber-glow shadow-2xl relative z-10">
        <CardHeader className="pb-2">
          <div className="flex justify-between items-center mb-4">
            {[0, 1, 2].map((i) => (
              <div key={i} className={`h-2 flex-1 mx-1 rounded-full ${step >= i ? 'bg-primary' : 'bg-secondary'}`} />
            ))}
          </div>
          <CardTitle className="text-2xl font-bold tracking-tight">
            {step === 0 && "Verify Identity"}
            {step === 1 && "Profile Setup"}
            {step === 2 && "LinkedIn Optimization"}
            {step === 3 && "Welcome Aboard!"}
          </CardTitle>
          <CardDescription>
            {step === 0 && "Secure your JobAccelerator AI account"}
            {step === 1 && "Complete your universal professional profile"}
            {step === 2 && "Boost your career with AI profile optimization"}
            {step === 3 && "JobAccelerator AI is ready to find your next role"}
          </CardDescription>
        </CardHeader>
        <CardContent className="min-h-[300px]">
          {step === 0 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4">
              <div className="p-4 rounded-xl bg-secondary/30 border border-border/50">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-lg bg-primary/20 text-primary"><Mail className="h-5 w-5" /></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">Email Verification</p>
                    <p className="text-xs text-muted-foreground">{user?.email}</p>
                  </div>
                  {emailVerified && <CheckCircle className="h-5 w-5 text-green-500" />}
                </div>
                {!emailVerified && (
                  <div className="flex flex-col gap-2">
                    <div className="flex gap-2">
                      <Input value={emailOtp} onChange={(e) => setEmailOtp(e.target.value)} placeholder="Enter code" className="bg-background" />
                      <Button onClick={verifyEmail} disabled={loading}>Verify</Button>
                    </div>
                    <p className="text-[10px] text-muted-foreground text-center">Didn't receive code? Check spam or <button onClick={handleResendOtp} className="underline text-primary">Resend</button></p>
                  </div>
                )}
              </div>

              <div className="p-4 rounded-xl bg-secondary/30 border border-border/50">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 rounded-lg bg-primary/20 text-primary"><Phone className="h-5 w-5" /></div>
                  <div className="flex-1">
                    <p className="text-sm font-medium">Phone Verification</p>
                    <p className="text-xs text-muted-foreground">{phone}</p>
                  </div>
                  {phoneVerified && <CheckCircle className="h-5 w-5 text-green-500" />}
                </div>
                {!phoneVerified && (
                  <div className="flex flex-col gap-2">
                    <div className="flex gap-2">
                      <Input value={phoneOtp} onChange={(e) => setPhoneOtp(e.target.value)} placeholder="Enter code" className="bg-background" />
                      <Button onClick={verifyPhone} disabled={loading}>Verify</Button>
                    </div>
                    <p className="text-[10px] text-muted-foreground text-center">Verification code sent from +91 9667964756 via WhatsApp <button onClick={handleResendOtp} className="underline text-primary">Resend</button></p>
                  </div>
                )}
              </div>
            </div>
          )}

          {step === 1 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4">
              {!useManual ? (
                <div className="p-6 rounded-2xl bg-secondary/20 border border-primary/20 text-center">
                  <Sparkles className="h-10 w-10 text-primary mx-auto mb-4" />
                  <h3 className="text-xl font-semibold mb-2">Smart Profile Setup</h3>
                  <p className="text-sm text-muted-foreground mb-6">Upload your resume, and our AI will automatically build your professional profile. No manual entry required.</p>
                  
                  {/* Fyltr.co Embedded Form */}
                  <div className="relative aspect-[4/3] w-full overflow-hidden rounded-xl border border-border/50 bg-background shadow-2xl">
                    <iframe 
                      src={`https://www.fyltr.co/embed/form/jobaccelerator-ai-onboarding?email=${user?.email}&name=${encodeURIComponent(user?.name || "")}`}
                      className="h-full w-full border-0"
                      title="Smart Onboarding Form"
                      onLoad={() => console.log("Fyltr form loaded")}
                    />
                  </div>
                  
                  <div className="mt-4 flex flex-col gap-2">
                    <p className="text-[10px] text-muted-foreground italic">Powered by Fyltr.co AI Extraction Engine</p>
                    <Button variant="ghost" size="sm" onClick={() => setUseManual(true)} className="text-primary text-xs hover:bg-primary/10">
                      Form not loading? Switch to Manual Setup
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="manual-name">Full Name</Label>
                    <Input id="manual-name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Harsh Madan" className="bg-secondary/50" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="manual-phone">Phone Number</Label>
                    <Input id="manual-phone" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+91 98765 43210" className="bg-secondary/50" />
                  </div>
                  <Button variant="ghost" size="sm" onClick={() => setUseManual(false)} className="text-muted-foreground text-xs">
                    Try Smart Setup instead
                  </Button>
                </div>
              )}
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 text-center">
              <div className="space-y-2 text-left">
                <Label>LinkedIn Profile URL</Label>
                <div className="flex gap-2">
                  <Input value={linkedinUrl} onChange={(e) => setLinkedinUrl(e.target.value)} placeholder="linkedin.com/in/username" className="bg-secondary/50" />
                  <Button onClick={handleEvaluateLinkedin} variant="outline" disabled={loading}>
                    {loading ? <Loader2 className="animate-spin h-4 w-4" /> : "Evaluate"}
                  </Button>
                </div>
              </div>

              {score !== null && (
                <div className="py-8 space-y-4">
                  <div className="relative inline-flex items-center justify-center">
                    <svg className="w-32 h-32 transform -rotate-90">
                      <circle cx="64" cy="64" r="58" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-secondary" />
                      <circle cx="64" cy="64" r="58" stroke="currentColor" strokeWidth="8" fill="transparent" 
                        strokeDasharray={364.4} strokeDashoffset={364.4 - (364.4 * score) / 100}
                        className={`${score > 90 ? 'text-green-500' : 'text-primary'} transition-all duration-1000 ease-out`} />
                    </svg>
                    <span className="absolute text-2xl font-bold">{score}%</span>
                  </div>
                  <p className="text-lg font-medium">LinkedIn Profile Score</p>
                  {score < 95 && (
                    <div className="p-4 rounded-xl bg-primary/10 border border-primary/20">
                      <p className="text-sm mb-3">Your score is below our target of 95%. Would you like our AI to optimize your profile for better visibility and ATS compatibility?</p>
                      <Button onClick={handleOptimizeLinkedin} className="w-full gap-2" disabled={optimizing}>
                        {optimizing ? <Loader2 className="animate-spin h-4 w-4" /> : <Sparkles className="h-4 w-4" />}
                        {optimizing ? "Optimizing..." : "Yes, Optimize My Profile"}
                      </Button>
                    </div>
                  )}
                  {score >= 95 && (
                    <div className="flex items-center justify-center gap-2 text-green-500 font-medium">
                      <CheckCircle className="h-5 w-5" /> Excellent Profile Score!
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {step === 3 && (
            <div className="text-center py-12 space-y-6 animate-in zoom-in-95">
              <div className="inline-flex p-6 rounded-full bg-green-500/20 text-green-500 mb-4">
                <CheckCircle className="h-16 w-16" />
              </div>
              <h2 className="text-3xl font-bold">You're All Set!</h2>
              <p className="text-muted-foreground max-w-sm mx-auto">Your account is verified and your professional profile is optimized to 98%. You're ready to apply across all industries.</p>
              <Button onClick={() => navigate('/dashboard')} size="lg" className="w-full max-w-xs group">
                Enter Dashboard <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          )}
        </CardContent>
        <CardFooter className="justify-end">
          {step === 0 && <Button onClick={() => updateOnboardingStep(1)} disabled={!emailVerified || !phoneVerified || loading}>Next Step <ArrowRight className="ml-2 h-4 w-4" /></Button>}
          {step === 1 && <Button onClick={handleSaveDetails} disabled={!name || !phone || loading}>Continue <ArrowRight className="ml-2 h-4 w-4" /></Button>}
          {step === 2 && score >= 95 && <Button onClick={() => updateOnboardingStep(3)}>Finalize <ArrowRight className="ml-2 h-4 w-4" /></Button>}
        </CardFooter>
      </Card>
    </div>
  );
}
