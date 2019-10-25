from datetime import datetime, timezone

from ioticlabs.dt.api.event.base import AssetEvent, field




class LocationSetMixin:
    """Mixin for events containing data about the location of the asset. Provides attribute _location_field, a record
    containing Latitude and Longitude float fields, which it expects/validates at the top level of the event record.
    This Location can be None if no location data is available.
    """

    _location_field = field('Location', ['null', {
        'type': 'record',
        'name': 'Location',
        'fields': [
            field('Latitude', 'float', doc='Asset latitude'),
            field('Longitude', 'float', doc='Asset longitude')
        ]
    }], doc='Asset location')

    __coordinate_dimensions = {'Latitude': (-90.0, 90.0), 'Longitude': (-180.0, 180.0)}

    def _validate_data(self):
        super()._validate_data()

        # TODO: restructure FieldDataErrorSet so wrapping array for SuccessSet is unnecessary
        data = self.data if isinstance(self.data, list) else [self.data]
        for item in data:
            self.__check_location(item)

    @classmethod
    def __check_location(cls, data):
        location = data['Location']
        if location is None:
            return
        for coordinate, (minval, maxval) in cls.__coordinate_dimensions.items():
            assert isinstance(location[coordinate], float)
            assert minval <= location[coordinate] <= maxval


class FieldDataSuccessSet(LocationSetMixin, AssetEvent):
    """FieldDataSuccessSet
    Event published when new or changed asset field data source is successfully
    shared. Provides the most recent location information in the blob, if any is
    available.

    Origin:
    - Internal
    """

    __non_empty_string_fields = ('Blobname',)

    @classmethod
    def _default_version(cls):
        return 2

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                'type': 'record',
                'name': 'FieldDataSuccess',
                'fields': [
                    field('Blobname', 'string', doc='Blob Name'),
                ]
            },
            2: {
                'type': 'record',
                'name': 'FieldDataSuccess',
                'fields': [
                    field('Blobname', 'string', doc='Blob Name'),
                    cls._location_field,  # from LocationSetMixin
                ]
            },
        }

    def _validate_data(self):
        super()._validate_data()
        assert all(self.data[field_] for field_ in self.__non_empty_string_fields)


class FieldDataErrorSet(LocationSetMixin, AssetEvent):
    """FieldDataErrorSet
    Event published when errors were encountered processing field data blobs
    shared. Provides the most recent location information in the blob, if any is
    available.

    Origin:
    - Internal
    """
    __non_empty_string_fields = ('Blobname', 'Error')

    @classmethod
    def _default_version(cls):
        return 2

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                'type': 'array',
                'items': {
                    'type': 'record',
                    'name': 'FieldDataError',
                    'fields': [
                        field('Blobname', 'string', doc='Blob Name'),
                        field('Error', 'string', doc='Error'),
                    ]
                },
            },
            2: {
                'type': 'array',
                'items': {
                    'type': 'record',
                    'name': 'FieldDataError',
                    'fields': [
                        field('Blobname', 'string', doc='Blob Name'),
                        cls._location_field,  # from LocationSetMixin
                        field('Error', 'string', doc='Error'),
                    ]
                },
            },
        }

    def _validate_data(self):
        super()._validate_data()
        for item in self.data:
            assert all(item[field_] for field_ in self.__non_empty_string_fields)


class WeatherInfoSet(LocationSetMixin, AssetEvent):
    """WeatherInfoSet
    Event published when new or changed asset field data source is successfully
    shared. Provides the most recent location information in the blob, if any is
    available.

    Origin:
    - Internal
    """

    __non_empty_string_fields = ('Blobname',)

    @classmethod
    def _default_version(cls):
        return 1

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                {
                    'type': 'record',
                    'name': 'WeatherInfoSet',
                    'fields': [
                        field("WeatherType", "string"),
                        field("Position", "string"),
                        field("WindSpeed", "float"),
                        field("WindDirection", "float"),
                        field("WindGust", "float"),
                        field("Humidity", "float"),
                        field("Visibility", "string"),
                        field("Temperature", "float"),
                        field("FeelsLikeTemperature", "float"),
                        field("MaxUVIndex", "float"),
                        field("PrecipitationProbability", "string"),
                        field("WeatherStation", "KETTERING, ENGLAND"),
                        field("WeatherProvider", "mettofice_forecast")


                    ]
            }

        }
}

    def _validate_data(self):
        super()._validate_data()
        assert all(self.data[field_] for field_ in self.__non_empty_string_fields)
