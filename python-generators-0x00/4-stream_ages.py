import seed


def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data;")
    while True:
        age = cursor.fetchone()
        if not age:
            break
        yield age[0]
    cursor.close()
    connection.close()

def get_average_age():
    total = cnt = 0
    for age in stream_user_ages():
        total += age
        cnt += 1
    average = total/cnt
    print(f"Average age of users: {average}")