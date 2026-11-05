---
title: "Contract Tests for AI-Generated Service Integrations"
slug: "contract-and-integration-testing"
date: "2026-10-28"
description: "Contract tests verify that services agree on APIs and message schemas, catching incompatible integrations and invented interfaces in AI-generated code."
tags:
  - Testing
  - Software Architecture
  - AI Engineering
author: "Mohamed Amine Bchir"
authorUrl: "https://tn.linkedin.com/in/mohamed-amine-bchir"
draft: false
readingTime: 3
seriesTitle: "Unit Tests Are Dead"
seriesOrder: 3
---

An inventory service may need product details from a Product Catalogue service, user information from a User service, or authorization from a Payment service. Each service can work correctly on its own and still fail when they communicate: the caller sends the wrong field, expects the wrong response, or publishes a message with a schema the consumer does not understand.

This is not a new problem caused by AI. Microservice teams have always needed to keep independently developed services compatible. AI makes the old problem easier to reproduce: an agent can confidently invent an endpoint, response shape, or event schema, then write a mock that agrees with the same invention. The local test passes; the real service does not.

## Check both sides of the agreement

A contract test checks compatibility between a consumer and provider. In a consumer-driven approach, the consumer records the interactions it relies on and the provider verifies it can honor them. With a provider-owned schema, consumers check their use against that published agreement. For messaging, producer and consumer must agree on the event schema and its evolution.

![An inventory consumer and product catalogue provider are checked against a contract test.](../assets/Contract-test-illustration.png)

The contract needs grounding outside the generated client and its mock: an OpenAPI document, event schema, or consumer-driven contract verified against the provider. A document can be stale, so it is not evidence that the running provider conforms unless it is checked. These tests establish compatibility, not availability, authentication, timeout behavior, or resilience.

Tools such as [Pact](https://pact.io/) and [Microcks](https://microcks.io/) can help define and verify these agreements. The point here is not a tool tutorial: when an agent creates an integration, retain an independent compatibility check and watch for plausible but invented APIs and schemas.

The service-boundary spec from the previous article can use a mock server to keep a scenario controlled. Contract testing asks the next question: **does that mock represent a contract the real dependent service also honors?**

Contract tests address compatibility, not maintainability. A change can communicate correctly and still leave code that is hard to understand or extend. Next, we look at [how deterministic quality gates steer AI-generated code](../articles/deterministic-quality-gates-for-ai-code.html).

## The series

1. [Unit Tests Are Dead. The Unit Moved.](../articles/ai-unit-tests-unit-moved.html)
2. [Spec Tests at the Service Boundary](../articles/testing-real-service-boundaries.html)
3. **Contract Tests for AI-Generated Service Integrations** (this article)
4. [Deterministic Quality Gates for AI Code](../articles/deterministic-quality-gates-for-ai-code.html)
5. [What Our Tests Don't Prove](../articles/what-our-tests-dont-prove.html)
