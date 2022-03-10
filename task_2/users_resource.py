from flask import make_response, jsonify
from flask_restful import Resource, abort

from task_1.data import db_session
from task_1.data.users import User
from task_1.parsers import parser_editing_user, parser_add_user


class BaseUsersResourceClass(Resource):

    def abort_if_users_not_found(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if not user:
            abort(404, message=f'User {user_id} not found')


class UsersResource(BaseUsersResourceClass):

    def get(self, user_id):
        all_attributes = (
            'surname',
            'name',
            'age',
            'position',
            'speciality',
            'address',
            'email',
            'hashed_password'
        )

        self.abort_if_users_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        return jsonify({'user': user.to_dict(only=all_attributes)})

    def delete(self, user_id):
        self.abort_if_users_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()
        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'info': ' successfully'})

    def post(self, user_id):
        self.abort_if_users_not_found(user_id)
        args = parser_editing_user.parse_args()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == user_id).first()

        user.surname = args.get('surname', user.surname)
        user.name = args.get('name', user.name)
        user.age = args.get('age', user.age)
        user.position = args.get('position', user.position)
        user.speciality = args.get('speciality', user.speciality)
        user.address = args.get('address', user.address)
        user.email = args.get('email', user.email)
        user.set_password(args.get('password', user.password))
        db_sess.add(user)
        db_sess.commit()

        return jsonify({'info': ' successfully'})


class UsersListResource(Resource):
    def get(self):
        all_attributes = (
            'id',
            'surname',
            'name',
            'age',
            'position',
            'speciality',
            'address',
            'email',
            'hashed_password',
            'modified_date'
        )
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify(
            {'users': [item.to_dict(only=all_attributes) for item in users]}
        )

    def post(self):
        args = parser_add_user.parse_args()
        db_sess = db_session.create_session()

        user = User()
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        user.set_password(args['password'])
        db_sess.add(user)
        db_sess.commit()

        return jsonify({'info': ' successfully'})
