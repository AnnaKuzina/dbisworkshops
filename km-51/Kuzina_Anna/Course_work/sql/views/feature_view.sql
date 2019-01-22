CREATE OR REPLACE VIEW feature_view AS
    SELECT
        feature_name
    FROM
        feature
    WHERE
        feature.feature_deleted IS NULL;

CREATE OR REPLACE TRIGGER trg_delete_feature INSTEAD OF
    DELETE ON feature_view
    FOR EACH ROW
DECLARE
    PRAGMA autonomous_transaction;
BEGIN
    UPDATE feature
    SET
        feature.feature_deleted = systimestamp
    WHERE
        feature.feature_name = :old.feature_name;

    COMMIT;
END;