from typing import List

def paginate_items(data: List, page: int, limit: int):
	start = (page - 1) * limit
	end = start + limit
	items = data[start:end]
	pagination = {
			"pages": math.ceil(len(data) / limit),
			"page": page,
	}
	
	return items, pagination 
