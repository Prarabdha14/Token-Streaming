ACTIVE_GENERATIONS = {}

def set_generation_status(generation_id: str, is_active: bool):
    ACTIVE_GENERATIONS[generation_id] = is_active

def get_generation_status(generation_id: str) -> bool:
    return ACTIVE_GENERATIONS.get(generation_id, False)

def remove_generation(generation_id: str):
    if generation_id in ACTIVE_GENERATIONS:
        del ACTIVE_GENERATIONS[generation_id]
