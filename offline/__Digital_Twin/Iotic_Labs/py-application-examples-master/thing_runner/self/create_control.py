def create_control(self, pid, callback, callback_parsed=None):
    """Create a control for this Thing with a local point id (pid) and a control request feedback
    Returns a new [Control](Point.m.html#IoticAgent.IOT.Point.Control) object
    or the existing one if the Control already exists
    Raises [IOTException](./Exceptions.m.html#IoticAgent.IOT.Exceptions.IOTException)
    containing the error if the infrastructure detects a problem
    Raises [LinkException](../Core/AmqpLink.m.html#IoticAgent.Core.AmqpLink.LinkException)
    if there is a communications problem between you and the infrastructure
    `pid` (required) (string) local id of your Control
    `callback` (required) (function reference) callback function to invoke on receipt of a control request.
    The callback receives a single dict argument, with keys of:
        #!python
        'data'      # (decoded or raw bytes)
        'mime'      # (None, unless payload was not decoded and has a mime type)
        'subId'     # (the global id of the associated subscripion)
        'entityLid' # (local id of the Thing to which the control belongs)
        'lid'       # (local id of control)
        'confirm'   # (whether a confirmation is expected)
        'requestId' # (required for sending confirmation)
    `callback_parsed` (optional) (function reference) callback function to invoke on receipt of control data. This
    is equivalent to `callback` except the dict includes the `parsed` key which holds the set of values in a
    [PointDataObject](./Point.m.html#IoticAgent.IOT.Point.PointDataObject) instance. If both
    `callback_parsed` and `callback` have been specified, the former takes precedence and `callback` is only called
    if the point data could not be parsed according to its current value description.
    `NOTE`: `callback_parsed` can only be used if `auto_encode_decode` is enabled for the client instance.
    """
    logger.info("create_control(pid=\"%s\", control_cb=%s) [lid=%s]", pid, callback, self.__lid)
    if callback_parsed:
        callback = self._client._get_parsed_control_callback(callback_parsed, callback)
    return self.__create_point(R_CONTROL, pid, control_cb=callback)
