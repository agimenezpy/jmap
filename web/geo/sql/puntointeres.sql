CREATE INDEX idx_poi ON punto_interes USING gin(to_tsvector('spanish', translate(nombre, '�����', 'AEIOU')));