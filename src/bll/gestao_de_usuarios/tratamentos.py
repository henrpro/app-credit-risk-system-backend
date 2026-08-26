# Importações do projeto
from services.gestao_de_usuarios.insumos import InsumosGestaoUsuarios


def realizar_cadastro_usuario(database: str, payload: dict):

    """
    Função que cadastra um novo usuário. Se o usuário já existir ele será deletado e inserido novamente.
    """

    try:
        # Começamos extraindo os dados do payload
        user = payload.get('cdUser', '').strip()
        nome = payload.get('dsNome', '').strip()
        password = payload.get('cdPassword', '').strip()
        ds_profile = payload.get('dsProfile', '').strip()
        aprovador = payload.get('dsAlcadaAprovador') or None
        peso = float(payload['vlPesoAprovacao']) if payload.get('vlPesoAprovacao') not in (None, '') else None

        # Buscamos o idProfile 
        id_profile = InsumosGestaoUsuarios.get_id_profile(database, ds_profile)

        # Se o usuário já existir, deletamos
        df_existente = InsumosGestaoUsuarios.get_usuario(database, user)
        if not df_existente.empty:
            InsumosGestaoUsuarios.execute_delete_usuario(database, user)

        # Cadastra o novo usuário
        InsumosGestaoUsuarios.execute_insert_usuario(
            database=database,
            nome=nome,
            user=user,
            password=password,
            idprofile=id_profile,
            aprovador=aprovador,
            peso=peso
        )
    except Exception as e:
        raise e