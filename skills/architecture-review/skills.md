---
name: Architecture Review
id: architecture-review
version: 1.0.0
description: Evaluate design patterns, modularity, and coupling.
---

# Architecture Review Skill

## Objective

Evaluate the overall design and structure of the code to identify architectural weaknesses, excessive coupling, poor separation of responsibilities, and maintainability risks.

## Review Areas

Review the code for:

1. Separation of concerns
2. Single Responsibility Principle
3. Modularity
4. Coupling between components
5. Cohesion within modules
6. Dependency direction
7. Circular dependencies
8. Layering violations
9. Poor abstraction boundaries
10. Large classes or functions
11. God objects
12. Tight coupling to infrastructure
13. Inappropriate design patterns
14. Incorrect design-pattern implementation
15. Difficult-to-test components
16. Poor configuration management
17. Inconsistent error-handling strategy
18. Inconsistent data-flow design
19. Poor API boundaries
20. Scalability and extensibility
21. Reusability
22. Maintainability
23. Backward compatibility
24. Technical debt
25. Risky architectural decisions

## Review Guidelines

- Review the code structure and available repository context.
- Explain how components interact.
- Identify the architectural principle or design concern involved.
- Do not recommend a complete rewrite unless clearly justified.
- Prefer incremental and practical improvements.
- Distinguish architectural defects from reasonable project-specific choices.
- Do not assume that a specific architecture is mandatory.
- Consider the application's current size, complexity, and expected growth.
- Explain the trade-offs of the recommended design.
- Avoid duplicate findings caused by the same architectural issue.

## Architecture Severity Guidelines

- CRITICAL: Architectural issue threatens system integrity or causes severe operational risk.
- HIGH: Major design problem that significantly limits reliability, scalability, or maintainability.
- MEDIUM: Important structural issue that should be addressed.
- LOW: Minor design improvement.
- INFO: Architectural recommendation or future enhancement.

## Required Finding Details

For every finding, provide:

- Finding ID
- File path or affected component
- Start and end line where applicable
- Severity
- Architecture category
- Issue title
- Evidence
- Root cause
- Architectural impact
- Affected components
- Possible solutions
- Recommended solution
- Trade-offs
- Migration or implementation steps
- Validation steps
- Confidence score

## Review Expectations

The review should consider:

- Current implementation
- Existing project structure
- Dependency relationships
- Data flow
- Error flow
- Extensibility
- Testability
- Operational complexity

## Output Requirements

Return only valid JSON according to the review result schema.

If no significant architectural concern is found, return an empty findings array and provide a short summary of the reviewed design.