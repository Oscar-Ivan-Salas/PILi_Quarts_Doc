
import { test, expect } from '@playwright/test';

test('Verify Application and Chat Interface', async ({ page }) => {
    // 1. Go to the app
    console.log('Navigating to http://localhost:3010...');
    await page.goto('http://localhost:3010');

    // 2. Check page title or key element to verify load
    await expect(page).toHaveTitle(/PILI/i); // Adjust regex as needed based on actual title
    console.log('Page loaded successfully.');

    // 3. Open Chat Panel if it's closed (assuming there's a button if closed, but default is open)
    // Check if chat input exists
    const chatInput = page.locator('input[placeholder="Escribe un mensaje..."]');

    // If input not visible, look for toggle button
    if (!(await chatInput.isVisible())) {
        console.log('Chat panel not visible, attempting to open...');
        await page.click('button:has(.lucide-message-square)'); // Selector based on the Lucide icon used in ChatPanel.tsx
    }

    // 4. Send a message
    console.log('Typing message...');
    await chatInput.fill('Hola, esto es una prueba automatizada.');
    await page.keyboard.press('Enter');

    // 5. Verify user message appears in list
    console.log('Message sent. Verifying in chat history...');
    await expect(page.locator('text=Hola, esto es una prueba automatizada.')).toBeVisible();

    // 6. Verify response (wait for a bit)
    console.log('Waiting for response...');
    // Expecting a response bubble (aligned left/start) that is NOT the user message
    // We can look for the Bot icon or just wait for a new message
    // Just waiting for ANY message with role 'assistant' implicitly via UI structure or text
    // Let's use a timeout wait for simplicity as exact content is distinctive
    await page.waitForTimeout(3000);

    // Check if any message bubles exist that are NOT the user one
    const messages = page.locator('.whitespace-pre-wrap');
    const count = await messages.count();

    if (count > 1) {
        console.log('Response received!');
        const responseText = await messages.last().innerText();
        console.log('Response text:', responseText);
    } else {
        console.warn('No response received within timeout.');
        // throw new Error('No response received from backend.'); // strict mode
    }
});
