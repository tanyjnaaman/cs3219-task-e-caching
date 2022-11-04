from typing import List, Optional, Union
from fastapi import APIRouter, Body, Cookie
from src.workflow_manager import WorkflowManager

router = APIRouter()


@router.post("/create")
def create_link(
    url: str = Body(...),
    description: str = Body(...),
    jwt_token: Optional[str] = Cookie(None),
):
    """
    Create a new link.
    """
    # create link manager
    manager = WorkflowManager()

    # auth
    user = manager.auth(jwt_token)

    # create
    link = manager.create_link(url, description, user.user_id)

    return link


@router.get("/get_all_user")
def get_all_user_links(jwt_token: Optional[str] = Cookie(None)):
    """
    Get all links for a user.
    """
    # create link manager
    manager = WorkflowManager()

    # auth
    user = manager.auth(jwt_token)

    # get links
    links = manager.get_links(user.user_id)

    return links


@router.put("/update")
def update_link(
    link_id: str = Body(...),
    url: Union[str, None] = Body(...),
    description: Union[str, None] = Body(...),
    jwt_token: Optional[str] = Cookie(None),
):
    """
    Update a link.
    """
    # create link manager
    manager = WorkflowManager()

    # auth
    user = manager.auth(jwt_token)

    # update link
    link = manager.update_link(link_id, url, description)

    return link


@router.delete("/delete/{link_id}")
def delete_link(link_id: str, jwt_token: Optional[str] = Cookie(None)):
    """
    Delete a link.
    """
    # create link manager
    manager = WorkflowManager()

    # auth
    user = manager.auth(jwt_token)

    # delete link
    manager.delete_link(link_id)

    return {"message": "Link deleted."}
