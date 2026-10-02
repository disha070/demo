const assert = require('assert');
const { Given, When, Then, Before } = require('@cucumber/cucumber');

let scenarioCount = 0;

Before(function () {
  scenarioCount += 1;
});

Given(/.*/, function () {
  // no-op setup
});

When(/.*/, function () {
  // no-op action
});

Then(/.*/, function () {
  assert.strictEqual(true, true);
});
