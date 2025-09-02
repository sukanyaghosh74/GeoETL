-- sample_data/seed.sql
INSERT INTO products (provider, collection, product_id, acquisition_time, cloud_pct, properties, footprint)
VALUES ('mock', 'sentinel-2', 'MOCK_001', '2024-01-01T00:00:00', 5.0, '{}', ST_GeomFromText('POLYGON((12 48, 12.1 48, 12.1 48.1, 12 48.1, 12 48))', 4326));
