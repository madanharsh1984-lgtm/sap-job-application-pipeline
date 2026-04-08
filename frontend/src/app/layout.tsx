import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'JobAccelerator AI',
  description: 'AI-Powered Job Application Pipeline',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  )
}
