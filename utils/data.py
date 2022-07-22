

def short(objects: list) -> list:
    return [[str(field)[0:45] + "..." if (len(str(field)) > 45) else field for field in object] for object in objects]
