from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.utils import to_camel


class MiemModel(BaseModel):
    class Config:
        alias_generator = to_camel


class Project(MiemModel):
    id: int
    owner: bool
    status: str
    status_desc: str
    name_rus: str
    head: str
    direction_head: Optional[str]
    type: Optional[str]
    type_desc: Optional[str]
    type_id: Optional[int]
    status_id: Optional[int]
    date_created: Optional[datetime]
    vacancies: int
    team: list[str]
    vacancy_data: list[str]
    number: Optional[str]
    desc: Optional[str]
    hours_count: int
    faculty_id: Optional[int]
    thumbnail: Optional[str]

    class Config:
        title = 'Общая информация о проекте'


class Vacancy(MiemModel):
    vacancy_id: int
    role: str
    count: int
    applied: bool
    booked: bool
    approved: bool
    application_id: Optional[int]
    disciplines: list[str] = []
    additionally: list[str] = []

    class Config:
        title = 'Описание вакансии'


class ProjectDetail(MiemModel):
    id: int
    target: str
    annotation: str
    results: str
    vacancies: list[Vacancy] = []

    class Config:
        title = 'Подробная информация о проекте'
