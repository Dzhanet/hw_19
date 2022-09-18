from dao.model.user import User


class UserDAO:

    def __init__(self, session):
        self.session = session

    def get_all_users(self):
        """ Возвращает всех пользователей """
        return self.session.query(User).all()

    def get_one_user(self, pk):
        """ Возвращает пользователя по ID """
        return self.session.query(User).get_or_404(pk)

    def get_user_by_username(self, username):
        """Получить пользователя по имени"""
        return self.session.query(User).filter(User.username == username).first()

    def create(self, user_d):
        """" Добавляет пользователя """
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, user_d):
        """ Обновляет данные пользователя """
        user = self.get_one_user(user_d.get("id"))
        user.username = user_d.get("username")
        user.role = user_d.get("role")
        user.password = user_d.get("password")

        self.session.add(user)
        self.session.commit()

    def delete(self, bid):
        """ Удаляет пользователя """
        movie = self.get_one_user(bid)
        self.session.delete(movie)
        self.session.commit()
