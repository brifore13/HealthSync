import pytest
from sqlalchemy import text
from app.core.database import engine, SessionLocal, Base, get_db

def test_database_connection():
    """Test database connection works"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1

def test_session_creation():
    """Test database session creation"""
    db = SessionLocal()
    
    assert db is not None
    assert hasattr(db, 'query')
    assert hasattr(db, 'add')
    assert hasattr(db, 'commit')
    
    db.close()

def test_get_db_dependency():
    """Test get_db dependency function"""
    db_generator = get_db()
    db = next(db_generator)
    
    assert db is not None
    assert hasattr(db, 'query')
    
    # Clean up
    try:
        next(db_generator)
    except StopIteration:
        pass  # Expected

def test_database_tables_creation():
    """Test that database tables can be created"""
    # This should not raise an exception
    Base.metadata.create_all(bind=engine)
    
    # Check that tables exist
    with engine.connect() as connection:
        # Check users table
        result = connection.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        ))
        assert result.fetchone() is not None
        
        # Check health_records table
        result = connection.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='health_records'"
        ))
        assert result.fetchone() is not None

def test_database_tables_cleanup():
    """Test that database tables can be dropped"""
    # Create tables first
    Base.metadata.create_all(bind=engine)
    
    # Drop tables
    Base.metadata.drop_all(bind=engine)
    
    # Check that tables are gone
    with engine.connect() as connection:
        result = connection.execute(text(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        ))
        assert result.fetchone() is None