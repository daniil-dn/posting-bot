from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn


    # users
    async def add_user(self, user_id, username) -> None:
        """Store user in DB, ignore duplicates"""
        request = f"INSERT INTO tg_users(user_id, username) VALUES ({user_id}, '{username}') ON CONFLICT DO NOTHING;"
        await self.conn.execute(
            request
        )
        return

    async def list_users(self) -> List[int]:
        """List all bot users"""
        # return await self.conn.fetch(
        #     f"select userid from tg_users;"
        # )
        return [
            row[0]
            for row in await self.conn.fetch(
                "select userid, username from tg_users;",
            )
        ]

# SELECT pg_xact_commit_timestamp(xmin) as time, * FROM tg_users order by time limit 1; #Check for update