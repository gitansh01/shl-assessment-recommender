export const navLinks = [
  { label: "Features", href: "#features" },
  { label: "Workflow", href: "#workflow" },
  { label: "API", href: "#api" },
  { label: "Demo", href: "#demo" },
];

export const features = [
  {
    title: "Conversational recommendations",
    description:
      "Recruiters describe hiring needs in plain language and get curated assessments.",
  },
  {
    title: "Clarification handling",
    description:
      "The assistant asks follow-up questions when requirements are incomplete.",
  },
  {
    title: "Assessment comparison",
    description:
      "Compare two SHL assessments side-by-side with clear, grounded insights.",
  },
  {
    title: "Recommendation refinement",
    description:
      "Refine role, skills, or seniority and the shortlist updates instantly.",
  },
  {
    title: "Retrieval-augmented generation",
    description:
      "Searches the SHL catalog first to keep answers accurate and trusted.",
  },
  {
    title: "Hallucination prevention",
    description:
      "Strict guardrails keep responses inside the SHL catalog every time.",
  },
  {
    title: "SHL catalog grounding",
    description:
      "Only official SHL individual assessments are recommended with URLs.",
  },
];

export const workflowSteps = [
  {
    title: "User Query",
    description: "Hiring requirements shared in natural language.",
  },
  {
    title: "FastAPI Backend",
    description: "Stateless API receives full conversation context.",
  },
  {
    title: "FAISS Retrieval",
    description: "Semantic search across the SHL assessment catalog.",
  },
  {
    title: "Gemini LLM",
    description: "Clarifies intent and assembles recommendations.",
  },
  {
    title: "SHL Recommendations",
    description: "Shortlist delivered with official URLs and details.",
  },
];

export const techStack = [
  { name: "FastAPI", tag: "Backend" },
  { name: "Gemini", tag: "LLM" },
  { name: "FAISS", tag: "Vector Search" },
  { name: "sentence-transformers", tag: "Embeddings" },
  { name: "React", tag: "Frontend" },
  { name: "Tailwind CSS", tag: "Styling" },
];

export const apiPreview = {
  request: `{
  "messages": [
    {
      "role": "user",
      "content": "Hiring a Java developer with stakeholder communication skills."
    },
    {
      "role": "assistant",
      "content": "What seniority level are you hiring for?"
    },
    {
      "role": "user",
      "content": "Mid-level, around 4 years experience."
    }
  ]
}`,
  response: `{
  "reply": "Thanks. Here are the most relevant SHL assessments for a mid-level Java developer focused on stakeholder communication.",
  "recommendations": [
    {
      "name": "Java 8 (New)",
      "url": "https://www.shl.com/products/product-catalog/view/java-8-new/",
      "test_type": "K",
      "description": "Evaluates core Java knowledge, OOP fundamentals, and coding concepts."
    },
    {
      "name": "SQL Fundamentals",
      "url": "https://www.shl.com/products/product-catalog/view/sql-fundamentals/",
      "test_type": "K",
      "description": "Assesses SQL querying, joins, data manipulation, and database basics."
    },
    {
      "name": "DACT - Digital",
      "url": "https://www.shl.com/products/product-catalog/view/dact-digital/",
      "test_type": "P",
      "description": "Personality assessment focused on communication, teamwork, and work style."
    }
  ],
  "end_of_conversation": false
}`,
};
