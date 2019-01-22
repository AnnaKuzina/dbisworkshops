CREATE OR REPLACE PACKAGE category_package IS
    PROCEDURE add_category (
        status   OUT      VARCHAR2,
        c_name   IN       category_.category_name%TYPE
    );

    PROCEDURE del_category (
        status   OUT      VARCHAR2,
        c_name   IN       category_.category_name%TYPE
    );

END category_package;
/

CREATE OR REPLACE PACKAGE BODY category_package IS

    PROCEDURE add_category (
        status   OUT      VARCHAR2,
        c_name   IN       category_.category_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        INSERT INTO category_ ( category_name ) VALUES ( c_name );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN dup_val_on_index THEN
            status := 'Така категорія уже існує';
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_category;

    PROCEDURE del_category (
        status   OUT      VARCHAR2,
        c_name   IN       category_.category_name%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        DELETE FROM category_view
        WHERE
            category_view.category_name = c_name;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END del_category;

END category_package;