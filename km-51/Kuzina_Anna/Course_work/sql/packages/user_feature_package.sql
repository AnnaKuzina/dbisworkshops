CREATE OR REPLACE PACKAGE user_feature_package IS
    TYPE user_feature_row IS RECORD (
        f_name user_feature.feature_feature_name%TYPE
    );
    TYPE user_feature_table IS
        TABLE OF user_feature_row;
    PROCEDURE add_feature_to_user (
        status    OUT       VARCHAR2,
        f_name    IN        user_feature.feature_feature_name%TYPE,
        u_login   IN        user_feature.user_info_user_login%TYPE
    );

    PROCEDURE del_feature_from_user (
        status    OUT       VARCHAR2,
        f_name    IN        user_feature.feature_feature_name%TYPE,
        u_login   IN        user_feature.user_info_user_login%TYPE
    );

    FUNCTION get_user_feature_list (
        u_login   IN        user_feature.user_info_user_login%TYPE
    ) RETURN user_feature_table
        PIPELINED;

END user_feature_package;
/

CREATE OR REPLACE PACKAGE BODY user_feature_package IS

    PROCEDURE add_feature_to_user (
        status    OUT       VARCHAR2,
        f_name    IN        user_feature.feature_feature_name%TYPE,
        u_login   IN        user_feature.user_info_user_login%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        INSERT INTO user_feature (
            feature_feature_name,
            user_info_user_login
        ) VALUES (
            f_name,
            u_login
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_feature_to_user;

    PROCEDURE del_feature_from_user (
        status    OUT       VARCHAR2,
        f_name    IN        user_feature.feature_feature_name%TYPE,
        u_login   IN        user_feature.user_info_user_login%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        DELETE FROM user_feature
        WHERE
            user_feature.feature_feature_name = f_name
            AND user_feature.user_info_user_login = u_login;

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN OTHERS THEN
            ROLLBACK;
            status := sqlerrm;
    END del_feature_from_user;

    FUNCTION get_user_feature_list (
        u_login   IN        user_feature.user_info_user_login%TYPE
    ) RETURN user_feature_table
        PIPELINED
    IS
    BEGIN
        FOR curr IN (
            SELECT DISTINCT
                feature_feature_name
            FROM
                user_feature
            WHERE
                user_feature.user_info_user_login = u_login
        ) LOOP
            PIPE ROW ( curr );
        END LOOP;
    END get_user_feature_list;

END user_feature_package;