from sqlalchemy.orm import Session

# Function to perform a database transaction
def perform_transaction(db: Session, func):
    try:
        result = func(db)
        db.commit()  # Commit the transaction
        return result
    except Exception as e:
        db.rollback()  # Rollback the transaction in case of an error
        raise e
