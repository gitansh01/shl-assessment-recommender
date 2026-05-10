import SectionHeader from "./SectionHeader.jsx";
import FeatureCard from "./FeatureCard.jsx";
import { features } from "../data/content.js";

const icons = [
  <svg key="chat" viewBox="0 0 24 24" className="h-5 w-5">
    <path
      fill="currentColor"
      d="M7 7h10a1 1 0 010 2H7a1 1 0 010-2zm0 4h6a1 1 0 010 2H7a1 1 0 010-2zm-2 7a1 1 0 01-1-1V6a3 3 0 013-3h10a3 3 0 013 3v7a3 3 0 01-3 3H9l-4 3v-2z"
    />
  </svg>,
  <svg key="compare" viewBox="0 0 24 24" className="h-5 w-5">
    <path
      fill="currentColor"
      d="M7 3a2 2 0 012 2v14a2 2 0 11-4 0V5a2 2 0 012-2zm10 6a2 2 0 012 2v8a2 2 0 11-4 0v-8a2 2 0 012-2z"
    />
  </svg>,
  <svg key="refine" viewBox="0 0 24 24" className="h-5 w-5">
    <path
      fill="currentColor"
      d="M4 7h10a1 1 0 010 2H4a1 1 0 010-2zm0 8h6a1 1 0 010 2H4a1 1 0 010-2zm14-2 3 3-3 3-1.4-1.4 1.6-1.6-1.6-1.6L18 13z"
    />
  </svg>,
  <svg key="rag" viewBox="0 0 24 24" className="h-5 w-5">
    <path
      fill="currentColor"
      d="M4 5a2 2 0 012-2h12a2 2 0 012 2v12a2 2 0 01-2 2h-6l-4 3v-3H6a2 2 0 01-2-2V5zm4 4h8a1 1 0 010 2H8a1 1 0 010-2z"
    />
  </svg>,
  <svg key="shield" viewBox="0 0 24 24" className="h-5 w-5">
    <path
      fill="currentColor"
      d="M12 2l8 3v6c0 5-3.4 9.7-8 11-4.6-1.3-8-6-8-11V5l8-3zm-1 12.6l5-5-1.4-1.4L11 11.8 9.4 10.2 8 11.6l3 3z"
    />
  </svg>,
];

export default function Features() {
  return (
    <section id="features" className="section-padding">
      <div className="container-page">
        <SectionHeader
          label="Features"
          title="Designed for recruiters and hiring managers"
          description="Built for enterprise use with reliable recommendations, comparison tools, and strict catalog grounding."
        />
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature, index) => (
            <FeatureCard
              key={feature.title}
              {...feature}
              icon={icons[index % icons.length]}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
