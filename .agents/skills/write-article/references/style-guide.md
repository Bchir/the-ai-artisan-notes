# Style & Tone Guide: The AI Artisan Notes

## 1. Identity & Perspective

**The AI Artisan Notes** reflects the mindset of a modern software artisan: someone who views AI not as a black-box miracle or pure replacement for thinking, but as a sophisticated chisel and lathe for thoughtful builders.

- **Tone**: Pragmatic, insightful, direct, curious, and technically rigorous.
- **Perspective**: First-person plural ("we") or singular ("I") when sharing firsthand engineering experiences; clear third-person for architectural explanations.
- **Zero Fluff**: Skip generic marketing introductions (e.g., "In today's fast-paced digital world, AI is revolutionizing everything..."). Jump straight to the substance.

---

## 2. Structural Principles

### Inverted Pyramid with Craft Context
1. **The Hook**: State the thesis or challenge immediately in the first paragraph.
2. **Mental Models**: Use diagrams (Mermaid), analogies, or conceptual diagrams before diving into code.
3. **Working Code & Concrete Examples**: Show real, concise, reproducible patterns rather than pseudocode where possible.
4. **Edge Cases & Reality Checks**: Always discuss what fails, performance impacts, or failure modes.
5. **Synthesis**: Conclude with a crisp, actionable takeaway.

---

## 3. Formatting & Markdown Guidelines

- **Headings**:
  - H1 (`#`) is reserved for the page title (injected by the layout template).
  - Use H2 (`##`) for major sections.
  - Use H3 (`###`) for subsections.
- **Code Fences**:
  - Specify the language on every fence (` ```python `, ` ```bash `, ` ```typescript `).
  - Keep snippets focused; trim out boilerplate that distracts from the core point.
- **Callouts**:
  - Use GitHub-style alerts for emphasis:
    ```markdown
    > [!NOTE] Implementation context
    > [!TIP] Practical recommendation
    > [!WARNING] Potential risk or breaking change
    ```
- **Tables**:
  - Use markdown tables to compare alternatives or display trade-offs cleanly.
- **Lists**:
  - Use bold lead-ins for list items:
    ```markdown
    - **Determinism**: Ensures repeatability across identical prompts.
    - **Modularity**: Keeps runbooks small and focused.
    ```
