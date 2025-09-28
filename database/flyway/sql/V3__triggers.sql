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