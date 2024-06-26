from typing import List

def paginate_items(data: List, page: int, limit: int,):
    start = (page - 1) * limit
    end = start + limit
    return data[start:end]