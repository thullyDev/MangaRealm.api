from typing import List
import math

def paginate_items(data: List, page: int, limit: int):
	start = (page - 1) * limit
	end = start + limit
	items = data[start:end]
	pagination = {
			"pages": str(math.ceil(len(data) / limit)),
			"page": str(page),
	}
	
	return items, pagination 
