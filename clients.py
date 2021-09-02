import asyncio
from typing import Any

import ujson
from httpx import AsyncClient

from core.settings import settings
from project.schemas.project import Project, ProjectDetail


class MiemAPIClient(AsyncClient):
    async def get_projects(self) -> list[Project]:
        return [Project(**data) for data in self._get_many('/projects')]

    async def get_project(self, project_id: int) -> ProjectDetail:
        project_data, vacancies_data = await asyncio.gather(
            self._get_one(f'/project/body/{project_id}'),
            self._get_many(f'/project/vacancies/{project_id}'),
        )
        return ProjectDetail(**project_data, vacancies=list(vacancies_data))

    async def _get_one(
        self, path: str, params: dict = None, headers: dict = None, **kwargs: Any
    ) -> dict:
        response = await self.get(path, params=params, headers=headers, **kwargs)
        body = ujson.loads(response.text['data'])
        if not isinstance(body, dict):
            raise ValueError(f'API Response for {path} is not json deserializable')
        return body

    async def _get_many(
        self, path: str, params: dict = None, headers: dict = None, **kwargs: Any
    ) -> list[dict]:
        response = await self.get(path, params=params, headers=headers, **kwargs)
        body = ujson.loads(response.text['data'])
        if not isinstance(body, list):
            raise ValueError(f'API Response for {path} is not iterable')
        return body


miem_client = MiemAPIClient(
    base_url=f'{settings.miem_api_url}/public-api',
    timeout=settings.miem_api_timeout,
)
