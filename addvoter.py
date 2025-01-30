# import psycopg2
# import random
# from datetime import datetime, timedelta

# # Database connection
# conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
# cur = conn.cursor()

# # Define candidates
# candidates = [
#     'ec72cd93-bc41-45cd-8977-9b2ae3d82ab3',
#     '0678b3a3-4713-45fb-8207-c499989a2280',
#     '46489a96-634f-4681-bc8f-54356c4d2259'
# ]

# # Insert 100 new votes
# for voter_id in range(10300, 11300):  # Adjust voter_id range as needed
#     candidate_id = random.choice(candidates)
#     voting_time = datetime.now() - timedelta(seconds=random.randint(0, 86400))  # Random time within the last day
#     vote = 1

#     try:
#         # Attempt to insert the record
#         cur.execute(
#             "INSERT INTO votes (voter_id, candidate_id, voting_time, vote) VALUES (%s, %s, %s, %s)",
#             (str(voter_id), candidate_id, voting_time, vote)
#         )
#     except psycopg2.errors.UniqueViolation as e:
#         print(f"Duplicate voter_id {voter_id}. Skipping...")
#         conn.rollback()  # Rollback the transaction on error
#     except Exception as e:
#         print(f"Error inserting voter {voter_id}: {e}")
#         conn.rollback()  # Rollback the transaction on any other error
#     else:
#         conn.commit()  # Commit if no error

# # Close the connection
# cur.close()
# conn.close()

# print("Inserted new votes successfully.")
import psycopg2
import random
from datetime import datetime, timedelta

# Database connection
conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
cur = conn.cursor()

# Define candidates
candidates = [
    'ec72cd93-bc41-45cd-8977-9b2ae3d82ab3',
    '0678b3a3-4713-45fb-8207-c499989a2280',
    '46489a96-634f-4681-bc8f-54356c4d2259'
]

# Insert new votes
start_voter_id = 12300  # Adjust starting voter ID
end_voter_id = 13300    # Adjust ending voter ID
for voter_id in range(start_voter_id, end_voter_id):
    candidate_id = random.choice(candidates)
    voting_time = datetime.now() - timedelta(seconds=random.randint(0, 86400))  # Random time within the last day
    vote = 1

    try:
        # Attempt to insert the record
        cur.execute(
            "INSERT INTO votes (voter_id, candidate_id, voting_time, vote) VALUES (%s, %s, %s, %s)",
            (str(voter_id), candidate_id, voting_time, vote)
        )
    except psycopg2.errors.UniqueViolation:
        print(f"Duplicate voter_id {voter_id}. Skipping...")
        conn.rollback()  # Rollback the transaction on error
    except Exception as e:
        print(f"Error inserting voter {voter_id}: {e}")
        conn.rollback()  # Rollback the transaction on any other error
    else:
        conn.commit()  # Commit if no error

# Close the connection
cur.close()
conn.close()

print("Inserted new votes successfully.")
