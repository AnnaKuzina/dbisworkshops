CREATE OR REPLACE PACKAGE gift_category_package IS
    TYPE gift_category_row IS RECORD (
        c_name gift_category.category_category_name%TYPE
    );
    TYPE gift_category_table IS
        TABLE OF gift_category_row;
    PROCEDURE add_category_to_gift (
        status   OUT      VARCHAR2,
        c_name   IN       gift_category.category_category_name%TYPE,
        g_name   IN       gift_category.gift_gift_name%TYPE
    );

    PROCEDURE del_category_from_gift (
        status   OUT      VARCHAR2,
        g_name   IN       gift_category.gift_gift_name%TYPE
    );

    FUNCTION get_gift_category_list (
        g_name   IN       gift_category.gift_gift_name%TYPE
    ) RETURN gift_category_table
        PIPELINED;

END gift_category_package;
/

CREATE OR REPLACE PACKAGE BODY gift_category_package IS

    PROCEDURE add_category_to_gift (
        status   OUT      VARCHAR2,
        c_name   IN       gift_category.category_category_name%TYPE,
        g_name   IN       gift_category.gift_gift_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        INSERT INTO gift_category (
            category_category_name,
            gift_gift_name
        ) VALUES (
            c_name,
            g_name
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_category_to_gift;

    PROCEDURE del_category_from_gift (
        status   OUT      VARCHAR2,
        g_name   IN       gift_category.gift_gift_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        DELETE FROM gift_category
        WHERE
            gift_category.gift_gift_name = g_name;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END del_category_from_gift;

    FUNCTION get_gift_category_list (
        g_name   IN       gift_category.gift_gift_name%TYPE
    ) RETURN gift_category_table
        PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT DISTINCT
                category_category_name
            FROM
                gift_category
            WHERE
                gift_category.gift_gift_name = g_name
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;
    END get_gift_category_list;

END gift_category_package;