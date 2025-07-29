from app import app
from model import User as UserModel


# Ресурсы для пользователей
class User(Resource):
    def get(self, user_id):
        with app.app_context():
            # Ищем пользователя по id
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                response = jsonify({"message": "User not found"})
                response.status_code = 404
                return response 
            # Возвращаем данные автора в формате JSON
            return jsonify(user.as_dict())
    
    def post(self, user_id):
        with app.app_context():
            # Ищем пользователя по id
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                response = jsonify({"message": "User not found"})
                response.status_code = 404
                return response 
            # Получаем данные для создания пользователя
            new_user = request.get_json()
            new_user["id"] = book_id
            # Создаем новую книгу
            new_book = BookModel(**new_book)
            try:
                db.session.add(new_book)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error adding user"})
                response.status_code = 500
                return response
            # Возвращаем новые данные пользователя
            response = jsonify(new_book.as_dict())
            response.status_code = 200
            return response
    
    @jwt_required()
    def put(self, user_id):
        with app.app_context():
            # Ищем пользователя по id
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                response = jsonify({"message": "User not found"})
                response.status_code = 404
                return response
            # Получаем данные для обновления
            updated_data = request.get_json()
            # Обновляем поля пользователя, если они предоставлены
            user.name = updated_data.get("name", user.name)
            user.login = updated_data.get("login", user.login)
            user.password = updated_data.get("password", user.password)
            # user.avatar = updated_data.get("avatar", user.avatar)
            user.title = updated_data.get("title", user.title)
            user.email = updated_data.get("email", user.email)
            # Пытаемся зафиксировать изменения в базе данных
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error updating user"})
                response.status_code = 500
                return response
            # Возвращаем обновленные данные пользователя
            response = jsonify(user.as_dict())
            response.status_code = 200
            return response
    
    @jwt_required()
    def delete(self, user_id):
        with app.app_context():
            # Ищем пользователя по id
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                response = jsonify({"message": "User not found"})
                response.status_code = 404
                return response
            # Удаляем запись из базы данных
            try:
                UserModel.query.filter_by(id=user_id).delete()
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                response = jsonify({"message": "Error deleting user"})
                response.status_code = 500
                return response
            # Возвращаем успешное сообщение
            response = jsonify({"message": "User deleted"})
            response.status_code = 200
            return response
