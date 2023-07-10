import psycopg2

# Database connection parameters
db_host = 'localhost'
db_port = '5433'
db_name = 'snmptrapreceiver'
db_user = 'postgres'
db_password = 'postgres123'

def store_trap_messages(messages):
    # Establish a database connection
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
    cursor = conn.cursor()

    # Store the trap messages in the database
    insert_query = "INSERT INTO trap_table (id, trap_message) VALUES (NEXTVAL('id_seq'), %s)"
    cursor.execute(insert_query, (messages,))

    # Commit the database transaction
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()
