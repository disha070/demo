# GitHub Copilot Instructions: BDD and Gherkin

When implementing an issue that changes user-visible behavior, add or update a `.feature` file with acceptance scenarios and implement the corresponding tests and code. Do not create placeholder scenarios or tests just to make CI pass.

## User stories

When an issue needs a feature definition, put a business-facing story directly under the `Feature:` line:

```gherkin
Feature: Descriptive feature title
  As a [user persona or system role]
  I want to [action or system trigger]
  So that [business value]
```

## Gherkin conventions

- Capitalize keywords (`Feature:`, `Scenario:`, `Given`, `When`, `Then`, `And`).
- Indent `Scenario:` by 2 spaces and steps by 4 spaces.
- Quote concrete inputs, UI text, and expected messages with double quotes.
- Avoid placeholder values unless the scenario is a deliberate `Scenario Outline`.

## MFA behavior

- TOTP countdown window: 30 seconds.
- Token length: 6 digits.
- Lock out after 5 consecutive incorrect attempts.