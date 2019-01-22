CREATE OR REPLACE VIEW category_view AS
    SELECT
        category_name
    FROM
        category_
    WHERE
        category_.category_deleted IS NULL;

CREATE OR REPLACE TRIGGER trg_delete_category INSTEAD OF
    DELETE ON category_view
    FOR EACH ROW
DECLARE
    PRAGMA autonomous_transaction;
BEGIN
    UPDATE category_
    SET
        category_.category_deleted = systimestamp
    WHERE
        category_.category_name = :old.category_name;

    COMMIT;
END;