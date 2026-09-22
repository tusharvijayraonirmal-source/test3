---
name: Test Quality Review
id: test-quality
version: 1.0.0
description: Review test coverage, assertions, and test design.
---

# Test Quality Review Skill

## Objective

Evaluate the quality, completeness, reliability, and maintainability of the available automated tests.

## Review Areas

Review the code and tests for:

1. Missing tests for important functionality
2. Missing tests for critical business logic
3. Missing edge-case tests
4. Missing negative-case tests
5. Missing exception tests
6. Weak or missing assertions
7. Assertions that do not validate behavior
8. Tests that can pass without testing the intended logic
9. Overuse of mocks
10. Incorrect mock behavior
11. Tests coupled to implementation details
12. Duplicate tests
13. Flaky test patterns
14. Order-dependent tests
15. Shared mutable test data
16. Poor test naming
17. Large and complex test cases
18. Missing setup or cleanup
19. Missing integration tests
20. Missing API contract tests
21. Missing security-related tests
22. Missing performance tests where relevant
23. Inadequate test isolation
24. Hard-coded environment assumptions
25. Missing regression tests for identified defects

## Review Guidelines

- Identify the production behavior that requires testing.
- Explain what scenario is not covered.
- Check whether assertions validate the expected result.
- Verify that tests cover success, failure, and boundary conditions.
- Do not claim that complete test coverage is required for every line.
- Prioritize critical paths and business behavior.
- Distinguish missing tests from poor test implementation.
- Do not report a missing test when equivalent coverage is clearly present elsewhere.
- Consider test readability, stability, and maintainability.
- Recommend the most valuable tests first.

## Test Quality Severity Guidelines

- CRITICAL: Critical functionality has no meaningful test coverage and may cause severe failures.
- HIGH: Important behavior or regression risk is insufficiently tested.
- MEDIUM: Noticeable test gap or weak test design.
- LOW: Minor test improvement.
- INFO: Optional testing recommendation.

## Required Finding Details

For every finding, provide:

- Finding ID
- Test file path
- Related production file or function
- Start and end line where applicable
- Severity
- Test category
- Issue title
- Evidence
- Missing or weak scenario
- Root cause
- Risk of undetected regression
- Possible test approaches
- Recommended test cases
- Suggested assertions
- Validation steps
- Confidence score

## Recommended Test Categories

When applicable, recommend:

- Unit tests
- Integration tests
- End-to-end tests
- API tests
- Contract tests
- Security tests
- Regression tests
- Boundary-value tests
- Negative tests
- Error-handling tests
- Performance tests

## Output Requirements

Return only valid JSON according to the review result schema.

If the available tests are adequate for the reviewed scope, return an empty findings array and summarize the tested areas.