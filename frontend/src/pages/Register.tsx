import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { useAuth } from "@/context/AuthContext";

export default function Register() {
  const { token } = useAuth();
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const normalizePhone = (value: string) => {
    const trimmed = value.trim();
    const cleaned = trimmed.replace(/[^\d+]/g, "");

    if (!cleaned) {
      return "";
    }

    if (cleaned.startsWith("+")) {
      return cleaned;
    }

    return cleaned.length === 10 ? `+91${cleaned}` : `+${cleaned}`;
  };

  // Handle Token redirect only if it's potentially valid
  useEffect(() => {
    if (token && token.length > 20) {
      console.log("Logged in user visiting register - redirecting to onboarding");
      navigate('/onboarding');
    }
  }, [token, navigate]);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    // Normalize phone number (remove spaces, ensure it starts with + if needed)
    // For this simulation, we keep it as is but ensure it's a string
    const normalizedPhone = normalizePhone(phone);

    console.log("Registering at:", `${import.meta.env.VITE_API_URL}/auth/register`);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          email: email.trim(), 
          password, 
          name: name.trim(), 
          phone: normalizedPhone 
        })
      });

      if (response.ok) {
        toast.success("Registration successful. Sign in to verify your email and WhatsApp OTP.");
        navigate('/login');
      } else {
        const error = await response.json();
        toast.error(error.detail || "Registration failed");
      }
    } catch (error) {
      console.error("Registration error:", error);
      toast.error("Failed to connect to server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4 futuristic-bg">
      <Card className="w-full max-w-md glass-card border-primary/20 shadow-2xl shadow-primary/5">
        <CardHeader className="space-y-1 text-center pb-2">
          <CardTitle className="text-2xl font-bold tracking-tight">Create an account</CardTitle>
          <CardDescription className="text-muted-foreground">
            Join JobAccelerator AI - Apply Smarter. Get Hired Faster.
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleRegister}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">Full Name</Label>
              <Input
                id="name"
                placeholder="Harsh Madan"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className="bg-secondary/50"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">Email address</Label>
              <Input
                id="email"
                type="email"
                placeholder="madan.harsh1984@gmail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-secondary/50"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone Number</Label>
              <Input
                id="phone"
                type="tel"
                placeholder="+91 9667964756"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
                className="bg-secondary/50"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="bg-secondary/50"
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col space-y-4">
            <Button type="submit" className="w-full h-11" disabled={loading}>
              {loading ? "Creating account..." : "Sign Up"}
            </Button>
            <p className="text-sm text-center text-muted-foreground">
              Already have an account?{" "}
              <Link to="/login" className="text-primary hover:underline font-medium">
                Sign In
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
