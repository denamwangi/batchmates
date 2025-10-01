from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
import json 
import os
from backend.models.orm import Base, Person, Interest, NormalizedInterest, InterestType, PersonInterest

engine = create_engine(
    os.getenv('MCP_URL')
)
inspector = inspect(engine)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def create_tables():
    if "interests" not in inspector.get_table_names():
        Base.metadata.create_all(engine)
    else:
        print('Tables exist!')

interest_types = [ 'technical_skills_and_interests', 'non_technical_hobbies_and_interest']
def add_interest_types():
    interest_types_to_db = []
    with SessionLocal() as session:
        for interest_type in interest_types:
            if session.query(InterestType).filter_by(name=interest_type).first():
                print(f"InterestType already in db: {interest_type}")
            else:
                interest_types_to_db.append(InterestType(name=interest_type))
        if interest_types_to_db:
            session.add_all(interest_types_to_db)
            session.commit()

def add_normalized_interests(normalized_interests):
    normalized_interests_to_db = []
    with SessionLocal() as session:
        for normalized_interest in normalized_interests:
            if session.query(NormalizedInterest).filter_by(name=normalized_interest).first():
                print(f"Already has normalized interest: {normalized_interest}")
            else:
                normalized_interests_to_db.append(NormalizedInterest(
                    name=normalized_interest
                ))
        if normalized_interests_to_db:
            session.add_all(normalized_interests_to_db)
            session.commit()

def get_normalized_interest(interest, normalized_interests_mappings, session):
    print('finding normalized interest for ', interest)
    normalized_interest = normalized_interests_mappings.get(interest, 'misc')
    print('normalized interest is: ', normalized_interest)
    normalized_interest_in_db = session.query(NormalizedInterest).filter_by(name=normalized_interest).first()
    if not normalized_interest_in_db:
        normalized_interest_in_db = NormalizedInterest(
            name=normalized_interest
        )
        session.add(normalized_interest_in_db)
        session.flush()
    return normalized_interest_in_db

def add_interests(intros, normalized_interests_mappings):
    all_tech_interests = set()
    for name, intro in intros.items():
        technical_skills_and_interests = intro['technical_skills_and_interests']
        for tech_interest in technical_skills_and_interests:
            all_tech_interests.add(tech_interest)

    interests_to_db = []
    with SessionLocal() as session:
        for tech_interest in all_tech_interests:
            normalized_interest_in_db = get_normalized_interest(tech_interest, normalized_interests_mappings, session)

            if session.query(Interest).filter_by(description=tech_interest).first():
                print(f" Interest already exists: {tech_interest}")
            else:
                interests_to_db.append(Interest(
                    description=tech_interest,
                    normalized_interest_id=normalized_interest_in_db.id,
                ))
        if interests_to_db:
            session.add_all(interests_to_db)
            session.commit()
        for tech_interest in session.query(Interest):
            print(f" {tech_interest.description}")

def add_people(intros):
    people_to_db = []
    with SessionLocal() as session:
        for name, intro in intros.items():
            if session.query(Person).filter_by(name=name).first():
                print(f"Person is already in db: {name}")
            else:
                people_to_db.append(Person(
                    name=intro.get('name', name),
                    location=intro.get('location', 'n/a'),
                    role_and_institution=intro.get('role_and_institution', 'n/a')
                ))
        if people_to_db:
            session.add_all(people_to_db)
            session.commit()

        for person in session.query(Person):
            print(f" {person.name}")


def add_person_interests(intros, normalized_interests_mappings):
    with SessionLocal() as session:
        for name, intro in intros.items():
            person_name = intro.get('name', name)
            print(f"\n Adding interests for: {person_name}")

            person_in_db = session.query(Person).filter_by(name=person_name).first()
            for interest_type in interest_types:
                interests = intro[interest_type]
                interest_type_in_db = session.query(InterestType).filter_by(name=interest_type).first()

                if not interest_type_in_db:
                    interest_type_in_db = InterestType(
                        name=interest_type,
                    )
                    session.add(interest_type_in_db)
                    session.flush()

                person_interests_to_add_to_db = []
                for interest in interests:
                    interest_in_db = session.query(Interest).filter_by(description=interest).first()
                    normalized_interest_in_db = get_normalized_interest(interest, normalized_interests_mappings, session)
                    if not interest_in_db:
                        interest_in_db = Interest(
                            description=interest,
                            normalized_interest_id=normalized_interest_in_db.id,
                        )
                        session.add(interest_in_db)
                        session.flush()
                    # check if in db already
                    if session.query(PersonInterest).filter_by(
                        person_id=person_in_db.id,
                        interest_id=interest_in_db.id,
                        interesttype_id=interest_type_in_db.id,
                    ).first():
                        print(f"{person_in_db.name} already has {interest_in_db.description} in the DB")
                    else:
                        person_interests_to_add_to_db.append(PersonInterest(
                            person_id=person_in_db.id,
                            interest_id=interest_in_db.id,
                            interesttype_id=interest_type_in_db.id,
                        ))
                print(f"    person_interests_to_add_to_db: {person_interests_to_add_to_db}")
                if person_interests_to_add_to_db:
                    session.add_all(person_interests_to_add_to_db)
                    session.flush()
        session.commit()
                    




def initialize_db():
    create_tables()

    with open('zulip_intros_json.json', 'r') as f:
        intros = json.load(f)
    with open('interest_mappings.json', 'r') as f:
        data = json.load(f)
        normalized_interests = data['standardized_tags']
        normalized_interests_mappings = data['mappings']

    
    # Example normalization call removed; normalization happens during add_* flows.

#

    add_interest_types()
    add_people(intros)
    add_normalized_interests(normalized_interests)
    add_interests(intros, normalized_interests_mappings)
    add_person_interests(intros, normalized_interests_mappings)

    # person = Person(
    #         id="dena", 
    #         name="Dena Metili Mwangi", 
    #         location="Brooklyn", 
    #         role_and_institution='Previous EM'
    #     )
    # tech_interest = InterestType(name='technical_skills_and_interests')
    # goal = InterestType(name='goal')
    # llm = Interest(description="LLM")
    # openxr = Interest(description="OpenXR")

    # session.add_all([person, tech_interest, goal, llm, openxr])
    # session.flush()

    # pi_1 = PersonInterest(
    #     person_id=person.id,
    #     interest_id=llm.id,
    #     interesttype_id=tech_interest.id
    # )
    # pi_2 = PersonInterest(
    #     person_id=person.id,
    #     interest_id=openxr.id,
    #     interesttype_id=tech_interest.id
    # )
    # session.add(pi_1, pi_2)

    # session.commit()
    # for person in session.query(Person):
    #     print(f" { person.id} and {person.name} and {person.interests}")

if __name__ == "__main__":
    initialize_db()
    # for person in session.query(Person).limit(5):
    #     print(f" {person.name} has these interests: ")
    #     for pi in person.interests: print(f"....   {pi.interest.description}")
        
        

