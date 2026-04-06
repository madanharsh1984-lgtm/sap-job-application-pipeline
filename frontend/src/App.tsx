import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes, Navigate, useLocation } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import DashboardLayout from "@/components/DashboardLayout";
import DashboardOverview from "@/pages/DashboardOverview";
import JobFeed from "@/pages/JobFeed";
import Credentials from "@/pages/Credentials";
import ResumeManager from "@/pages/ResumeManager";
import ActivityLogs from "@/pages/ActivityLogs";
import Onboarding from "@/pages/Onboarding";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import Index from "@/pages/Index";
import NotFound from "@/pages/NotFound";
import { AuthProvider, useAuth } from "@/context/AuthContext";

const queryClient = new QueryClient();

const getPostAuthPath = (user: { onboarding_step?: number } | null) => {
  if (!user || (user.onboarding_step ?? 0) < 3) {
    return "/onboarding";
  }

  return "/dashboard";
};

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { token, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div className="flex min-h-screen items-center justify-center futuristic-bg text-sm text-muted-foreground">Loading your workspace...</div>;
  }

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

const AppContent = () => {
  const { token, user, isLoading } = useAuth();

  if (token && isLoading) {
    return <div className="flex min-h-screen items-center justify-center futuristic-bg text-sm text-muted-foreground">Loading your account...</div>;
  }
  
  return (
    <Routes>
      <Route path="/login" element={!token ? <Login /> : <Navigate to={getPostAuthPath(user)} replace />} />
      <Route path="/register" element={<Register />} />
      <Route path="/onboarding" element={token ? <Onboarding /> : <Navigate to="/login" replace />} />
      <Route path="/" element={!token ? <Index /> : <Navigate to={getPostAuthPath(user)} replace />} />
      
      <Route 
        path="/dashboard" 
        element={
          <ProtectedRoute>
            {user && user.onboarding_step < 3 ? <Navigate to="/onboarding" replace /> : <DashboardLayout />}
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardOverview />} />
        <Route path="jobs" element={<JobFeed />} />
        <Route path="credentials" element={<Credentials />} />
        <Route path="resumes" element={<ResumeManager />} />
        <Route path="logs" element={<ActivityLogs />} />
      </Route>
      
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
