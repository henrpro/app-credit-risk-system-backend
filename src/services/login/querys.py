
query_get_user = lambda database, username: f"""

    SELECT
        cdUser,
        cdPassword,
        dsProfile
    FROM {database}.dbo.tCRS_0001_UsuarioCadastro A
    LEFT JOIN {database}.dbo.tCRS_0002_ProfileAcesso B ON A.idProfile = B.idProfile
    WHERE cdUser = '{username}'
    
"""
