---
name: Security Review
id: security-review
version: 1.0.0
description: Identify potential vulnerabilities and unsafe patterns.
---

# Security Review Skill

**# Security Review Skill**

**## Objective**

Identify security vulnerabilities, unsafe coding patterns, insecure configurations, and potential attack vectors in the provided code.

**## Review Areas**

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

26. Security by design

- Sensitive data handling

- Public-facing applications or APIs

- Authentication or authorization changes

- New external integrations

- Significant architectural changes

27. Secure coding practices based on OWASP principles

28. Static security analysis

- Disabled SAST checks

- Bypassed security gates

- Removed or weakened security scanning

29. Security logging and auditability

- Login/logout events

- Failed authentication

- Password resets

- Critical transactions

- Security-sensitive administrative actions

30. Sensitive information in logs

- Passwords, tokens, API keys

- MFA/OTP codes

- Private keys or credentials

- Sensitive request or transaction data

31. Production-sensitive data protection

- Sensitive data used in non-production environments

- Missing masking or protection where required

**## Review Guidelines**

- Review the changed code and relevant surrounding code when necessary.

- Do not report a security issue without explaining the attack path or security impact.

- Distinguish confirmed vulnerabilities from potential risks and verification items.

- Never assume that a value is user-controlled unless the code or context supports it.

- Identify the source of untrusted input whenever possible.

- Identify the dangerous operation or sink.

- Explain whether input validation, encoding, authentication, or authorization is missing.

- Do not invent security requirements, architecture, files, functions, or business rules.

- Do not report an issue only because a security control is not visible in the supplied code.

- Do not report duplicate findings.

- Focus on issues affecting confidentiality, integrity, availability, authentication, authorization, or sensitive information.

- Do not expose actual secrets in the report.

- Mask sensitive values if they appear in the code.

- Consider the application's technology and execution environment.

- Avoid reporting theoretical vulnerabilities without practical evidence.

- Do not assume ISG approval is missing without supporting evidence.

- Treat missing organizational security or logging information as a verification item when appropriate.

**## Security Severity Guidelines**

- CRITICAL: Remote code execution, authentication bypass, or major data compromise.

- HIGH: Serious exploitable vulnerability with significant impact.

- MEDIUM: Exploitable issue requiring specific conditions or limited impact.

- LOW: Defense-in-depth issue or low-impact weakness.

- INFO: Security hardening or verification recommendation.

**## Required Security Finding Details**

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

**## False Positive Handling**

Do not report:

- A vulnerability when the relevant input is clearly trusted.

- A missing control that is implemented elsewhere and supported by context.

- A secret when the value is clearly a placeholder or test value.

- A theoretical attack without a reasonable attack path.

- Secure parameterized queries as SQL injection.

- Frontend-only validation as sufficient server-side validation.

- Missing ISG evidence as proof that ISG review was skipped.

- Missing logging when the supplied code does not provide enough context to determine whether logging occurs elsewhere.

**## OWASP Baseline**

Use OWASP Top 10 as a baseline when applicable, including:

- Broken Access Control

- Cryptographic Failures

- Injection

- Insecure Design

- Security Misconfiguration

- Vulnerable Components

- Identification and Authentication Failures

- Software and Data Integrity Failures

- Security Logging and Monitoring Failures

- Mishandling of security-sensitive information


## False Positive Handling

Do not report:

- A vulnerability when the relevant input is clearly trusted.
- A missing control that is implemented elsewhere and supported by context.
- A secret when the value is clearly a placeholder or test value.
- A theoretical attack without a reasonable attack path.

## Output Requirements

Return only valid JSON according to the review result schema.

If no security issue is found, return an empty findings array and state that no confirmed security vulnerability was identified in the reviewed scope.