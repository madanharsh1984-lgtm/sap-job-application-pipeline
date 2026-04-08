"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { logout } from "@/lib/api";

interface NavBarProps {
  isAdmin?: boolean;
}

export default function NavBar({ isAdmin }: NavBarProps) {
  const pathname = usePathname();

  const userLinks = [
    { href: "/dashboard", label: "Dashboard" },
    { href: "/jobs", label: "Qualified Jobs" },
    { href: "/resume", label: "Resume" },
    { href: "/connections", label: "Connections" },
    { href: "/account", label: "Account" },
  ];

  const adminLinks = [
    { href: "/admin/dashboard", label: "Dashboard" },
    { href: "/admin/users", label: "Users" },
    { href: "/admin/jobs", label: "Jobs" },
    { href: "/admin/payments", label: "Payments" },
  ];

  const links = isAdmin ? adminLinks : userLinks;

  return (
    <nav className="nav">
      <Link href={isAdmin ? "/admin/dashboard" : "/dashboard"} className="nav-brand">
        JobAccelerator AI {isAdmin && "(Admin)"}
      </Link>
      <div className="nav-links">
        {links.map((link) => (
          <Link
            key={link.href}
            href={link.href}
            style={pathname === link.href ? { color: "var(--primary)", fontWeight: 700 } : {}}
          >
            {link.label}
          </Link>
        ))}
        <button onClick={logout}>Logout</button>
      </div>
    </nav>
  );
}
