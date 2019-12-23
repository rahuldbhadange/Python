try:
    start_time = dateutil.parser.parse(start)
    stop_time = dateutil.parser.parse(stop)

    if start_time >= stop_time:
        raise ValueError("Stop time must be after start time")

    converted_start_time = start_time.isoformat()
    converted_stop_time = stop_time.isoformat()
except ValueError as ex:
    logger.exception("parse stop and start failed")
    raise BadRequest({"code": "parse stop and start failed", "description": str(
        ex)}, status_code=400)


for item in items:
    if self._is_kif_item_closed(item):
        clmno = item.get("Clmno", "")
        if not clmno:
            raise ValueError("keying off Clmno for kif data but field missing")

        # this item has been closed so remove from upcoming events
        remove_list.append({"asset_id": event.asset, "_clmno": clmno})
        continue
    if 

    mapped_item = self._create_kif_data(event, item)
    update_list.append(mapped_item)
