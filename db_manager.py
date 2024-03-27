import sqlite3


def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("GoogleSheet.db")

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # SQL statement to create a table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS GoogleSheetProducts (
        id INTEGER PRIMARY KEY,
        haul_id INTEGER NOT NULL,
        sku TEXT NOT NULL,
        product_name TEXT NOT NULL,
        main_category TEXT NOT NULL,
        sub_category TEXT NOT NULL,
        packaging TEXT NOT NULL,
        condition TEXT NOT NULL,
        condition_notes TEXT,
        inserts TEXT NOT NULL,
        title_change TEXT,
        upc TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        in_google_drive BOOLEAN DEFAULT FALSE
        barcode_generated BOOLEAN DEFAULT FALSE
    );
    """

    # Execute the SQL statement to create the table
    cursor.execute(create_table_sql)

    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()

    print("Database and table created successfully.")


# Call the function to create the database and table
# create_database()


def get_data(haul_id=None):
    # Connect to the SQLite database
    conn = sqlite3.connect("Products.db")

    # Create a cursor object using the connection
    cursor = conn.cursor()
    if haul_id:
        # SQL statement to select data from the table for a specific haul_id
        select_sql = "SELECT * FROM Products WHERE haul_id = ?;"
        # Execute the SQL statement to select the data
        cursor.execute(select_sql, (haul_id,))
    else:
        select_sql = "SELECT * FROM Products;"

        # Execute the SQL statement to select the data
        cursor.execute(select_sql)

    # Fetch all the selected data
    data = cursor.fetchall()

    # Close the connection to the database
    conn.close()

    return data


def get_inserted_skus(haul_id):
    # Connect to the SQLite database
    conn = sqlite3.connect("Products.db")

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # SQL statement to select the inserted skus for a specific haul_id
    select_sql = "SELECT sku FROM Products WHERE haul_id = ?;"
    # Execute the SQL statement to select the inserted skus
    cursor.execute(select_sql, (haul_id,))

    # Fetch all the selected skus
    skus = cursor.fetchall()

    # Close the connection to the database
    conn.close()

    return [sku[0] for sku in skus]


def insert_data(data):
    # Connect to the SQLite database
    conn = sqlite3.connect("Products.db")

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # SQL statement to insert data into the table
    insert_sql = """
    INSERT INTO Products (
        haul_id,sku, product_name, main_category, sub_category, packaging, condition, condition_notes, inserts, upc, in_google_drive
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?,?);
    """

    # Execute the SQL statement to insert the data
    cursor.execute(
        insert_sql,
        (
            data["haul_id"],
            data["sku"],
            data["product_name"],
            data["main_category"],
            data["sub_category"],
            data["packaging"],
            data["condition"],
            data["condition_notes"],
            data["inserts"],
            data["upc"],
            True,  # Set in_google_drive to True
        ),
    )

    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()

    print("Data inserted successfully.")


def delete_data(haul_id):
    # Connect to the SQLite database
    conn = sqlite3.connect("Products.db")

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # SQL statement to delete data from the table for a specific haul_id
    delete_sql = "DELETE FROM Products WHERE haul_id = ?;"
    # Execute the SQL statement to delete the data
    cursor.execute(delete_sql, (haul_id,))

    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()

    print("Data deleted successfully.")


def bulk_delete_skus(skus):
    # Connect to the SQLite database
    conn = sqlite3.connect("Products.db")

    # Create a cursor object using the connection
    cursor = conn.cursor()

    # SQL statement to delete data from the table for a specific haul_id
    delete_sql = "DELETE FROM Products WHERE sku = ?;"
    # Execute the SQL statement to delete the data
    for sku in skus:
        cursor.execute(delete_sql, (sku,))

    # Commit the changes to the database
    conn.commit()

    # Close the connection to the database
    conn.close()

    print("Data deleted successfully.")


bulk_delete_skus(
    [
        "P003004",
        "P003005",
        "P003006",
        "P003007",
        "P003008",
        # "FB070027",
        # "FB070028",
        # "FB070029",
        # "FB070030",
        # "FB070031",
        # "FB070032",
        # "FB070033",
        # "FB070034",
        # "FB070035",
        # "FB070036",
        # "FB070037",
        # "FB070038",
        # "FB070039",
        # "FB070040",
        # "FB070041",
        # "FB070042",
        # "FB070043",
        # "FB070044",
        # "FB070045",
        # "FB070046",
        # "FB070047",
        # "FB070048",
        # "FB070049",
        # "FB070050",
        # "FB070051",
        # "FB070052",
        # "FB070053",
        # "FB070054",
        # "FB070055",
        # "FB070056",
        # "FB070057",
        # "FB070058",
        # "FB070059",
        # "FB070060",
        # "FB070061",
        # "FB070062",
        # "FB070063",
        # "FB070064",
        # "FB070065",
        # "FB070066",
        # "FB070067",
        # "FB070068",
    ]
)

# delete_data("WM002")
