from collections import defaultdict
from typing import Any

from pandas import DataFrame
from peewee import JOIN
from surprise import Dataset, Reader

from clients import miem_client
from models.user import Like, User
from project.schemas.project import Project


async def get_predictor() -> Any:
    all_users: list[User] = list(
        await User.manager.get(User.select().join_from(User, Like, JOIN.LEFT_OUTER))
    )
    all_projects: list[Project] = await miem_client.get_projects()
    data = defaultdict(list)
    """
           project_id1 project_id2 project_id3 project_id4
    user1       1           0           0           1
    user2       0           0           1           0
    user3       0           1           0           1
    """
    for user in all_users:
        user_liked = {like.project_id for like in user.likes}
        for project in all_projects:
            data['userId'].append(user.id)
            data['projectId'].append(project.id)
            data['rating'].append(int(project.id in user_liked))
    df = DataFrame(data=data)
    reader = Reader(rating_scale=(0, 1))
    dataset = Dataset.load_from_df(df[['userID', 'projectId', 'rating']], reader)
    # TODO: Complete predictions


async def get_recommendations(current_user: User) -> list[Project]:
    predictor = await get_predictor()
    predictions: set[int] = set(predictor.predict(current_user.id))
    all_projects: list[Project] = await miem_client.get_projects()
    return [project for project in all_projects if project.id in predictions]
