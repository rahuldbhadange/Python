def get_template(self, data=None):  # noqa (complexity)

    """
    Get new template which represents the values of this point in a
    [PointDataObject](./Point.m.html#IoticAgent.IOT.Point.PointDataObject).
    If data is set (to a dictionary), use this to populate the created template.
    """

    
    with self.__lock:
        if self.__value_templates is None and self.__last_parse_ok:
            try:
                self.__refresh()
            except RefreshException:
                # Point has no (useable) values - don't try to refetch again
                self.__last_parse_ok = False
                raise
        if self.__value_templates is None:
            raise ValueError('Point has no values')
        if data is None:
            template = PointDataObject(self.__value_templates, self.__filter)
        else:
            while True:
                try:
                    template = PointDataObject._from_dict(self.__value_templates, self.__filter, data)
                except:
                    # parsing has failed for first time since refresh so try again
                    if self.__last_parse_ok:
                        logger.debug('Failed to parse data from for point %s, refreshing', self.__point)
                        self.__last_parse_ok = False
                        try:
                            self.__refresh()
                        except RefreshException:
                            break
                    else:
                        raise
                else:
                    self.__last_parse_ok = True
                    break
        return template
