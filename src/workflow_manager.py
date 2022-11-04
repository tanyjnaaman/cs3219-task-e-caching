from typing import List
from src.exceptions import UnauthorizedException
from src.link.services.link_services import LinkCrudService
from src.link.interfaces.link import Link


class WorkflowManager:
    def __init__(
        self,
        link_crud_service: LinkCrudService = LinkCrudService(),
    ):
        self.link_crud_service = link_crud_service

    def get_links(self) -> List[Link]:
        """
        Get all links.
        """
        # get links
        links = self.link_crud_service.get_links()

        return links

    def get_links_by_id(self, id: str) -> Link:
        """
        Get a specific link.
        """
        # get links
        links = self.link_crud_service.get_link_by_id(id)

        return links
