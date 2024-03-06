import aiohttp
from datetime import datetime, timedelta
import json
import os
from base.base_class import BaseClass


class GithubClient(BaseClass):

    def __init__(self):
        super().__init__()
        self.username = os.getenv("GIT_USER")
        self.repo = os.getenv("GIT_REPO")
        self.session = None

    async def start_session(self) -> None:
        self.session = aiohttp.ClientSession()

    async def close_session(self) -> None:
        if self.session:
            await self.session.close()

    async def get_latest_commits(self, from_date: dict) -> list[str]:
        """
        :param from_date: dict with timestamp in ISO 8601 form. Example:
        {'since':'2023-11-23T18:50:13Z'}
        :return: list of commits
        """
        url = f'https://api.github.com/repos/{self.username}/{self.repo}/commits'
        params = from_date
        sha_list = []
        async with self.session.get(url, params=params) as query:
            if query.status == 200:
                response = await query.text()
                commits = json.loads(response)
                for commit in commits:
                    sha_list.append(commit['sha'])
                print(f'Found {len(sha_list)} commits')
            else:
                print(f"Failed to retrieve commits: Status code: {query.status}")
        return sha_list

    async def get_commit_info(self, commit_sha: str) -> str:
        """
        From a commit identifier, get all associated files and their changes.
        :param commit_sha: commit identifier
        :return: Content as a string instead of writing to a file
        """
        url = f'https://api.github.com/repos/{self.username}/{self.repo}/commits/{commit_sha}'
        content = ""
        async with self.session.get(url) as query:
            if query.status == 200:
                text = await query.text()
                commit_data = json.loads(text)
                content += f"Commit id:{commit_sha}\n"
                content += f"Commit message: {commit_data['commit']['message']}\n"
                for file in commit_data['files']:
                    content += f"File: {file['filename']}\n"
                    content += f"Additions: {file['additions']}\n"
                    content += f"Deletions: {file['deletions']}\n"
                    content += f"Changes: {file['changes']}\n"
                    if 'patch' in file:
                        content += f"Patch: {file['patch']}\n"
                    else:
                        content += "Patch: Not available\n"
            else:
                print(f"Failed to retrieve commit data. Status code: {query.status}")
                return ""
        return content

    @staticmethod
    def get_timestamp(days: int = 1) -> dict:
        """
        Gets timestamp from n number of days in the past, returned in ISO8601 format
        Example: days=1 will return the timestamp from 24 hours ago
        :return: dict {'since':timestamp}
        """
        current_time = datetime.now()
        # get time delta
        timestamp = current_time - timedelta(days=days)
        # Change to ISO 8601 format
        iso_8601_format = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
        result = {'since': iso_8601_format}
        return result
