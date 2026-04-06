import { test } from '@playwright/test';

test('check for console errors', async ({ page }) => {
  page.on('console', msg => {
    console.log(`BROWSER_CONSOLE: [${msg.type()}] ${msg.text()}`);
  });
  
  page.on('pageerror', error => {
    console.log(`BROWSER_ERROR: ${error.message}`);
  });

  await page.goto('http://localhost:3005/register');
  await page.waitForTimeout(5000);
});
