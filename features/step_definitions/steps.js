const assert = require('assert');
const { Given, When, Then, Before } = require('@cucumber/cucumber');

// Counter to track scenario order within a single test run process.
// The Before hook increments this for each scenario; the second scenario will be forced to fail.
let scenarioCount = 0;

Before(function (scenario) {
  scenarioCount += 1;
  // Mark the second scenario to fail so we see the PR annotation.
  this.shouldFail = (scenarioCount === 2);
});

// Generic step handlers: these match any step text. Replace with specific regexes if you want tighter matching.
Given(/.*/, function () {
  // no-op setup
});

When(/.*/, function () {
  // no-op action
});

Then(/.*/, function () {
  if (this.shouldFail) {
    // intentional failing assertion for the second scenario
    assert.strictEqual(true, false);
  } else {
    // passing assertion for other scenarios
    assert.strictEqual(true, true);
  }
});
