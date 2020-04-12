import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.connection import create_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

conn = create_connection()
db_session = conn.cursor()

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init():
    try:
        # Try to create session to check if DB is awake
        db_session.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e

    try:
        with open("./app/constraints.sql", "r") as f:
            db_session.execute(f.read())
        conn.commit()
    except Exception as e:
        logger.warning(e)


def main():
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")
    conn.close()


if __name__ == "__main__":
    main()
