import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SAP SaaS MVP',
  description: 'Job application SaaS MVP',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='en'>
      <body style={{ fontFamily: 'Arial, sans-serif', margin: 0, padding: 16 }}>{children}</body>
    </html>
  );
}
