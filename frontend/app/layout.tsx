import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Agent Reliability Lab',
  description: 'FutureAGI-Powered Multi-Agent Reliability Benchmark Lab',
};

const navItems = [
  { label: 'Dashboard', href: '/' },
  { label: 'New Experiment', href: '/experiment' },
  { label: 'Experiments', href: '/experiments' },
  { label: 'Evaluations', href: '/evaluations' },
  { label: 'Logs', href: '/logs' },
  { label: 'Settings', href: '/settings' },
];

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${inter.className} antialiased bg-background text-primary`}
      >
        <div className="flex h-screen">
          {/* Sidebar */}
          <aside className="w-56 shrink-0 border-r border-border bg-card flex flex-col">
            <div className="px-5 py-6">
              <h1 className="text-lg font-semibold text-primary tracking-tight">
                Agent Bench
              </h1>
              <p className="text-xs text-secondary mt-0.5">Reliability Lab</p>
            </div>
            <nav className="flex-1 px-3">
              {navItems.map((item) => (
                <a
                  key={item.href}
                  href={item.href}
                  className="block rounded-md px-3 py-2 text-sm text-secondary hover:text-primary hover:bg-background transition-colors"
                >
                  {item.label}
                </a>
              ))}
            </nav>
          </aside>

          {/* Main area */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Top header */}
            <header className="h-14 shrink-0 border-b border-border bg-card flex items-center justify-between px-6">
              <span className="text-sm text-secondary">Dashboard</span>
              <span className="text-xs text-success bg-success/10 px-2 py-1 rounded">
                Connected to FutureAGI
              </span>
            </header>

            {/* Page content */}
            <main className="flex-1 overflow-y-auto p-6">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}
