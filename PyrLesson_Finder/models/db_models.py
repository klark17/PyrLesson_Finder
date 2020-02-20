from .meta import Base
import bcrypt
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Table, Boolean, Sequence, Date, Time
from sqlalchemy.orm import relationship, backref


lessons = Table('lessons',
				Base.metadata,
				Column('userParticipantId', Integer, ForeignKey('user.id')),
				Column('lessonId', Integer, ForeignKey('lesson.id')),
				)

depLessons = Table('depLessons',
				Base.metadata,
				Column('participantId', Integer, ForeignKey('participant.id')),
				Column('lessonId', Integer, ForeignKey('lesson.id')),
				)

hosting = Table('hosting',
				Base.metadata,
				Column('organizationId', Integer, ForeignKey('organization.id')),
				Column('lessonId', Integer, ForeignKey('lesson.id')),
				)

# TODO: DB Browser for SQLite
# TODO: email Lisa to meet
# TODO: make sure you look into how sessions are handled in both frameworks
class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	active = Column(Boolean(), nullable=False)
	fName = Column(String(50), nullable=False)
	lName = Column(String(50), nullable=False)
	email = Column(String(50), unique=True, nullable=False)
	birthday = Column(Date, nullable=False)
	username = Column(String(30), unique=True, nullable=False)
	password = Column(String(60), nullable=False)
	lessons = relationship('Lesson', secondary=lessons, backref=backref('selfParticipant', lazy='dynamic'))
	dependents = relationship('Participant', backref=backref('guardian'))

	# organization = relationship('Organization', uselist=False, backref='admin')
	# roles = relationship('Role', secondary='user_roles', backref=backref('users', lazy='dynamic'))
	# active = Column('is_active', Boolean(), nullable=False, server_default='0')
	# organizer = relationship('Lesson', backref='contactEmail', lazy='dynamic')

	def set_password(self, pw):
		pwHash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
		self.password = pwHash.decode('utf8')

	def check_password(self, pw):
		if self.password is not None:
			expected_hash = self.password.encode('utf8')
			return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
		return False

	def __repr__(self):
		return f"User('{self.fName}', '{self.username}', '{self.email}')"


class Participant(Base):
	__tablename__ = 'participant'
	id = Column(Integer, primary_key=True)
	fName = Column(String(50), nullable=False)
	lName = Column(String(50), nullable=False)
	contactNum = Column(String(12))
	contactEmail = Column(String(50), nullable=False)
	user = Column(Integer, ForeignKey('user.id'))
	lessons = relationship('Lesson', secondary=depLessons, backref=backref('participants', lazy='dynamic'))


	def __repr__(self):
		return f"Dependent('{self.fName}', '{self.contactNum}', '{self.contactEmail}')"


class Organization(Base):
	__tablename__ = 'organization'
	id = Column(Integer, primary_key=True)
	manager = Column(String(50), nullable=False)
	managerEmail = Column(String(250), nullable=False)
	name = Column(String(50), nullable=False)
	address = Column(String(50), nullable=False)
	town = Column(String(30), nullable=False)
	state = Column(String(50), nullable=False)
	lessons = relationship('Lesson', backref='organization', lazy=True)


class Lesson(Base):
	__tablename__ = 'lesson'
	id = Column(Integer, primary_key=True)
	name = Column(String(100), nullable=False)
	startDate = Column(Date, nullable=False)
	endDate = Column(Date, nullable=False)
	startTime = Column(Time, nullable=False)
	endTime = Column(Time, nullable=False)
	contactEmail = Column(String(250), nullable=False)
	level = Column(Integer)
	location = Column(String(50), nullable=False)
	organizationId = Column(Integer(), ForeignKey('organization.id'), nullable=False)
	instructor = Column(String(50), nullable=False)
	desc = Column(String(200))
	cap = Column(Integer, nullable=False)
	day = Column(String, nullable=False)

	def __repr__(self):
		return f"Lesson('{self.startDate}', '{self.endDate}', '{self.level}', '{self.location}')"
