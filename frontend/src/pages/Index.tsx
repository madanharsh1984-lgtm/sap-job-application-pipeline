import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { 
  Zap, ArrowRight, Sparkles, Gift
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen futuristic-bg text-foreground selection:bg-primary/30 selection:text-primary-foreground font-sans antialiased">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-background/40 backdrop-blur-xl border-b border-white/5 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-primary flex items-center justify-center shadow-[0_0_20px_rgba(0,243,255,0.3)]">
              <Zap className="h-6 w-6 text-black fill-current" />
            </div>
            <span className="font-black text-2xl tracking-tighter uppercase italic">JobAccelerator<span className="text-primary italic">AI</span></span>
          </div>
          <div className="flex items-center gap-6">
            <Button variant="ghost" onClick={() => navigate("/login")} className="hidden sm:flex font-bold uppercase tracking-widest text-xs opacity-70 hover:opacity-100 hover:bg-white/5 transition-all">Login</Button>
            <Button onClick={() => navigate("/register")} className="h-11 px-8 font-black uppercase tracking-widest text-xs rounded-full bg-primary text-black hover:bg-primary/80 shadow-[0_0_25px_rgba(0,243,255,0.4)] transition-all">
              Join Waitlist
            </Button>
          </div>
        </div>
      </nav>

      {/* Main Hero / Content */}
      <main className="pt-32 pb-20 px-6">
        <div className="max-w-5xl mx-auto text-center space-y-12">
          
          {/* Header Section (Matching Image Text) */}
          <div className="space-y-4 animate-in fade-in slide-in-from-top-10 duration-1000">
            <h1 className="text-5xl md:text-8xl font-black tracking-tighter leading-none text-white drop-shadow-[0_4px_4px_rgba(0,0,0,0.5)]">
              JobAccelerator AI:<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-b from-white to-zinc-500">Arriving Soon!</span>
            </h1>
          </div>

          {/* Giveaway Section (Matching Image Box & Text) */}
          <div className="relative max-w-2xl mx-auto py-12 animate-in fade-in zoom-in duration-1000">
            {/* Background Glows */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] bg-primary/5 blur-[120px] rounded-full pointer-events-none" />
            
            {/* The Box (Represented with a Card) */}
            <div className="relative z-10 p-1 rounded-[2rem] bg-gradient-to-b from-zinc-700/50 to-transparent">
              <div className="p-8 md:p-12 rounded-[1.8rem] bg-card/80 border border-zinc-500/20 backdrop-blur-3xl relative overflow-hidden group shadow-2xl">
                {/* Circuit pattern overlay inside card */}
                <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/circuit-board.png')] opacity-5 pointer-events-none" />
                
                <div className="flex flex-col items-center space-y-8 relative z-10">
                  {/* Glowing Box Icon / Placeholder */}
                  <div className="relative group cursor-pointer animate-bounce duration-[4000ms]">
                    <div className="absolute inset-0 bg-accent/20 blur-3xl rounded-full scale-150 group-hover:bg-accent/40 transition-all duration-500" />
                    <div className="h-40 w-40 md:h-56 md:w-56 bg-gradient-to-br from-zinc-800 to-black rounded-3xl border-2 border-zinc-700 flex items-center justify-center shadow-2xl relative">
                      {/* Ribbons matching image */}
                      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-8 h-full bg-accent/30 border-x border-accent/20" />
                      <div className="absolute top-1/2 left-0 -translate-y-1/2 w-full h-8 bg-accent/30 border-y border-accent/20" />
                      
                      <Gift className="h-20 w-20 md:h-32 md:w-32 text-white drop-shadow-[0_0_20px_rgba(255,255,255,0.5)]" />
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h2 className="text-4xl md:text-6xl font-black tracking-tight uppercase italic leading-none">
                      <span className="text-primary drop-shadow-[0_0_15px_rgba(0,243,255,0.5)]">GIVEAWAY:</span><br />
                      <span className="text-white">1-Month PRO</span><br />
                      <span className="text-white">Membership</span>
                    </h2>
                  </div>
                </div>
              </div>
            </div>

            {/* Entry Instructions (Matching Image Text) */}
            <div className="mt-12 space-y-6 text-center animate-in fade-in slide-in-from-bottom-10 duration-1000 delay-500">
              <h3 className="text-2xl md:text-4xl font-black tracking-tighter text-white">To enter:</h3>
              <div className="flex flex-col items-center space-y-4 text-lg md:text-2xl font-bold tracking-tight text-zinc-300">
                <p className="flex items-center gap-4">
                  <span className="text-primary font-black">1.</span> Share this post
                </p>
                <p className="flex items-center gap-4">
                  <span className="text-primary font-black">2.</span> Comment "JobAccelerator AI"
                </p>
              </div>
            </div>
          </div>

          {/* Waitlist CTA */}
          <div className="pt-12 animate-in fade-in slide-in-from-bottom-12 duration-1000 delay-700">
            <Button 
              size="lg" 
              onClick={() => navigate("/register")} 
              className="h-16 px-12 text-xl font-black uppercase tracking-widest rounded-full bg-primary text-black hover:bg-primary/80 shadow-[0_0_40px_rgba(0,243,255,0.3)] gap-4 transition-all hover:scale-105"
            >
              Get Early Access <ArrowRight className="h-6 w-6" />
            </Button>
          </div>
        </div>
      </main>

      {/* Footer info */}
      <footer className="py-12 px-6 border-t border-white/5 mt-20">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6 text-zinc-500 text-sm font-bold uppercase tracking-widest">
          <p>© 2026 JobAccelerator AI. All rights reserved.</p>
          <div className="flex gap-8">
            <a href="#" className="hover:text-primary transition-colors">Privacy</a>
            <a href="#" className="hover:text-primary transition-colors">Terms</a>
            <a href="#" className="hover:text-primary transition-colors">Twitter</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
