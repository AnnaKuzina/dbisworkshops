CREATE OR REPLACE PACKAGE user_package IS
    PROCEDURE add_user (
        status       OUT          VARCHAR2,
        u_login      IN           user_info.user_login%TYPE,
        u_name       IN           user_info.user_name%TYPE,
        u_password   IN           user_info.user_password%TYPE
    );

    FUNCTION login (
        u_login      user_info.user_login%TYPE,
        u_password   user_info.user_password%TYPE
    ) RETURN NUMBER;

END user_package;
/

CREATE OR REPLACE PACKAGE BODY user_package IS

    PROCEDURE add_user (
        status       OUT          VARCHAR2,
        u_login      IN           user_info.user_login%TYPE,
        u_name       IN           user_info.user_name%TYPE,
        u_password   IN           user_info.user_password%TYPE
    ) IS
        PRAGMA autonomous_transaction;
    BEGIN
        INSERT INTO user_info (
            user_login,
            user_name,
            user_password
        ) VALUES (
            u_login,
            u_name,
            u_password
        );

        COMMIT;
        status := 'ok';
    EXCEPTION
        WHEN dup_val_on_index THEN
            status := 'Користувач з таким логіном уже існує';
        WHEN OTHERS THEN
            status := sqlerrm;
    END add_user;

    FUNCTION login (
        u_login      user_info.user_login%TYPE,
        u_password   user_info.user_password%TYPE
    ) RETURN NUMBER IS
        res   NUMBER(1);
    BEGIN
        SELECT
            COUNT(*)
        INTO res
        FROM
            user_info
        WHERE
            user_info.user_login = u_login
            AND user_info.user_password = u_password;

        return(res);
    END login;

END user_package;
/