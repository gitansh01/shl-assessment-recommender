import Button from "./Button.jsx";
import { navLinks } from "../data/content.js";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/80 backdrop-blur">
      <div className="container-page flex h-16 items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-100 text-brand-700">
            SHL
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-900">
              SHL Assessment Recommender
            </p>
            <p className="text-xs text-slate-500">
              Conversational assessment discovery
            </p>
          </div>
        </div>
        <nav className="hidden items-center gap-6 text-sm text-slate-600 md:flex">
          {navLinks.map((link) => (
            <a key={link.href} href={link.href} className="hover:text-slate-900">
              {link.label}
            </a>
          ))}
        </nav>
        <div className="hidden md:block">
          <Button href="#demo">Try Demo</Button>
        </div>
      </div>
    </header>
  );
}
