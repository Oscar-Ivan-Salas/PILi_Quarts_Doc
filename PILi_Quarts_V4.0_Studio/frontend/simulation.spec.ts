
import { test, expect } from '@playwright/test';

test.describe('PILI User Simulation', () => {
    test('Simulate Real User Conversation', async ({ page }) => {
        console.log('\n🔵 [USER] Abriendo navegador en http://localhost:3010...');
        await page.goto('http://localhost:3010');

        // Check Title
        const title = await page.title();
        console.log(`ℹ️ [SYSTEM] Título de la página: "${title}"`);
        await expect(page).toHaveTitle(/PILI/i);

        // Find Chat Interface
        console.log('ℹ️ [SYSTEM] Buscando interfaz de chat...');
        const chatInput = page.locator('input[placeholder="Escribe un mensaje..."]');

        // Open if needed
        if (!(await chatInput.isVisible())) {
            console.log('🟡 [USER] El chat está cerrado. Haciendo clic en el icono para abrir...');
            await page.click('button:has(.lucide-message-square)');
            await expect(chatInput).toBeVisible();
        }

        // Send Message
        const userMessage = "Hola PILI, ¿cómo estás hoy?";
        console.log(`🔵 [USER] Escribiendo: "${userMessage}"`);
        await chatInput.fill(userMessage);
        await page.waitForTimeout(500); // Small human pause
        await page.keyboard.press('Enter');

        // Check for typing indicator (optional, tough to catch but good to try)
        // console.log('ℹ️ [SYSTEM] Esperando indicador de "escribiendo"...');

        // Wait for Response
        console.log('⏳ [SYSTEM] Esperando respuesta del asistente...');
        // We wait for a new message bubble that is NOT the user's
        // Using a more robust locator strategy: wait for the last message to contain something meaningful or just count changes

        // Wait up to 10 seconds for response
        await expect(async () => {
            const messages = page.locator('.whitespace-pre-wrap');
            const count = await messages.count();
            // Assuming at least 1 message (user's) exists now. Wait for 2.
            expect(count).toBeGreaterThan(1);
        }).toPass({ timeout: 10000 });

        // Capture Response
        const messages = page.locator('.whitespace-pre-wrap');
        const responseText = await messages.last().innerText();

        console.log(`🟢 [ASSISTANT] Respuesta recibida:\n"${responseText}"\n`);

        console.log('✅ [SUCCESS] Conversación completada correctamente.');
    });
});
