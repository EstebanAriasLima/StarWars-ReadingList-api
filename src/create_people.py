
@app.cli.command("create-people")
def create_people():
    person = Person.create(
            name="jose",
        eye_color="blue"
    )

print(person.serialize())