import SectionHeader from "./SectionHeader.jsx";
import StackItem from "./StackItem.jsx";
import { techStack } from "../data/content.js";

export default function TechStack() {
  return (
    <section id="stack" className="section-padding">
      <div className="container-page">
        <SectionHeader
          label="Tech Stack"
          title="Modern, production-ready stack"
          description="Built with reliable, industry-standard tooling for fast API delivery and high-quality retrieval."
        />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {techStack.map((item) => (
            <StackItem key={item.name} {...item} />
          ))}
        </div>
      </div>
    </section>
  );
}
