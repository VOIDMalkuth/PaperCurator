import os
import sqlite3

from loguru import logger

DB_PATH = os.environ.get("DB_PATH", "arxiv.db")


class ArxivDB:
    def __init__(self, db_path):
        """Initialize database connection and create tables if they don't exist"""
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self._create_tables()

    def _create_tables(self):
        """Create required tables if they don't exist"""
        # Create paper table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS paper (
                entry_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                link TEXT NOT NULL,
                submitted_date TEXT NOT NULL,
                abstract TEXT NOT NULL,
                relevance INTEGER DEFAULT -1,
                summary TEXT,
                feed_sent INTEGER DEFAULT 0
            )
        """)

        # Create arxiv_data_info table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS arxiv_data_info (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        # Initialize arxiv_data_info with default values if empty
        self.cursor.execute("SELECT COUNT(*) FROM arxiv_data_info")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.executemany(
                "INSERT INTO arxiv_data_info (key, value) VALUES (?, ?)",
                [("last_paper_id", None), ("last_published_time", None)],
            )

        self.conn.commit()

    def add_paper_if_not_exists(
        self,
        entry_id,
        title,
        link,
        submitted_date,
        abstract,
        relevance=-1,
        summary=None,
        feed_sent=0,
    ):
        """Add a new paper record"""
        # Check if an entry exists
        self.cursor.execute("SELECT 1 FROM paper WHERE entry_id = ?", (entry_id,))
        exists = self.cursor.fetchone() is not None
        if exists:
            return False

        logger.debug(f"Adding paper: {title}")
        try:
            self.cursor.execute(
                """
                INSERT INTO paper (entry_id, title, link, submitted_date, abstract, relevance, summary, feed_sent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    entry_id,
                    title,
                    link,
                    submitted_date,
                    abstract,
                    relevance,
                    summary,
                    feed_sent,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            logger.error(f"Failed to add paper: {title}")
            return False

    def get_papers_by_relevance(self, relevance):
        """Get papers filtered by relevance"""
        self.cursor.execute("SELECT * FROM paper WHERE relevance = ?", (relevance,))
        return self.cursor.fetchall()

    def get_one_paper_by_relevance(self, relevance):
        """Get papers filtered by relevance"""
        self.cursor.execute(
            "SELECT * FROM paper WHERE relevance = ? LIMIT 1", (relevance,)
        )
        return self.cursor.fetchone()

    def get_unpublished_papers(self):
        """Get papers filtered by relevance"""
        self.cursor.execute(
            "SELECT * FROM paper WHERE (relevance = 100 or relevance = 2) and feed_sent = 0"
        )
        return self.cursor.fetchall()

    def update_paper(self, entry_id, relevance=None, summary=None, feed_sent=None):
        """Update paper relevance and/or summary"""
        update_fields = []
        params = []

        if relevance is not None:
            update_fields.append("relevance = ?")
            params.append(relevance)

        if summary is not None:
            update_fields.append("summary = ?")
            params.append(summary)

        if feed_sent is not None:
            update_fields.append("feed_sent = ?")
            params.append(feed_sent)

        if not update_fields:
            return False

        params.append(entry_id)
        query = f"""
            UPDATE paper 
            SET {', '.join(update_fields)}
            WHERE entry_id = ?
        """

        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_data_info(self, key):
        """Get value from arxiv_data_info table"""
        self.cursor.execute("SELECT value FROM arxiv_data_info WHERE key = ?", (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_data_info(self, key, value):
        """Update value in arxiv_data_info table"""
        self.cursor.execute("SELECT 1 FROM arxiv_data_info WHERE key = ?", (key,))
        exists = self.cursor.fetchone() is not None
        if not exists:
            self.cursor.execute(
                "INSERT INTO arxiv_data_info (key, value) VALUES (?, ?)", (key, value)
            )
        else:
            self.cursor.execute(
                """
                UPDATE arxiv_data_info
                SET value = ?
                WHERE key = ?
            """,
                (value, key),
            )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def close(self):
        """Close database connection"""
        self.conn.close()

    def __del__(self):
        """Destructor to ensure database connection is closed"""
        try:
            self.conn.close()
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
