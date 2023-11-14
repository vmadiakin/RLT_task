import asyncio
from datetime import timedelta, datetime
from motor.motor_asyncio import AsyncIOMotorClient


async def aggregate_salaries(dt_from, dt_upto, group_type):
    dt_from = datetime.fromisoformat(dt_from)
    dt_upto = datetime.fromisoformat(dt_upto)

    client = AsyncIOMotorClient('mongodb://localhost:27017', connect=False)
    db = client['mongodb']
    collection = db['sample_collection']

    current_date = dt_from
    all_days = []
    while current_date <= dt_upto:
        all_days.append(current_date)
        if group_type == "hour":
            current_date += timedelta(hours=1)
        elif group_type == "day":
            current_date += timedelta(days=1)
        elif group_type == "month":
            next_month = (
                    current_date.replace(day=1) + timedelta(days=32)
            ).replace(day=1)
            current_date = next_month

    date_format_dict = {
        "hour": "%Y-%m-%dT%H:00:00",
        "day": "%Y-%m-%dT00:00:00",
        "month": "%Y-%m-01T00:00:00"
    }
    date_format = date_format_dict.get(group_type)
    if not date_format:
        return {"error": "Invalid group_type"}

    pipeline = [
        {"$match": {"dt": {"$gte": dt_from, "$lte": dt_upto}}},
        {"$group": {
            "_id": {"$dateToString": {"format": date_format, "date": "$dt"}},
            "total_value": {"$sum": "$value"}
        }},
        {"$sort": {"_id": 1}}
    ]

    result = await collection.aggregate(pipeline).to_list(None)

    data_dict = {entry["_id"]: entry["total_value"] for entry in result}

    dataset = [data_dict.get(day.strftime(date_format), 0) for day in all_days]
    labels = [day.strftime(date_format) for day in all_days]

    return {"dataset": dataset, "labels": labels}


async def main():
    data = {
        "dt_from": "2022-10-01T00:00:00",
        "dt_upto": "2022-11-30T23:59:00",
        "group_type": "day"
    }

    result = await aggregate_salaries(data["dt_from"], data["dt_upto"], data["group_type"])
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

