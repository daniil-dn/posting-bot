from typing import List


class Repo:
    """Db abstraction layer"""

    def __init__(self, conn):
        self.conn = conn

    async def get_username_from_id(self, user_id) -> str:
        req = f'select username from tg_users where user_id = {user_id}'
        res = await self.conn.fetch(req)
        username = res[0]['username']
        return username

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
            row
            for row in await self.conn.fetch(
                "select userid, username from tg_users;",
            )
        ]

    async def ban_user(self, user_id):
        request = f"INSERT INTO ban_list (user_id) VALUES ({user_id}) ON CONFLICT DO NOTHING;"
        await self.conn.execute(
            request
        )
        return "user is banned"

    async def unban_user(self, user_id):
        request = f"delete from ban_list where user_id = {user_id};"
        await self.conn.execute(
            request
        )
        return "user is unbanned"

    async def banlist_str(self):
        request = f"select * from ban_list;"
        return str([row[0] for row in await self.conn.fetch(request)])

    async def check_ban(self, user_id) -> bool:
        return bool([
            row[0]
            for row in await self.conn.fetch(
                f"select user_id from ban_list where user_id = {user_id}",
            )
        ])

# SELECT pg_xact_commit_timestamp(xmin) as time, * FROM tg_users order by time limit 1; #Check for update
