from pydantic import BaseModel, Field

class PaginationMetadata(BaseModel):
    items_per_page: int
    total_items: int
    current_page: int
    total_pages: int