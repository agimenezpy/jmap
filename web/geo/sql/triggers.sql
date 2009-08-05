BEGIN;
/**
 * Actualización de Area
 */
CREATE OR REPLACE FUNCTION actualiza_area() RETURNS trigger AS $actualiza_area$
BEGIN
    NEW.area = cast(area(NEW.the_geom) as integer);
    RETURN NEW;
END;
$actualiza_area$ LANGUAGE plpgsql;

CREATE TRIGGER actualiza_area BEFORE INSERT OR UPDATE ON area_interes FOR EACH ROW EXECUTE PROCEDURE actualiza_area();

/**
 * Actualización de Etiquetas de Via Transito
 */
CREATE OR REPLACE FUNCTION reunir_trazos() RETURNS trigger AS $reunir_trazos$
DECLARE
    referencia_id INTEGER;
BEGIN
    IF TG_OP = 'UPDATE'
    THEN
        IF NEW.ref_id = OLD.ref_id AND NEW.the_geom <> OLD.the_geom
        THEN
            UPDATE via_transito
            SET the_geom = (SELECT multi(linemerge(collect(the_geom))) from via_trazo where ref_id = NEW.ref_id)
            WHERE id = NEW.ref_id;
        ELSIF NEW.ref_id <> OLD.ref_id
        THEN
            UPDATE via_transito
            SET the_geom = (SELECT multi(linemerge(collect(the_geom))) from via_trazo where ref_id = NEW.ref_id)
            WHERE id = NEW.ref_id;
            
            UPDATE via_transito
            SET the_geom = (SELECT multi(linemerge(collect(the_geom))) from via_trazo where ref_id = OLD.ref_id)
            WHERE id = OLD.ref_id;
        END IF;
    ELSE
        IF TG_OP = 'INSERT'
        THEN
            referencia_id := NEW.ref_id;
        ELSE
            referencia_id := OLD.ref_id;
        END IF;
        
        UPDATE via_transito
        SET the_geom = (SELECT multi(linemerge(collect(the_geom))) FROM via_trazo WHERE ref_id = referencia_id)
        WHERE id = referencia_id;
    END IF;
    RETURN NEW;
END;
$reunir_trazos$ LANGUAGE plpgsql;

CREATE TRIGGER reunir_trazos AFTER INSERT OR UPDATE OR DELETE ON via_trazo FOR EACH ROW EXECUTE PROCEDURE reunir_trazos();

END;