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

Across the series, we looked at ways to agree on expected behavior, check it through service boundaries, verify compatibility between services, and enforce engineering standards. These checks help us respect our specifications and the behavior we promised. They do not close the book on operational requirements.

There is still a whole world to validate: latency, throughput, capacity, resilience, and recovery. A spec test can prove that an item is added to a cart, but not that it happens quickly under peak load. Make a customer wait 60 seconds and you have an angry customer, even if every functional test passes. Load, stress, and recovery tests matter too; choose them according to the operational requirements and the cost of failure.

A green build means the checks we chose passed. It is not a verdict on the whole system. We must gather evidence for both the behavior we promised and the operational experience users need, then make the remaining risks explicit.

## The series

1. [Unit Tests Are Dead. The Unit Moved.](../articles/ai-unit-tests-unit-moved.html)
2. [Spec Tests at the Service Boundary](../articles/testing-real-service-boundaries.html)
3. [Contract Tests for AI-Generated Service Integrations](../articles/contract-and-integration-testing.html)
4. [Deterministic Quality Gates for AI Code](../articles/deterministic-quality-gates-for-ai-code.html)
5. **What Our Tests Don't Prove** (this article)
