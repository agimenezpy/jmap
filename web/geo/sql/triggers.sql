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

DROP TRIGGER IF EXISTS actualiza_area ON area_interes;
CREATE TRIGGER actualiza_area BEFORE INSERT OR UPDATE ON area_interes FOR EACH ROW EXECUTE PROCEDURE actualiza_area();

/**
 * Actualización de Etiquetas de Via Transito
 */
CREATE OR REPLACE FUNCTION mezclar_trazos(referencia INTEGER) RETURNS VOID AS $mezclar_trazos$
DECLARE
    geom record;
BEGIN
    SELECT multi(linemerge(collect(the_geom))) AS the_geom INTO geom FROM via_trazo WHERE ref_id = referencia;
    UPDATE via_transito SET the_geom = geom.the_geom WHERE id = referencia;
END;
$mezclar_trazos$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION reunir_trazos() RETURNS trigger AS $reunir_trazos$
DECLARE
    referencia_id INTEGER;
BEGIN
    IF TG_OP = 'UPDATE'
    THEN
        IF NEW.ref_id = OLD.ref_id AND NEW.the_geom <> OLD.the_geom
        THEN
            PERFORM mezclar_trazos(NEW.ref_id);
        ELSIF NEW.ref_id <> OLD.ref_id
        THEN
            PERFORM mezclar_trazos(NEW.ref_id);
            PERFORM mezclar_trazos(OLD.ref_id);
        END IF;
    ELSE
        IF TG_OP = 'INSERT'
        THEN
            referencia_id := NEW.ref_id;
        ELSE
            referencia_id := OLD.ref_id;
        END IF;

        PERFORM mezclar_trazos(referencia_id);
    END IF;
    RETURN NEW;
END;
$reunir_trazos$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS reunir_trazos ON via_trazo;
CREATE TRIGGER reunir_trazos AFTER INSERT OR UPDATE OR DELETE ON via_trazo FOR EACH ROW EXECUTE PROCEDURE reunir_trazos();

END;