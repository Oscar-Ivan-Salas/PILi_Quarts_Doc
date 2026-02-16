import { test, expect } from '@playwright/test';

test('Full User Journey: Quote Creation and Export', async ({ page }) => {
    // 1. Navigate to Home
    await page.goto('http://localhost:3010');

    // 2. Select "Cotización Simple"
    // Closes "Proyectos" (expanded by default) to avoid ambiguity? No, just expand Cotizaciones
    await page.getByRole('button', { name: 'Cotizaciones' }).click();
    // Wait for animation
    await page.waitForTimeout(500);
    // specific selector for the first "Simple" button (Cotizaciones is first in list)
    // We can filter by the section container if needed, but order usage is acceptable here
    await page.getByRole('button', { name: 'Simple' }).first().click();

    // 3. Fill Form
    // Check for unique text on form
    await expect(page.getByText('Datos del Cliente')).toBeVisible();

    // Fill Client Data
    await page.getByPlaceholder('Ej: Constructora ABC S.A.C.').fill('Test Client Corp');
    await page.getByPlaceholder('11 dígitos').fill('20123456789');

    // Select Service (Electricidad)
    await page.locator('button').filter({ hasText: 'Electricidad' }).click();

    // Select Industry (Construcción)
    await page.locator('button').filter({ hasText: 'Construcción' }).click();

    // Fill Description
    await page.getByPlaceholder('Describe el proyecto a cotizar detalladamente...').fill('Solicito cotización para cableado de 5 oficinas administrativas.');

    // 4. Start Chat
    await page.getByRole('button', { name: 'Comenzar Chat con Vista Previa' }).click();

    // 5. Interact with Chat
    // Verify we are in Step 2
    await expect(page.getByText('Paso 2')).toBeVisible();
    await expect(page.getByText('Co-Creación con IA')).toBeVisible();

    // Type message
    /* Use specific placeholder for chat input to avoid strict mode violation with form textarea */
    const chatInput = page.getByPlaceholder('Pregúntale a PILi...');
    await chatInput.fill('Hola, por favor agrega 10 puntos de red Cat6.');
    await page.locator('button').filter({ hasText: 'Send' }).click();

    // Verify message appears in chat
    await expect(page.getByText('Hola, por favor agrega 10 puntos de red Cat6.')).toBeVisible();

    // 6. Proceed to Editor
    await page.getByRole('button', { name: 'Finalizar Edición' }).click();

    // 7. Verify Editor & Export
    // Verify we are in Step 3
    await expect(page.getByText('Vista Previa del Documento')).toBeVisible();

    // Excel Export
    // Using verify download event
    const downloadPromise = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Descargar Excel' }).click();
    const download = await downloadPromise;

    // Verify filename
    console.log('Downloaded filename:', download.suggestedFilename());
    expect(download.suggestedFilename()).toContain('Cotizacion_Test Client Corp.xlsx');
});
