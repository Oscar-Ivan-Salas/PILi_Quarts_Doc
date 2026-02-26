-- SQL Setup for Supabase - N04 Binary Factory
-- =============================================

-- 1. Create a table for Document Templates (Metadata)
CREATE TABLE IF NOT EXISTS n04_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,
    category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create a bucket for Storing Generated Documents (Binary Storage)
-- Note: This is usually done via Supabase Dashboard UI, but here is the manual setup.
-- Bucket Name: "binary-factory-storage"

-- 3. Policy to allow public read (Adjust for production)
-- CREATE POLICY "Public Access" ON storage.objects FOR SELECT USING (bucket_id = 'binary-factory-storage');

-- 4. Initial seed for templates
INSERT INTO n04_templates (name, category) VALUES 
('COTIZACION_SIMPLE', 'Cotizaciones'),
('COTIZACION_COMPLEJA', 'Cotizaciones'),
('PROYECTO_SIMPLE', 'Proyectos'),
('PROYECTO_COMPLEJO_PMI', 'Proyectos'),
('INFORME_TECNICO', 'Informes'),
('INFORME_EJECUTIVO_APA', 'Informes')
ON CONFLICT (name) DO NOTHING;
