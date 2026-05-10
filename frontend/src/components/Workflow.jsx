import SectionHeader from "./SectionHeader.jsx";
import WorkflowStep from "./WorkflowStep.jsx";
import { workflowSteps } from "../data/content.js";

export default function Workflow() {
  return (
    <section id="workflow" className="section-padding bg-white">
      <div className="container-page">
        <SectionHeader
          label="Workflow"
          title="A clear, enterprise-ready workflow"
          description="Every response is grounded in SHL catalog data to keep recommendations accurate and defensible."
        />
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center">
          {workflowSteps.map((step, index) => (
            <div key={step.title} className="flex flex-1 items-center gap-4">
              <WorkflowStep
                title={step.title}
                description={step.description}
                index={index + 1}
              />
              {index < workflowSteps.length - 1 ? (
                <span className="hidden text-lg font-semibold text-slate-400 lg:block">
                  →
                </span>
              ) : null}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
