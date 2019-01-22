CREATE OR REPLACE PACKAGE feature_package IS
    PROCEDURE add_feature (
        status   OUT      VARCHAR2,
        f_name   IN       feature.feature_name%TYPE
    );

    PROCEDURE del_feature (
        status   OUT      VARCHAR2,
        f_name   IN       feature.feature_name%TYPE
    );

    PROCEDURE replace_feature (
        status   OUT      VARCHAR2,
        f_name   IN       feature.feature_name%TYPE
    );


END feature_package;
/

CREATE OR REPLACE PACKAGE BODY feature_package IS

    PROCEDURE add_feature (
        status   OUT      VARCHAR2,
        f_name   IN       feature.feature_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        INSERT INTO feature ( feature_name ) VALUES ( f_name );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN dup_val_on_index THEN
            status := 'Така характеристика уже існує';
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_feature;

    PROCEDURE del_feature (
        status   OUT      VARCHAR2,
        f_name   IN       feature.feature_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        DELETE FROM feature_view
        WHERE
            feature_view.feature_name = f_name;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END del_feature;

    PROCEDURE replace_feature (
        status   OUT      VARCHAR2,
        f_name   IN       feature.feature_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        UPDATE feature
        SET
            FEATURE.FEATURE_DELETED = NULL
        where
            feature_view.feature_name = f_name;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END replace_feature;
END feature_package;