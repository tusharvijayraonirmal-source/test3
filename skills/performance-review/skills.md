---
name: Performance Review
id: performance-review
version: 1.0.0
description: Spot inefficiencies, redundant operations, and hotspots.
---

# Performance Review Skill

## Objective

Identify performance bottlenecks, inefficient algorithms, unnecessary resource usage, and scalability concerns in the provided code.

## Review Areas

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