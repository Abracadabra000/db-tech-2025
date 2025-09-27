CREATE OR REPLACE FUNCTION set_modified_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_date := now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    t TEXT;
BEGIN
    FOREACH t IN ARRAY ARRAY['customer','category','product','product_category','deal','deal_item'] LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS trg_%s_set_modified_date ON %I', t, t);
        EXECUTE format('CREATE TRIGGER trg_%s_set_modified_date BEFORE UPDATE ON %I FOR EACH ROW EXECUTE FUNCTION set_modified_date()', t, t);
    END LOOP;
END$$;

CREATE OR REPLACE FUNCTION recalc_deal_total()
RETURNS TRIGGER AS $$
DECLARE
    affected_deal_id INT;
BEGIN
    affected_deal_id := COALESCE(NEW.deal_id, OLD.deal_id);
    UPDATE deal d
    SET total_amount = COALESCE((
        SELECT SUM(di.quantity * di.price)
        FROM deal_item di
        WHERE di.deal_id = affected_deal_id
    ), 0)
    WHERE d.id = affected_deal_id;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_recalc_deal_total_insert ON deal_item;
DROP TRIGGER IF EXISTS trg_recalc_deal_total_update ON deal_item;
DROP TRIGGER IF EXISTS trg_recalc_deal_total_delete ON deal_item;

CREATE TRIGGER trg_recalc_deal_total_insert
AFTER INSERT ON deal_item
FOR EACH ROW EXECUTE FUNCTION recalc_deal_total();

CREATE TRIGGER trg_recalc_deal_total_update
AFTER UPDATE ON deal_item
FOR EACH ROW EXECUTE FUNCTION recalc_deal_total();

CREATE TRIGGER trg_recalc_deal_total_delete
AFTER DELETE ON deal_item
FOR EACH ROW EXECUTE FUNCTION recalc_deal_total();

