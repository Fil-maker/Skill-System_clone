from flask import jsonify, g

from api import app
from api.auth import basic_auth, token_auth


@app.route('/api/login', methods=['POST'])
@basic_auth.login_required
# Путь получает в заголовках запроса логин и пароль пользователя (декоратор @basic.auth.login_required)
# и, если данные верны, возвращает токен. Чтобы защитить маршруты API с помощью токенов, необходимо
# добавить декоратор @token_auth.login_required
def get_token():
    token = g.current_user.get_token()
    g.db_session.commit()
    return jsonify({'success': True, 'authToken': {'token': token,
                                                   'expires': str(g.current_user.token_expiration)}})


@app.route('/api/logout', methods=['POST'])
@token_auth.login_required
# Отзыв токена
def revoke_token():
    g.current_user.revoke_token()
    g.db_session.commit()
    g.current_user = None
    g.db_session = None
    return jsonify({'success': True})
