
import { test, expect } from '@playwright/test';

test('Verify Excel Export Endpoint', async ({ request }) => {
    // 1. Send a POST request to /api/generate/excel
    const response = await request.post('http://localhost:8003/api/generate/excel', {
        data: {
            title: "Test Project",
            type: "cotizacion-simple",
            data: {
                cliente: { nombre: "Test Client", ruc: "12345678901" },
                proyecto: "Test Project",
                items: [
                    { descripcion: "Item 1", cantidad: 10, precio_unitario: 50 },
                    { descripcion: "Item 2", cantidad: 5, precio_unitario: 100 }
                ]
            }
        }
    });

    // 2. Check Status
    expect(response.status()).toBe(200);

    // 3. Check Headers
    const headers = response.headers();
    expect(headers['content-type']).toContain('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    expect(headers['content-disposition']).toContain('attachment');
    expect(headers['content-disposition']).toContain('.xlsx');

    // 4. Check Body Size (Should be > 0)
    const body = await response.body();
    expect(body.length).toBeGreaterThan(0);
});
