CREATE OR REPLACE PACKAGE gift_package IS
    PROCEDURE add_gift (
        status    OUT       VARCHAR2,
        g_name    IN        gift.gift_name%TYPE,
        g_price   IN        gift.gift_price%TYPE,
        g_desc    IN        gift.gift_desc%TYPE
    );

    PROCEDURE del_gift (
        status   OUT      VARCHAR2,
        g_name   IN       gift.gift_name%TYPE
    );

    PROCEDURE update_gift (
        status    OUT       VARCHAR2,
        g_name    IN        gift.gift_name%TYPE,
        g_price   IN        gift.gift_price%TYPE,
        g_desc    IN        gift.gift_desc%TYPE
    );

END gift_package;
/

CREATE OR REPLACE PACKAGE BODY gift_package IS

    PROCEDURE add_gift (
        status    OUT       VARCHAR2,
        g_name    IN        gift.gift_name%TYPE,
        g_price   IN        gift.gift_price%TYPE,
        g_desc    IN        gift.gift_desc%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        INSERT INTO gift (
            gift_name,
            gift_price,
            gift_desc
        ) VALUES (
            g_name,
            g_price,
            g_desc
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN dup_val_on_index THEN
            status := 'Такий подарунок уже існує';
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_gift;

    PROCEDURE del_gift (
        status   OUT      VARCHAR2,
        g_name   IN       gift.gift_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        DELETE FROM gift_view
        WHERE
            gift_view.gift_name = g_name;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END del_gift;

    PROCEDURE update_gift (
        status    OUT       VARCHAR2,
        g_name    IN        gift.gift_name%TYPE,
        g_price   IN        gift.gift_price%TYPE,
        g_desc    IN        gift.gift_desc%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        UPDATE gift
        SET
            gift.gift_price = g_price,
            gift.gift_desc = g_desc
        WHERE
            gift.gift_name = g_name;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            status := sqlerrm;
    END update_gift;

END gift_package;