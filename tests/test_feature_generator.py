import unittest

from scripts.generate_bdd_feature import build_feature


class BuildFeatureTests(unittest.TestCase):
    def test_builds_indented_feature_from_issue_fields(self):
        body = """### Feature name
Account sign-in

### User story
As a registered user
I want to sign in
So that I can access my account

### Scenarios (Gherkin)
Scenario: Successful sign-in
  Given a registered user
  When they submit valid credentials
  Then they see their account
"""

        feature = build_feature("42", body)

        self.assertEqual(
            feature,
            """Feature: Account sign-in

  As a registered user
  I want to sign in
  So that I can access my account

  Scenario: Successful sign-in
    Given a registered user
    When they submit valid credentials
    Then they see their account
""",
        )

    def test_rejects_scenarios_without_steps(self):
        body = """### Feature name
Sign-in

### User story
As a registered user
I want to sign in
So that I can access my account

### Scenarios (Gherkin)
Scenario: Sign-in
"""

        with self.assertRaisesRegex(ValueError, "at least one Gherkin step"):
            build_feature("42", body)


if __name__ == "__main__":
    unittest.main()