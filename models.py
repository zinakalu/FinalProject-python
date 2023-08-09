from database import db



user_questions = db.Table('user_questions',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'))
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    questions = db.relationship('Question', secondary=user_questions, backref='user', cascade='all')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

    def __repr__(self):
        return f'<User {self.username}>'



class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)


    def __repr__(self):
        return f'<Question {self.content}>'