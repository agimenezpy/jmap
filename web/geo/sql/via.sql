CREATE INDEX idx_via ON via_transito USING gin(to_tsvector('spanish', translate(upper(nombre), '������', 'AEIOUU')));
