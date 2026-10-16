---
name: Security Review
id: security-review
version: 1.0.0
description: Identify potential vulnerabilities and unsafe patterns.
---

# Security Review Skill

## Objective

Identify security vulnerabilities, unsafe coding patterns, insecure configurations, and potential attack vectors in the provided code.

## Review Areas

Review the code for:

1. Injection vulnerabilities
   - SQL injection
   - Command injection
   - Code injection
   - Template injection
   - LDAP injection
2. Cross-site scripting
3. Cross-site request forgery
4. Broken authentication
5. Broken authorization and access control
6. Insecure direct object references
7. Sensitive data exposure
8. Hard-coded secrets and credentials
9. Unsafe handling of tokens and API keys
10. Insecure file operations
11. Path traversal
12. Unsafe deserialization
13. Server-side request forgery
14. Insecure HTTP communication
15. Missing TLS or certificate validation
16. Weak cryptographic practices
17. Insecure password handling
18. Improper input validation
19. Improper output encoding
20. Excessive permissions
21. Unsafe subprocess execution
22. Insecure dependency usage
23. Logging of passwords, tokens, or personal information
24. Missing security headers where applicable
25. Information leakage through error messages

## Review Guidelines

- Do not report a security issue without explaining the attack path or security impact.
- Distinguish confirmed vulnerabilities from potential risks.
- Never assume that a value is user-controlled unless the code or context supports it.
- Identify the source of untrusted input whenever possible.
- Identify the dangerous operation or sink.
- Explain whether input validation, encoding, authentication, or authorization is missing.
- Do not expose actual secrets in the report.
- Mask sensitive values if they appear in the code.
- Consider the application's technology and execution environment.
- Avoid reporting theoretical vulnerabilities without practical evidence.

## Security Severity Guidelines

- CRITICAL: Remote code execution, authentication bypass, or major data compromise.
- HIGH: Serious exploitable vulnerability with significant impact.
- MEDIUM: Exploitable issue requiring specific conditions or limited impact.
- LOW: Defense-in-depth issue or low-impact weakness.
- INFO: Security hardening recommendation.

## Required Security Finding Details

For every security finding, provide:

- Finding ID
- File path
- Start and end line
- Vulnerability category
- Severity
- Confidence
- Vulnerable code evidence
- Attack scenario
- Root cause
- Security impact
- Affected asset or data
- Possible solutions
- Recommended remediation
- Validation and security test steps
- Whether the issue requires configuration or code changes

## False Positive Handling

Do not report:

- A vulnerability when the relevant input is clearly trusted.
- A missing control that is implemented elsewhere and supported by context.
- A secret when the value is clearly a placeholder or test value.
- A theoretical attack without a reasonable attack path.

## Output Requirements

Return only valid JSON according to the review result schema.

If no security issue is found, return an empty findings array and state that no confirmed security vulnerability was identified in the reviewed scope.