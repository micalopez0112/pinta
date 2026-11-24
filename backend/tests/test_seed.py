from sqlalchemy.engine import make_url

from app.seed import describe_database


def test_describe_database_shows_where_but_never_the_password():
    url = make_url("postgresql+psycopg://usuario:contraseña-secreta@ep-abc-123.us-east-1.aws.neon.tech/neondb")
    description = describe_database(url)
    assert description == "ep-abc-123.us-east-1.aws.neon.tech/neondb"
    assert "secreta" not in description
    assert "usuario" not in description


def test_describe_database_for_the_local_default():
    url = make_url("postgresql+psycopg://pinta:pinta@localhost:5434/pinta")
    assert describe_database(url) == "localhost:5434/pinta"
