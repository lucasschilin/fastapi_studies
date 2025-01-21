from http import HTTPStatus

from fastapi import HTTPException

from fastapi_studies.schemas.user import UserDB, UserSchema

database = {}
database_ids = []


def controller_create_user(user: UserSchema):
    for id, dados in database.items():
        if dados.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Nome de usuário não disponível.',
            )
        elif dados.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Endereço de e-mail não disponível.',
            )

    user_with_id = UserDB(
        id=(1 if len(database_ids) == 0 else database_ids[-1] + 1),
        **user.model_dump(),
    )

    database[user_with_id.id] = user_with_id
    database_ids.append(user_with_id.id)

    return user_with_id


def controller_get_users():
    users = []
    for id, dados in database.items():
        users.append(dados)

    return {'users': users}


def controller_get_user(id: int):
    if id not in database:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    return database[id]


def controller_update_user(id: int, user: UserSchema):
    if id not in database:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    user_with_id = UserDB(
        id=id,
        **user.model_dump(),
    )
    database[id] = user_with_id

    return user_with_id


def controller_delete_user(id: int):
    if id not in database:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado.',
        )

    database.pop(id, None)

    return {'message': 'Usuário deletado.'}
