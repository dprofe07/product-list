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
        )
    }"""
    print("Migrated to: v1")
    res = {}
    for key, val in data.items():
        if key == "##migration_version":
            continue
        res[key] = List(val)
    res["##migration_version"] = 1
    return res


def migrate_to_version2(data):
    """{
        'list_name': List(
            items=[ListItem...],
            last_change_time=timestamp,
            last_export_time=timestamp
        )
    }"""
    print("Migrated to: v2")
    res = {}
    for key, val in data.items():
        if key == "##migration_version":
            continue
        res[key] = List(val.items, val.last_change_time)
    res["##migration_version"] = 2
    return res


MIGRATIONS = [
    migrate_to_version0,
    migrate_to_version1,
    migrate_to_version2,
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

