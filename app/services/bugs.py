from app.core.utils import read_json, write_json
from app.services.errors import BugNotFoundError
from app.schemas.bugs import Bug

class BugService:
    def filter_by_params(self, params: str, bugs: list[dict]) -> list[dict]:
        return [bug for bug in bugs if bug[params] == params]

    async def get_bug_by_id(self, bug_id: str, bugs: list[dict]) -> dict:
        for bug in bugs:
            if bug['id'] == bug_id:
                return bug 

    async def get_bugs(
            self,
            status: str | None = None,
            severity: str | None = None,
            assignee: str | None = None
    ) -> list[dict]:
        bugs = await read_json('bugs.json')
        if status is not None:
            bugs = self.filter_by_params(status, bugs)
        if severity is not None:
            bugs = self.filter_by_params(severity, bugs)
        if assignee is not None:
            bugs = self.filter_by_params(assignee, bugs)

        if not bugs:
            raise BugNotFoundError('Bug not found')

        return bugs

    async def get_reported_bugs(self, reporter: str) -> list[dict]:
        bugs = await read_json('bugs.json')

        user_bugs = [bug for bug in bugs if bug['reporter'] == reporter]

        if not user_bugs:
            raise BugNotFoundError('Bug not found')
        return user_bugs

    async def get_assigned_bugs(self, assignee: str) -> list[dict]:
        bugs = await read_json('bugs.json')

        user_bugs = [bug for bug in bugs if bug['assignee'] == assignee]

        if not user_bugs:
            raise BugNotFoundError('Bug not found')
        return user_bugs

    async def get_bug(self, title: str) -> dict:
        bugs = await read_json('bugs.json')

        for bug in bugs:
            title = title.lower().strip()
            if title == bug['title'].lower().strip():
                return bug
        raise BugNotFoundError('Bug not found')

    async def report_bug(self, bug: dict, reporter: str) -> dict:
        user_bug = bug.copy()
        bugs = await read_json('bugs.json')

        bug_model = Bug(
            id=str(len(bugs) + 1),
            **bug
        )

        user_bug = bug_model.model_dump()
        user_bug['reporter'] = reporter
        bugs.append(user_bug)

        await write_json('bugs.json', bugs)

        return user_bug

    async def update_bug(self, bug_id: str, bug_update: dict) -> dict:
        bugs = await read_json('bugs.json')
        bug = await self.get_bug_by_id(bug_id, bugs)

        if not bug:
            raise BugNotFoundError('Bug not found')

        for key, update in bug_update.items():
            for k, _ in bug.items():
                if key == k:
                    bug[k] = update
                    continue
        await write_json('bugs.json', bugs)

        return bug

    async def delete_bug(self, bug_id: str):
        bugs = await read_json('bugs.json')
        bug = await self.get_bug_by_id(bug_id, bugs)

        if not bug:
            raise BugNotFoundError('Bug not found')

        bugs.remove(bug)

        await write_json('bugs.json', bugs)

bug_service = BugService()
