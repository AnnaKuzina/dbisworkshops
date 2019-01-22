CREATE OR REPLACE PACKAGE gift_feature_package IS
    TYPE gift_feature_row IS RECORD (
        f_name gift_feature.feature_feature_name%TYPE
    );
    TYPE gift_feature_table IS
        TABLE OF gift_feature_row;
    PROCEDURE add_feature_to_gift (
        status   OUT      VARCHAR2,
        f_name   IN       gift_feature.feature_feature_name%TYPE,
        g_name   IN       gift_feature.gift_gift_name%TYPE
    );

    PROCEDURE del_feature_from_gift (
        status   OUT      VARCHAR2,
        g_name   IN       gift_feature.gift_gift_name%TYPE
    );

    FUNCTION get_gift_feature_list (
        g_name   IN       gift_feature.gift_gift_name%TYPE
    ) RETURN gift_feature_table
        PIPELINED;

END gift_feature_package;
/

CREATE OR REPLACE PACKAGE BODY gift_feature_package IS

    PROCEDURE add_feature_to_gift (
        status   OUT      VARCHAR2,
        f_name   IN       gift_feature.feature_feature_name%TYPE,
        g_name   IN       gift_feature.gift_gift_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        INSERT INTO gift_feature (
            feature_feature_name,
            gift_gift_name
        ) VALUES (
            f_name,
            g_name
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_feature_to_gift;

    PROCEDURE del_feature_from_gift (
        status   OUT      VARCHAR2,
        g_name   IN       gift_feature.gift_gift_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        DELETE FROM gift_feature
        WHERE
            gift_feature.gift_gift_name = g_name;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END del_feature_from_gift;

    FUNCTION get_gift_feature_list (
        g_name   IN       gift_feature.gift_gift_name%TYPE
    ) RETURN gift_feature_table
        PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT DISTINCT
                feature_feature_name
            FROM
                gift_feature
            WHERE
                gift_feature.gift_gift_name = g_name
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;
    END get_gift_feature_list;

END gift_feature_package;