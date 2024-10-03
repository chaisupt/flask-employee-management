def init_status():
    # Delayed import to avoid circular import issues
    from app.models import Status, db

    deleted_status = Status.query.get(1)
    if not deleted_status:
        # Create the 'Deleted' status if it doesn't exist
        deleted_status = Status(id=1, status_name="Deleted")
        db.session.add(deleted_status)
        db.session.commit()
    elif deleted_status.status_name != "Deleted":
        # If the status with id=1 exists but isn't named 'Deleted', update it
        deleted_status.status_name = "Deleted"
        db.session.commit()

