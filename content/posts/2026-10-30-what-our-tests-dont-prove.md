---
title: "What Our Tests Don't Prove"
slug: "what-our-tests-dont-prove"
date: "2026-10-30"
description: "Unit, spec, and contract tests provide evidence for changes, but operational readiness still requires risk-based load and recovery checks."
tags:
  - Testing
  - AI Engineering
author: "Mohamed Amine Bchir"
authorUrl: "https://tn.linkedin.com/in/mohamed-amine-bchir"
draft: false
readingTime: 3
seriesTitle: "Unit Tests Are Dead"
seriesOrder: 5
---

This series began with a green build that did not deserve our confidence: an agent changed the implementation and its tests together, and both could share the same mistaken assumption.

The answer was not to abandon unit tests. It was to use different checks for different questions. Focused unit tests protect algorithms and invariants. Spec tests check agreed behavior through the application boundary. Contract tests check compatibility between services. Deterministic quality gates enforce the engineering standards we choose. Together, they give us stronger evidence about a change, while leaving human review focused on behavior, design, and risk decisions that need judgment.

But passing the reservation scenarios, including the concurrency case, does not show that the service will meet its latency and error-rate targets under peak traffic. Load and recovery checks can provide evidence about those operational risks. Choose them in proportion to the cost of failure, not as a checklist for every change.

A green build means the checks we chose passed. It is not a verdict on the whole system. We choose the standards, gather the evidence that matters, and accept the remaining risk.

## The series

1. [Unit Tests Are Dead. The Unit Moved.](../articles/ai-unit-tests-unit-moved.html)
2. [Spec Tests at the Service Boundary](../articles/testing-real-service-boundaries.html)
3. [Contract Tests for AI-Generated Service Integrations](../articles/contract-and-integration-testing.html)
4. [Deterministic Quality Gates for AI Code](../articles/deterministic-quality-gates-for-ai-code.html)
5. **What Our Tests Don't Prove** (this article)
