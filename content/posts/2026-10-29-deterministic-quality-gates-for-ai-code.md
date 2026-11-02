---
title: "Deterministic Quality Gates for AI Code"
slug: "deterministic-quality-gates-for-ai-code"
date: "2026-10-29"
description: "Deterministic quality gates let agents fix routine violations before review, so people can focus on behavior, design, and engineering decisions."
tags:
  - Software Quality
  - AI Engineering
author: "Mohamed Amine Bchir"
authorUrl: "https://tn.linkedin.com/in/mohamed-amine-bchir"
draft: false
readingTime: 5
seriesTitle: "Unit Tests Are Dead"
seriesOrder: 4
---

We built analyzers to tell us when code was getting harder to maintain. Then we ignored them.

Not because the warnings were always hard to understand, but because dealing with them cost time and attention. You stop the feature you were working on, switch context, inspect the warning, decide whether it matters, make a change, and rerun checks. When the task is already demanding and the warning is not blocking you, it is easy to defer it. Sometimes we simply could not be bothered. Then the warnings pile up, and the next person has even more noise to sort through.

An agent changes that trade-off. It can handle the repetitive loop of running the check, investigating the diagnostic, making a reasoned fix, and verifying it without asking a person to repeatedly abandon their work for each warning. That makes it practical to enforce standards more strictly than we often did before agents: checks that used to be advisory can become build-blocking gates, applied consistently rather than only when someone has time and patience to chase them.

This is not a reason to blindly promote every warning to an error. People still choose which standards matter, and agents still need guidance to address the design concern rather than silence the signal. The payoff is less human effort spent on routine cleanup and more attention available for behavior, architecture, and decisions that need judgment.

## Choose gates that protect real decisions

A quality gate is useful when it enforces a decision the team actually values and gives feedback specific enough to act on. Depending on the stack and risk, that might be a complexity threshold, a forbidden dependency rule, a type check, or a security analyzer. Turning on every available warning is not a quality strategy; a noisy gate teaches people and agents to work around it.

The metric is not the goal. The quality decision behind it is.

## Choose and tune the checks

Quality gates do not have to be invented one rule at a time. For example, Microsoft's .NET SDK analyzers offer predefined analysis modes, including a `Recommended` mode, and let teams enable or tune rules by category or individual diagnostic. In other ecosystems, use the equivalent presets and per-rule configuration. Start with a useful baseline, then make the checks that matter to your project visible and enforceable.

As one concrete example, a shipping endpoint that accumulates checks for payment, inventory, destination, customs, and delivery can cross a configured cyclomatic-complexity limit. In .NET, CA1502 can report that threshold violation. The diagnostic is a signal to inspect the design, not an instruction to extract code mechanically. See Microsoft's documentation on [analysis modes and category configuration](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/configuration-options) and the [CA1502 complexity rule](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1502).

Put a short, tool-independent instruction in the repository's `AGENTS.md` so agents can apply it to any quality gate:

```markdown
When a quality gate fails:

- Identify what the check is intended to protect. Use its output, rule ID, category, documentation, failing test, and surrounding design as evidence.
- Decide whether the code has the underlying problem. If a sensible design change addresses it, make that change; do not just silence the diagnostic, move the violation, or game a metric.
- Re-run the relevant checks and tests. Confirm that the change fixed the concern without breaking behavior or creating the same problem elsewhere.
- Treat suppression or an exception as a last resort, only when the rule does not apply or conflicts with a sound design. Keep it narrow and justify why it is warranted.
```

For the complexity example, that means the agent first investigates whether the endpoint is combining unrelated shipping decisions. If payment, inventory, and delivery rules belong together, splitting them just to lower the count is metric gaming. If the endpoint really is coordinating distinct responsibilities, a focused policy or other design change may make the code easier to understand and maintain. The extracted logic and its behavior still need tests, and the gate still applies there. If the complexity is inherent and the rule is not useful in that case, the agent should explain why and propose a narrow, justified exception for review rather than take suppression as its first move.

That is the feedback loop: the check points to a concern; the agent investigates intent and design, makes a reasoned change, then reruns the gate and relevant tests. A green result confirms the configured threshold is met. It does not by itself prove the design improved, so the change remains reviewable by a person.

## Let agents close the feedback loop

The same principle applies beyond a compiler analyzer. A formatter or type checker can block a build; an architecture test can identify a forbidden dependency; a security check can report a vulnerable package. Whatever the tool, its result needs to reach the agent while it can still act on it. The agent should investigate the failure, make a reasoned change, and rerun the gate and relevant tests before handing the work to a reviewer. If a check only appears later in a dashboard or pull-request system, make sure the agent can retrieve it and the team agrees whether it blocks a merge.

For a new codebase, the team can start with a strict baseline. In a mature system, apply a rule to changed code first and expand it as existing debt is addressed. Either way, choose gates for the risks they reduce, keep their feedback actionable, and avoid enforcing thresholds for their own sake. A green check is not a design review; it is evidence that the configured boundary passed. Human review still matters. It can focus less on routine violations and more on choices the rules cannot make, while the code is held to a stricter, more consistent baseline.

## The series

1. [Unit Tests Are Dead. The Unit Moved.](../articles/ai-unit-tests-unit-moved.html)
2. [Spec Tests at the Service Boundary](../articles/testing-real-service-boundaries.html)
3. [Contract Tests for AI-Generated Service Integrations](../articles/contract-and-integration-testing.html)
4. **Deterministic Quality Gates for AI Code** (this article)
5. [What Our Tests Don't Prove](../articles/what-our-tests-dont-prove.html)
