from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Person(Base):
    __tablename__ = "people"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    location = Column(String)
    role_and_institution = Column(String)

    interests = relationship("PersonInterest", back_populates="person")


class Interest(Base):
    __tablename__ = "interests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, unique=True, nullable=False)
    normalized_interest_id = Column(Integer, ForeignKey("normalized_interests.id"))

    normalized_interest = relationship("NormalizedInterest", back_populates="interests")
    people = relationship("PersonInterest", back_populates="interest")


class NormalizedInterest(Base):
    __tablename__ = "normalized_interests"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    interests = relationship('Interest', back_populates="normalized_interest")


# goals, technical_skills_and_interests, non_technical_hobbies_and_interest
class InterestType(Base):
    __tablename__ = "interest_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    person_interests = relationship("PersonInterest", back_populates="interest_type")


class PersonInterest(Base):
    __tablename__ = "person_interests"
    person_id = Column(Integer, ForeignKey("people.id"), primary_key=True)
    interest_id = Column(Integer, ForeignKey("interests.id"), primary_key=True)
    interesttype_id = Column(Integer, ForeignKey("interest_types.id"), primary_key=True)

    person = relationship('Person', back_populates='interests')
    interest = relationship('Interest', back_populates='people')
    interest_type = relationship('InterestType', back_populates='person_interests')


