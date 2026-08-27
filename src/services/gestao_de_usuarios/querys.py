# _______________________________ Geral _______________________________

query_get_usuarios_cadastrados = lambda database: f"""

    SELECT DISTINCT
        A.cdUser,
        A.dsNome,
        B.dsProfile
    FROM {database}.dbo.tCRS_0001_UsuarioCadastro A
    LEFT JOIN {database}.dbo.tCRS_0002_ProfileAcesso B ON A.idProfile = B.idProfile

"""

query_get_usuario = lambda database, user: f"""

    SELECT 
        A.cdUser,
        A.dsNome,
        A.cdPassword,
        B.dsProfile,
        A.dsAlcadaAprovador,
        A.vlPesoAprovacao
    FROM {database}.dbo.tCRS_0001_UsuarioCadastro A
    LEFT JOIN {database}.dbo.tCRS_0002_ProfileAcesso B ON A.idProfile = B.idProfile
    WHERE A.cdUser = '{user}'

"""

query_get_profiles = lambda database: f"""

    SELECT 
        idProfile,
        dsProfile
    FROM {database}.dbo.tCRS_0002_ProfileAcesso

"""

query_get_id_profile = lambda database, profile: f"""

    SELECT idProfile
    FROM {database}.dbo.tCRS_0002_ProfileAcesso
    WHERE dsProfile = '{profile}'

"""

# _______________________________ Insert _______________________________

query_insert_usuario = lambda database, user, nome, password, idprofile, aprovador, peso: f"""

    INSERT INTO {database}.dbo.tCRS_0001_UsuarioCadastro (
        cdUser,
        dsNome,
        cdPassword,
        idProfile,
        dsAlcadaAprovador,
        vlPesoAprovacao
    )
    VALUES (
        '{user}',
        '{nome}',
        '{password}',
        {idprofile},
        {f"'{aprovador}'" if aprovador is not None else 'NULL'},
        {peso if peso is not None else 'NULL'}
    )

"""

# _______________________________ Delete _______________________________

query_delete_usuario = lambda database, user: f"""

    DELETE 
    FROM {database}.dbo.tCRS_0001_UsuarioCadastro
    WHERE cdUser = '{user}'

"""