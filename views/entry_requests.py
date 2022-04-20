import sqlite3
import json
from models import Entry
from models import Mood

def get_all_entries():
    """_summary_

    Returns:
        _type_: _description_
    """
    # Q: can you show me how to properly fill out a docstring?
    # I've been just adding blank ones in like the one above
    # to get rid of the missing docstring errors
    # A:
# Q: does this line say "using sqlite3, connect to "./kennel.sqlite3" and use it as the database?
    # A:

    # Q: what does "as conn" mean?
    # A:
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        # Q: can you give me the general purpose of the above two lines?
        # feels like we use db_cursor a lot and I have no idea what it does
        # A:

        #this is the sql query for what specific info I need when get_all_animals() runs
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id,
            m.label
        FROM Entry e
        JOIN Mood m
            ON m.id = e.mood_id
        """)

        # Initialize an empty list to hold all animal representations
        entries = []

        # Convert rows of data into a Python list
        #Q: which rows of data is this converting?
        # A:
        dataset = db_cursor.fetchall()
        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id,
            t.name tag_label              
        FROM EntryTag et
        JOIN Tag t
            ON et.tag_id = t.id
        """)

        entry_tags = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

# Q:i know this is creating an instance of
# animal for the current row, but I am fairly unsure what that means.
# does it mean that for row one on the animal table, make a row(actually a column) called id,
# then make one called name, so on and so on?
# Q: I know its getting the data from the sql
# query for each of these, but I'm unsure what row['name'] is linked to, or 'status'
# is it connnected to the a.name and a.status in the sql query?
# A:
            mood = Mood(row['mood_id'], row['label'])
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'],
                            row['mood_id'])


            entry.mood = mood.__dict__

            tags = []
            for et_row in entry_tags:
                if et_row["entry_id"] == row["id"]:
                    tags.append(et_row["tag_id"])

            entry.tags = tags

# does this line add the location/customer
# dictionary that was joined in the sql query to the current animal instance?

            # animal.location = location.__dict__

            # animal.customer = customer.__dict__
    # Q: does this line add the newly created animal dictionary with the location
    # and customer dictionaries on it, to the list "animals" that we created above?
    # A:
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    # Q: I have no idea what the hell this line does
    # A:
    return json.dumps(entries)

def get_single_entry(id):
    """_summary_

    Args:
        id (_type_): _description_

    Returns:
        _type_: _description_
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM entry e
        WHERE e.id = ?
        """, ( id, ))
        # Q: what is happening with the "( id, )" part of the code block above?
        # A:

        # Load the single result into memory
        data = db_cursor.fetchone()
        # location = Location(data['location_id'], data['location_name'], data['location_address'])

        # customer = Customer(data['customer_id'], data['customer_name'], data['customer_address'])

        # Create an animal instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'],
                            data['date'], data['mood_id'])



        return json.dumps(entry.__dict__)

def delete_entry(id):
    """_summary_

    Args:
        id (_type_): _description_
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entry
        WHERE id = ?
        """, (id, ))

def get_entries_by_search(text):
    """_summary_

    Args:
        text (_type_): _description_

    Returns:
        _type_: _description_
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            e.id,
            e.concept,
            e.entry,
            e.date,
            e.mood_id
        FROM Entry e
        WHERE e.entry LIKE ?
        """, ( f"%{text}%", ))

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entry(row['id'], row['concept'], row['entry'], row['mood_id'],
                            row['date'])

            entries.append(entry.__dict__)

    return json.dumps(entries)

def create_journal_entry(new_entry):
    """_summary_

    Args:
        new_animal (_type_): _description_

    Returns:
        _type_: _description_
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, entry, date, mood_id )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
            new_entry['date'], new_entry['moodId'], ))
# Q: do the question marks mean that whatever the client sends as those values is what will be used?
# A:

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid


        for i, entry_tag in enumerate(new_entry["tags"]):
            db_cursor.execute("""
                INSERT INTO EntryTag
                    ( entry_id, tag_id )
                VALUES
                    ( ?, ? );
                """, (id, entry_tag ))

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id


    return json.dumps(new_entry)

def update_entry(id, new_entry):
    """_summary_

    Args:
        id (_type_): _description_
        new_animal (_type_): _description_

    Returns:
        _type_: _description_
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                date = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
        new_entry['date'], new_entry['mood_id'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True