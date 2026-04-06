import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { execSync } from 'child_process';

const SCREENSHOT_DIR = 'C:/Users/madan/OneDrive/Desktop/Linkdin Commercial/frontend/test-results-new/screenshots';

// Use a unique directory for each test run to avoid locks
if (!fs.existsSync(SCREENSHOT_DIR)) {
  fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });
}

function getOTPs(email) {
  try {
    const content = execSync('docker exec sap-saas-api cat latest_otp.txt').toString().trim();
    const [savedEmail, emailOtp, phoneOtp] = content.split(':');
    if (savedEmail === email) {
      return { emailOtp, phoneOtp };
    }
  } catch (err) {
    console.error("Error reading latest_otp.txt:", err.message);
  }
  return null;
}

test.describe('JobAccelerator AI Functional Testing - Cycle 4', () => {

  const testEmail = `test_${Date.now()}@gmail.com`;
  const testPhone = `+91${Math.floor(Math.random() * 9000000000) + 1000000000}`;

  test('Full E2E Signup & Onboarding Flow', async ({ page }) => {
    // 1. Register
    await page.goto('http://localhost:3005/register', { waitUntil: 'networkidle' });
    await page.getByLabel('Full Name').fill('Test User');
    await page.getByLabel('Email address').fill(testEmail);
    await page.getByLabel('Phone Number').fill(testPhone);
    await page.getByLabel('Password').fill('Password123!');
    await page.getByRole('button', { name: 'Sign Up' }).click();

    // 2. Login
    await page.waitForURL('**/login', { timeout: 15000 });
    await page.getByLabel('Email address').fill(testEmail);
    await page.getByLabel('Password').fill('Password123!');
    await page.getByRole('button', { name: 'Sign In' }).click();

    // 3. Verify OTP (Wait for Onboarding)
    await page.waitForURL('**/onboarding', { timeout: 15000 });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, `onboarding_${Date.now()}.png`) });

    await page.waitForTimeout(3000); 
    const otps = getOTPs(testEmail);
    if (!otps) throw new Error("Could not find OTP in latest_otp.txt");

    // Email OTP
    const emailBox = page.locator('div.rounded-xl', { hasText: 'Email Verification' });
    await emailBox.getByPlaceholder('Enter code').fill(otps.emailOtp);
    await emailBox.getByRole('button', { name: 'Verify' }).click();
    await expect(page.locator('text=Email verified').first()).toBeVisible();

    // Phone OTP
    const phoneBox = page.locator('div.rounded-xl', { hasText: 'Phone Verification' });
    await phoneBox.getByPlaceholder('Enter code').fill(otps.phoneOtp);
    await phoneBox.getByRole('button', { name: 'Verify' }).click();
    await expect(page.locator('text=Phone verified').first()).toBeVisible();

    // Click Next Step
    const nextStepButton = page.getByRole('button', { name: 'Next Step' });
    await expect(nextStepButton).toBeEnabled();
    await nextStepButton.click();

    // Step 1: Profile Setup
    await page.waitForSelector('text=Profile Setup', { timeout: 10000 });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, `step1_setup_${Date.now()}.png`) });

    // Switch to manual setup
    await page.getByRole('button', { name: 'Switch to Manual Setup' }).click();
    await page.locator('#manual-name').fill('Test User');
    await page.locator('#manual-phone').fill(testPhone);
    
    // Click "Continue"
    const continueBtn = page.getByRole('button', { name: 'Continue' });
    await expect(continueBtn).toBeEnabled();
    await continueBtn.click();

    // Step 2: LinkedIn Optimization
    await page.waitForSelector('text=LinkedIn Optimization', { timeout: 10000 });
    await page.getByPlaceholder('linkedin.com/in/username').fill('https://www.linkedin.com/in/testuser');
    await page.getByRole('button', { name: 'Evaluate' }).click();
    
    // Wait for score to appear
    await page.waitForSelector('text=Profile Score', { timeout: 15000 });
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, `step2_linkedin_${Date.now()}.png`) });

    // Click "Optimize My Profile" if score < 95
    const optimizeBtn = page.getByRole('button', { name: 'Optimize My Profile' });
    if (await optimizeBtn.isVisible()) {
      await optimizeBtn.click();
      await page.waitForSelector('text=Excellent Profile Score!', { timeout: 20000 });
    }

    // Click "Finalize"
    const finalizeBtn = page.getByRole('button', { name: 'Finalize' });
    await expect(finalizeBtn).toBeEnabled();
    await finalizeBtn.click();

    // Step 3: Welcome Aboard
    await page.waitForSelector('text=You\'re All Set!', { timeout: 10000 });
    await page.getByRole('button', { name: 'Enter Dashboard' }).click();

    // Verify Dashboard
    await page.waitForURL('**/dashboard', { timeout: 15000 });
    await expect(page.locator('text=Command Center').first()).toBeVisible();
    await page.screenshot({ path: path.join(SCREENSHOT_DIR, `completed_${Date.now()}.png`) });
  });

});
