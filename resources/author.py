# # Ресурсы для авторов
# class AuthorList(Resource):
#     def get(self):
#         authors = AuthorModel.query.limit(PAGING_LIMIT).all()
#         author_list = list()
#         for author in authors:
#             author_list.append(author.as_dict())
#         return jsonify(author_list)

#     @jwt_required()
#     def post(self):
#         authors = AuthorModel.query.all()
#         new_author = request.get_json()
#         name = new_author.get("name")
#         if not name:
#             response = jsonify({"message": "Author`s Name required"})
#             response.status_code = 400
#             return response
#         new_author = {
#             "name_eng": new_author.get("name_eng"),
#             "name": name,
#         }

#         with app.app_context():
#             author_obj = AuthorModel.query.filter_by(name=name).first()
#             if author_obj:
#                 response = jsonify({"message": "Author`s this Name already exists"})
#                 response.status_code = 400
#                 return response
#             # Создаем новый объект автор и добавляем его в базу данных
#             author_obj = AuthorModel(**new_author)
#             try:
#                 db.session.add(author_obj)
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 response = jsonify({"message": "Error adding author"})
#                 response.status_code = 500
#                 return response
        
#         author_obj = AuthorModel.query.filter_by(name=name).first()
#         # Возвращаем данные о добавленном авторе
#         response = jsonify(author_obj.as_dict())
#         response.status_code = 200
#         return response


# class Author(Resource):
#     def get(self, author_id):
#         with app.app_context():
#             # Ищем автора по id
#             author = AuthorModel.query.filter_by(id=author_id).first()
#             if not author:
#                 response = jsonify({"message": "Author not found"})
#                 response.status_code = 404
#                 return response 
#             # Возвращаем данные автора в формате JSON
#             return jsonify(author.as_dict())

#     @jwt_required()
#     def put(self, author_id):
#         with app.app_context():
#             # Ищем книгу по id
#             author = AuthorModel.query.filter_by(id=author_id).first()
#             if not author:
#                 response = jsonify({"message": "Author not found"})
#                 response.status_code = 404
#                 return response
#             # Получаем данные для обновления
#             updated_data = request.get_json()
#             # Обновляем поля книги, если они предоставлены
#             author.name = updated_data.get("name", author.name)
#             author.name_eng = updated_data.get("name_eng", author.name_eng)
#             # Пытаемся зафиксировать изменения в базе данных
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 response = jsonify({"message": "Error updating author"})
#                 response.status_code = 500
#                 return response
#             # Возвращаем обновленные данные книги
#             response = jsonify(author.as_dict())
#             response.status_code = 200
#             return response

#     @jwt_required()
#     def delete(self, author_id):
#         with app.app_context():
#             # Ищем книгу по id
#             author = AuthorModel.query.filter_by(id=author_id).first()
#             if not author:
#                 response = jsonify({"message": "Author not found"})
#                 response.status_code = 404
#                 return response
#             # Удаляем запись из базы данных
#             try:
#                 AuthorModel.query.filter_by(id=author_id).delete()
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 response = jsonify({"message": "Error deleting author"})
#                 response.status_code = 500
#                 return response
#             # Возвращаем успешное сообщение
#             response = jsonify({"message": "Author deleted"})
#             response.status_code = 200
#             return response
