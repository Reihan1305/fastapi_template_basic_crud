from typing import List, Optional

from fastapi import APIRouter, Depends

from basic_template.db.dao.dummy_dao import DummyDAO
from basic_template.db.models.dummy_model import DummyModel
from basic_template.web.api.dummy.schema import DummyModelDTO, DummyModelInputDTO

router = APIRouter()


@router.get("/", response_model=List[DummyModelDTO])
async def get_dummy_models(
    limit: int = 10,
    offset: int = 0,
    dummy_dao: DummyDAO = Depends(),
) -> List[DummyModel]:
    """
    Retrieve all dummy objects from the database.

    :param limit: Limit of dummy objects, defaults to 10.
    :param offset: Offset of dummy objects, defaults to 0.
    :param dummy_dao: DAO for dummy models.
    :return: List of dummy objects from the database.
    """
    return await dummy_dao.get_all_dummies(limit=limit, offset=offset)


@router.get("/byname/{name}", response_model=List[DummyModel])
async def filter_name(
    name: str,
    dummy_dao: DummyDAO = Depends(),
) -> List[DummyModel]:
    """
    Filter dummy models by name.

    :param name: Name of the dummy model to filter.
    :param dummy_dao: DAO for dummy models.
    :return: List of filtered dummy models.
    """
    return await dummy_dao.filter(name=name)


@router.get("/byid/{id}", response_model=List[DummyModelDTO])
async def get_by_id(id: int, dummy_dao: DummyDAO = Depends()) -> Optional[DummyModel]:
    """
    Retrieve a dummy model by its ID.

    :param id: ID of the dummy model.
    :param dummy_dao: DAO for dummy models.
    :return: List of dummy models matching the ID.
    """
    return await dummy_dao.get_by_id(id=id)


@router.post("/", response_model=DummyModelInputDTO, status_code=201)
async def create_dummy_model(
    new_dummy_object: DummyModelInputDTO,
    dummy_dao: DummyDAO = Depends(),
) -> DummyModelInputDTO:
    """
    Create a dummy model in the database.

    :param new_dummy_object: New dummy model item.
    :param dummy_dao: DAO for dummy models.
    :return: The created dummy model.
    """
    await dummy_dao.create_dummy_model(name=new_dummy_object.name)
    return new_dummy_object


@router.delete("/{id}", status_code=200)
async def delete_dummy(id: int, dummy_dao: DummyDAO = Depends()) -> str:
    """
    Delete a dummy model by its ID.

    :param id: ID of the dummy model to delete.
    :param dummy_dao: DAO for dummy models.
    :return: Success message.
    """
    await dummy_dao.delete_dummies(id=id)
    return "Delete dummy success."


@router.put("/{id}", response_model=DummyModelDTO)
async def update_dummy(
    id: int,
    update_dummy_model: DummyModelInputDTO,
    dummy_dao: DummyDAO = Depends(),
) -> DummyModel:
    """
    Update a dummy model.

    :param id: ID of the dummy model to update.
    :param update_dummy_model: Updated dummy model item.
    :param dummy_dao: DAO for dummy models.
    :return: The updated dummy model.
    """
    return await dummy_dao.update_dummies(id, name=update_dummy_model.name)
