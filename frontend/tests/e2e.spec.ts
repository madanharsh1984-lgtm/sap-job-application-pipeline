import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

// Using a new, dedicated screenshot folder
const SCREENSHOT_DIR = 'C:/Users/madan/OneDrive/Desktop/Linkdin Commercial/frontend/test-results-new/screenshots';

if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

test.describe('JobAccelerator AI E2E Testing - Cycle 3', () => {
  
  test('TC-001: Navigation and Page Load', async ({ page }) => {
    await page.goto('http://localhost:3005', { waitUntil: 'networkidle' });
    await expect(page).toHaveTitle(/JobAccelerator AI/);
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, 'homepage_cycle3.png') });
  });

  test('TC-002: Registration Page UI', async ({ page }) => {
    await page.goto('http://localhost:3005/register', { waitUntil: 'networkidle' });
    await expect(page.locator('text=Create an account')).toBeVisible();
    // Using getByLabel for better robustness
    await expect(page.getByLabel('Full Name')).toBeVisible();
    await expect(page.getByLabel('Email address')).toBeVisible();
    await expect(page.getByLabel('Phone Number')).toBeVisible();
    await expect(page.getByLabel('Password')).toBeVisible();
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, 'registration_page_cycle3.png') });
  });

  test('TC-003: Login Page UI', async ({ page }) => {
    await page.goto('http://localhost:3005/login', { waitUntil: 'networkidle' });
    await expect(page.locator('text=Welcome back')).toBeVisible();
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, 'login_page_cycle3.png') });
  });

});
