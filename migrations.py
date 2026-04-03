from list_class import List


def migrate_to_version0(data):
    """{
        'list_name': [ListItem...]
    }"""
    print("Migrated to: v0")
    return data | {
        "##migration_version": 0
    }


def migrate_to_version1(data):
    """{
        'list_name': List(
            items=[ListItem...],
            last_change_time=timestamp
            last_export_time=timestamp
        )
    }"""
    print("Migrated to: v1")
    res = {}
    for key, val in data.items():
        res[key] = List(val)
    res["##migration_version"] = 1
    return res


MIGRATIONS = [
    migrate_to_version0,
    migrate_to_version1
]

def migrate(data):
    current_version = data.get("##migration_version")
    start = 1
    if current_version is not None:
        start = current_version + 1
    if start < len(MIGRATIONS):
        for migr in MIGRATIONS[start:]:
            data = migr(data)
    return data

