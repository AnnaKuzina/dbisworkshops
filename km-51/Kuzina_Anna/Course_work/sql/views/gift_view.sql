CREATE OR REPLACE VIEW gift_view AS
    SELECT
        gift_name,
        gift_price,
        gift_desc
    FROM
        gift
    WHERE
        gift.gift_deleted IS NULL;

CREATE OR REPLACE TRIGGER trg_delete_gift INSTEAD OF
    DELETE ON gift_view
    FOR EACH ROW
DECLARE
    PRAGMA autonomous_transaction;
BEGIN
    UPDATE gift
    SET
        gift.gift_deleted = systimestamp
    WHERE
        gift.gift_name = :old.gift_name;

    COMMIT;
END;