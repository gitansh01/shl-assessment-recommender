# SHL Conversational Assessment Recommender UI

This folder contains a **React + Tailwind CSS** landing page for the SHL Conversational Assessment Recommender. The UI is clean, minimal, and recruiter-friendly with a modern SaaS layout.

---

## ✅ Folder Structure

```
frontend/
├── index.html
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── vite.config.js
└── src/
    ├── App.jsx
    ├── main.jsx
    ├── index.css
    ├── data/
    │   └── content.js
    └── components/
        ├── Navbar.jsx
        ├── Hero.jsx
        ├── ChatDemo.jsx
        ├── ChatMessage.jsx
        ├── AssessmentCard.jsx
        ├── Features.jsx
        ├── FeatureCard.jsx
        ├── Workflow.jsx
        ├── WorkflowStep.jsx
        ├── TechStack.jsx
        ├── StackItem.jsx
        ├── SectionHeader.jsx
        ├── Badge.jsx
        └── Button.jsx
```

---

## ▶️ Run the UI

```
cd frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

---

## 🧩 Reusable Components

- **Button**: Primary and secondary CTAs
- **Badge**: Section labels
- **SectionHeader**: Consistent section title + description
- **FeatureCard / AssessmentCard / WorkflowStep**: Reusable card patterns
- **ChatMessage**: Consistent chat bubble layout

---

## 💬 Sample Chat Data (Realistic)

The demo section uses realistic conversation data in:
```
src/data/content.js
```

Example:
```
User: We are hiring a Java developer for a fintech platform.
AI: Great. Which key skills should the assessment cover?
User: Spring Boot, SQL, and communication skills.
AI: Here are the most relevant SHL assessments based on your needs.
```

---

## 🎨 Typography Suggestions (Professional & Clean)

Recommended fonts:
- **Inter** (already used)
- Alternatives: **IBM Plex Sans**, **Source Sans 3**, **Helvetica Neue**

Suggested type scale:
- H1: 40–48px, weight 600
- H2: 28–32px, weight 600
- Body: 16–18px, weight 400–500

---

## ✅ UI Best Practices Used

- Consistent spacing (`py-16`, `gap-6`, `max-w-6xl`)
- Subtle shadows and rounded corners
- Soft blue accent color only for key actions
- Clean hierarchy and readable typography
- Mobile responsive grid layouts
- Minimal animations (hover and transition)

---

## 🔧 Customization Tips

Want to adjust branding?
- Change colors in `tailwind.config.js`
- Update logo text in `Navbar.jsx`
- Replace CTA labels in `Hero.jsx`

Need to add sections?
- Add a new component in `src/components`
- Import and render inside `App.jsx`

---

## ✅ Summary

This UI is:
- Professional and recruiter-friendly
- Minimal, clean, modern SaaS style
- Fully responsive
- Component-based and reusable
- Built with React + Tailwind CSS

Perfect for a portfolio-quality HR-tech demo.
