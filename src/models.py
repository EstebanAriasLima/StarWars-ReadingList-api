from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    edited = db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())
class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False, default=True)
    description = db.Column(db.String(500))

class Item(Base):
    __abstract__ = True
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}: {self.name}"

class Person(Item):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.String(120), unique=False, nullable=True)
    mass = db.Column(db.String(120), unique=False, nullable=True)
    hair_color = db.Column(db.String(120), unique=False, nullable=True)
    skin_color = db.Column(db.String(120), unique=False, nullable=True)
    eye_color = db.Column(db.String(120), unique=False, nullable=True)
    birth_year = db.Column(db.String(120), unique=False, nullable=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    homeworld = db.Column(db.String(120), unique=False, nullable=True)
    url = db.Column(db.String(120), unique=False, nullable=True)
    description = db.Column(db.String(120), unique=False, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'person',
    }

    @property
    def uid(self):
        return self.url.split("/")[-1]

    @classmethod
    def create(cls, data):
        instance = cls(**data)
        if (not isinstance(instance, cls)):
            return None
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)


    def __repr__(self) -> str:
        return f"{self.id}: {self.name}, {self.eye_color}"

    def __init_(self, **kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def serialize(self, long=False):
        response= {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
        }
        if long:
            return {**{
                'height': self.height,
                'mass': self.mass,
                'hair_color':self.hair_color,
                'skin_color':self.skin_color,
                'birth_year':self.birth_year,
                'gender':self.gender,
                'homeworld':self.homeworld,
                'url':self.url,
                'description':self.description,
                'uid':self.uid
            },**response} 
        else:
            return response

class Planet(Item):
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.String(120), unique=False, nullable=True)
    rotation_period = db.Column(db.String(120), unique=False, nullable=True)
    orbital_period = db.Column(db.String(120), unique=False, nullable=True)
    gravity = db.Column(db.String(120), unique=False, nullable=True)
    population = db.Column(db.String(120), unique=False, nullable=True)
    climate = db.Column(db.String(120), unique=False, nullable=True)
    terrain = db.Column(db.String(120), unique=False, nullable=True)
    surface_water = db.Column(db.String(120), unique=False, nullable=True)
    url = db.Column(db.String(120), unique=False, nullable=True)
    description = db.Column(db.String(120), unique=False, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'planet',
    }

    @classmethod
    def create(cls, data):
        instance = cls(**data)
        if (not isinstance(instance, cls)):
            return None
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

    def __repr__(self) -> str:
        return f"{self.id}: {self.name},  {self.climate}"

    def __init_(self, **kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
        }

class Vehicle(Item):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(120), unique=False, nullable=True)
    vehicle_class = db.Column(db.String(120), unique=False, nullable=True)
    manufacturer = db.Column(db.String(120), unique=False, nullable=True)
    cost_in_credits = db.Column(db.String(120), unique=False, nullable=True)
    length = db.Column(db.String(120), unique=False, nullable=True)
    crew = db.Column(db.String(120), unique=False, nullable=True)
    passengers = db.Column(db.String(120), unique=False, nullable=True)
    max_atmosphering_speed = db.Column(db.String(120), unique=False, nullable=True)
    cargo_capacity = db.Column(db.String(120), unique=False, nullable=True)
    consumables = db.Column(db.String(120), unique=False, nullable=True)
    films = db.Column(db.String(120), unique=False, nullable=True)
    pilots = db.Column(db.String(120), unique=False, nullable=True)
    url = db.Column(db.String(120), unique=False, nullable=True)
    description = db.Column(db.String(120), unique=False, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'vehicle',
    }

    @classmethod
    def create(cls, data):
        instance = cls(**data)
        if (not isinstance(instance, cls)):
            return None
        db.session.add(instance)
        try:
            db.session.commit()
            return instance
        except Exception as error:
            db.session.rollback()
            raise Exception(error.args)

    def __repr__(self) -> str:
        return f"{self.id}: {self.name}, {self.max_atmosphering_speed}"

    def __init_(self, **kwargs):
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "max_atmosphering_speed": self.max_atmosphering_speed,
        }




    def __repr__(self):
        return '<User %r>' % self.username
    

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }