
import { test, expect } from '@playwright/test';

test.describe('Verify Application Buttons', () => {

    test.beforeEach(async ({ page }) => {
        await page.goto('http://localhost:3010');
    });

    test('Verify WorkspaceHeader Buttons', async ({ page }) => {
        // 1. Home Button
        const homeBtn = page.getByRole('button', { name: 'Inicio' });
        await expect(homeBtn).toBeVisible();
        await homeBtn.click();
        // Assuming no navigation yet, but it shouldn't crash

        // 2. Save Button
        const saveBtn = page.getByRole('button', { name: 'Guardar' });
        await expect(saveBtn).toBeVisible();
        await saveBtn.click();

        // 3. Theme Toggle (Sun/Moon)
        // This toggles a class on html, let's just click it
        const themeBtn = page.locator('header button').nth(2); // 3rd button
        await themeBtn.click();

        // 4. User Profile
        const userBtn = page.locator('header button').nth(3);
        await userBtn.click();
    });

    test('Verify NavigationPanel Quick Actions', async ({ page }) => {
        // Quick Actions are at the bottom
        const newProjectBtn = page.getByRole('button', { name: 'Nuevo Proyecto' });
        await expect(newProjectBtn).toBeVisible();
        await newProjectBtn.click();

        const calculatorBtn = page.getByRole('button', { name: 'Calculadora' });
        await expect(calculatorBtn).toBeVisible();
        await calculatorBtn.click();
    });

    test('Verify Navigation & WorkArea Buttons', async ({ page }) => {
        // 'Proyectos' is open by default. Verify 'Complejo' is visible directly.
        // We don't click 'Proyectos' toggle because that would close it.
        const complexSub = page.getByRole('button', { name: 'Complejo' });
        await expect(complexSub).toBeVisible();
        await complexSub.click();

        // Check 'New Complex Project' button in WorkArea
        const newComplexBtn = page.getByRole('button', { name: 'Nuevo Proyecto Complejo' });
        await expect(newComplexBtn).toBeVisible();
        await newComplexBtn.click();

        // Navigate to 'Cotizaciones' (this is closed via default)
        const quotesSection = page.getByText('Cotizaciones');
        await quotesSection.click();

        // Use regex to match "Simple" and "10" (badge) specifically, avoiding the "Simple 3" from Proyectos
        // This ensures we click the Cotizaciones subsection, not the Proyectos one
        const simpleQuoteSub = page.getByRole('button', { name: /Simple.*10/ });
        await expect(simpleQuoteSub).toBeVisible();
        await simpleQuoteSub.click();

        // Check 'New Quote' button
        const newQuoteBtn = page.getByRole('button', { name: 'Nueva Cotización' });
        await expect(newQuoteBtn).toBeVisible();
        await newQuoteBtn.click();
    });

    test('Verify Chat Interface Buttons', async ({ page }) => {
        // Toggle Chat
        const chatToggle = page.locator('button:has(.lucide-message-square)');
        await chatToggle.click(); // Close or Open
        await page.waitForTimeout(500);
        await chatToggle.click(); // Revert state

        // If open, check send button state (disabled if empty)
        const sendBtn = page.locator('button:has(.lucide-send)');
        await expect(sendBtn).toBeDisabled(); // Input is empty
    });

});
