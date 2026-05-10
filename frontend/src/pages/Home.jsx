import Navbar from "../components/Navbar.jsx";
import Hero from "../components/Hero.jsx";
import ChatDemo from "../components/ChatDemo.jsx";
import Features from "../components/Features.jsx";
import Workflow from "../components/Workflow.jsx";
import ApiPreview from "../components/ApiPreview.jsx";
import TechStack from "../components/TechStack.jsx";
import Footer from "../components/Footer.jsx";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar />
      <main>
        <Hero />
        <ChatDemo />
        <Features />
        <Workflow />
        <ApiPreview />
        <TechStack />
      </main>
      <Footer />
    </div>
  );
}
