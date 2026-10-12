---
name: Performance Review
id: performance-review
version: 1.0.0
description: Spot inefficiencies, redundant operations, and hotspots.
---

# Performance Review Skill

**## Objective**

Identify performance bottlenecks, inefficient algorithms, unnecessary resource usage, and scalability concerns in the provided code.

**## Review Areas**

Review the code for:

1. Inefficient algorithms

2. Unnecessary nested loops

3. Poor time complexity

4. Poor space complexity

5. Repeated database queries

6. N+1 query patterns

7. Unnecessary API calls

8. Repeated file or network operations

9. Unnecessary object creation

10. Redundant calculations

11. Repeated parsing or serialization

12. Inefficient string operations

13. Unnecessary data copying

14. Large memory allocations

15. Memory leaks

16. Unclosed resources

17. Blocking operations

18. Synchronous operations in asynchronous workflows

19. Missing pagination

20. Loading unnecessary data

21. Inefficient caching

22. Missing batching

23. Excessive logging

24. Poor concurrency handling

25. Scalability limitations

26. Resource and capacity management

27. Performance-impacting configuration changes

28. Availability and resilience considerations

29. Monitoring and observability of performance

30. Auditability of performance-impacting changes

**## Review Guidelines**

- Identify the operation that causes the performance concern.

- Explain the likely time or space complexity when possible.

- Distinguish actual bottlenecks from minor optimization opportunities.

- Do not recommend optimization without explaining the expected benefit.

- Consider readability and maintainability along with performance.

- Avoid premature optimization.

- Do not assume production traffic or data size without evidence.

- Clearly label assumptions.

- Consider the execution environment and framework.

- Explain whether the issue affects latency, throughput, memory, CPU, or scalability.

- Review the actual changed code and relevant surrounding code when necessary.

- Only report findings supported by the supplied code, configuration, or PR information.

- Do not invent organizational requirements, architecture, traffic, or business rules.

- Do not treat the absence of evidence in a Git diff as proof that an ISO control is missing.

- Distinguish confirmed performance weaknesses from requirements that require organizational or compliance verification.

- Do not report duplicate findings.

- Prefer actionable findings with a clear remediation or verification requirement.

- Consider availability, capacity, resource usage, monitoring, and operational resilience.

- Do not claim ISO compliance or non-compliance based solely on code review.

**## Resource and Capacity Management**

Check for:

- Unnecessary resource consumption.

- Inefficient use of CPU, memory, storage, database, or network resources.

- Resource limits and capacity considerations where applicable.

- Changes that may negatively affect system availability or scalability.

- Appropriate handling of resource-intensive operations.

**## Performance Monitoring**

Check for:

- Performance-relevant metrics where required.

- Monitoring of resource usage and application performance.

- Performance-impacting errors or failures being observable.

- Changes that disable or weaken existing monitoring.

- Performance monitoring being appropriate for critical functionality.

**## Availability and Resilience**

Check for:

- Operations that may cause service degradation or unavailability.

- Resource exhaustion risks.

- Appropriate timeout and retry handling.

- Failure handling for external services and dependencies.

- Performance changes that could affect system availability.

**## Change and Configuration Management**

Check for:

- Performance-impacting changes being appropriately reviewed.

- Changes to resource, infrastructure, or performance configurations being traceable.

- Performance-related configuration changes not being bypassed or disabled without appropriate review.

- Significant architectural or system changes being considered for performance impact.

**## Auditability**

Check for:

- Performance-impacting changes being traceable to the relevant change or Pull Request where applicable.

- Relevant performance configurations being documented or traceable where required.

- Performance-related monitoring or operational changes providing sufficient evidence for investigation.

If the repository does not provide sufficient evidence to determine whether an organizational requirement is implemented:

- Do not assume that the requirement is missing.

- Report it as a verification requirement where appropriate.

- Identify what needs to be verified by the responsible team.

**## Verification Items**

Use a verification item when a requirement cannot be confirmed from the supplied code or configuration.

Examples:

- Capacity requirements may require verification.

- Performance monitoring integration may require verification.

- Resource limits may require confirmation from the responsible team.

- Availability and resilience requirements may require organizational verification.

- Significant performance-impacting architectural changes may require additional review.

Do not present a verification item as a confirmed performance issue or ISO non-compliance.

## Review Guidelines

- Identify the operation that causes the performance concern.
- Explain the likely time or space complexity when possible.
- Distinguish actual bottlenecks from minor optimization opportunities.
- Do not recommend optimization without explaining the expected benefit.
- Consider readability and maintainability along with performance.
- Avoid premature optimization.
- Do not assume production traffic or data size without evidence.
- Clearly label assumptions.
- Consider the execution environment and framework.
- Explain whether the issue affects latency, throughput, memory, CPU, or scalability.

## Performance Severity Guidelines

- CRITICAL: Performance issue can cause system outage or severe resource exhaustion.
- HIGH: Significant bottleneck likely to affect production workloads.
- MEDIUM: Noticeable inefficiency or scalability concern.
- LOW: Minor optimization opportunity.
- INFO: Optional improvement with limited immediate impact.

## Required Finding Details

For every finding, provide:

- Finding ID
- File path
- Start and end line
- Severity
- Performance category
- Issue title
- Evidence
- Root cause
- Expected impact
- Complexity analysis where applicable
- Possible solutions
- Recommended solution
- Validation steps
- Suggested benchmark or measurement
- Confidence score

## Validation Recommendations

Where appropriate, recommend:

- Unit or integration performance tests
- Load testing
- Stress testing
- Profiling
- Query analysis
- Memory measurement
- Benchmark comparison
- Response-time measurement
- CPU and memory monitoring

## Output Requirements

Return only valid JSON according to the review result schema.

Do not report a performance issue solely because an alternative implementation may be theoretically faster. Provide evidence or a reasonable explanation of the likely impact.