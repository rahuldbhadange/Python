# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

"""RRPS event definitions.

Any events which are defined in this class as well as any defined in modules which have
been explicitly imported herein will be useable by integrators & followers.
"""

from datetime import datetime, timezone

from ioticlabs.dt.api.event.base import AssetEvent, field


class SapMasterDataSet(AssetEvent):
    """SAP Master Data AKA "Stammdata"

    The master data for any Aggregate or Engine. Basic information such as identification numbers
    and descriptions, customer number etc.

    Rarely (if ever) changes

    Any new version of this event is a *complete* replacement for any previously stored version

    Origin:
    - SAP API: "Equipment Master Data ODATA"
    """
    @classmethod
    def _default_version(cls):
        return 1

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                'type': 'record',
                'name': 'SapMasterData',
                'fields': [
                    field('EqunrAgg', 'string', doc='Equipment Number'),
                    field('MaktxAgg', 'string', doc=''),
                    field('MatnrAgg', 'string', doc='Material Number'),
                    field('MaktxEng', 'string',
                          doc='Material Description Short Text'),
                    field('SernrAgg', 'string', doc='Serial Number'),
                    field('Name1', 'string', doc='Customer Name'),
                    field('EqunrEng', 'string', doc='Equipment Number'),
                    field('MatnrEng', 'string', doc='Material Number'),
                    field('SernrEng', 'string', doc='Serial Number'),
                    field('Kunde', 'string',
                          doc='Customer to Whom Serial Number was Delivered'),
                    field(
                        'Datab', [{'type': 'long', 'logicalType': 'date'}], doc='Valid From Date'),
                    field(
                        'Datbi', [{'type': 'long', 'logicalType': 'date'}], doc='Valid To Date'),
                    field('Yybau', 'string', doc='Engine series')
                ]
            }
        }

    # Need to find out what fields are optional
    __non_empty_string_fields = ()
    __min_timestamp = datetime(2010, 1, 1, tzinfo=timezone.utc)

    def _validate_data(self):
        self.__validate_master_data(self.data)

    @classmethod
    def __validate_master_data(
            cls, parts,
            # Reduce lookups by providing local references for class functions used in validation
            non_empty_string_fields=__non_empty_string_fields,
            # min_timestamp=__min_timestamp
    ):
        # validate_master_date = cls.__validate_master_data

        for part in parts:
            # non-empty strings (more validation required?)
            assert all(part[field] for field in non_empty_string_fields)


class SapBomAsBuiltSet(AssetEvent):
    """SAP Bill of Materials "BoM" as it was originally built

    Complete list of all the materials that comprise the aggregate and engine. "Flat" representation to
    allow building into a tree structure using the parent/son relationship

    Rarely (if ever) changes - probably only if a mistake was made in the original

    Any new version of this event is a *complete* replacement for any previously stored version

    Origin:
    - SAP API: "Ibase as built Data ODATA"
    """
    @classmethod
    def _default_version(cls):
        return 1

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                'type': 'array',
                'items': {
                    'type': 'record',
                    'name': 'SapBomAsBuilt',
                    'fields': [
                        field('ParRecno', 'string',
                              doc='IB: Unique record number'),
                        field('SonRecno', 'string',
                              doc='IB: Unique record number'),
                        field('Matnr', 'string', doc='Material Number'),
                        field('Sernr', 'string', doc='IB: Serial numbers'),
                        field('Descr', 'string',
                              doc='IB: IBase Short Text/Description'),
                        field('Valfr', 'string', doc='Valid from'),
                        field('Valto', 'string', doc='Valid to'),
                        field('Yyemrel', 'string', doc='Emission relevance')
                    ]
                }
            }
        }

    __non_empty_string_fields = ()  # Need to find out what fields are optional
    __min_timestamp = datetime(2010, 1, 1, tzinfo=timezone.utc)

    def _validate_data(self):
        self.__validate_master_data(self.data)

    @classmethod
    def __validate_master_data(
            cls, parts,
            # Reduce lookups by providing local references for class functions used in validation
            non_empty_string_fields=__non_empty_string_fields,
            # min_timestamp=__min_timestamp
    ):
        # validate_master_date = cls.__validate_master_data

        for part in parts:
            # non-empty strings (more validation required?)
            assert all(part[field] for field in non_empty_string_fields)


class SapEquipmentHistoryMixin():
    """SAP Equipment History - historical events in the life of the asset

    Super class of all the history events
    - One of these events for every historical event (that SAP knows about) in the life of the asset
    - Each subclass corresponds to a different type of historical event e.g. purchase, delivery, etc
    - Will contain the list of relevant documents in the body. These documents are the detail of what went
      on as part of the event. This look-up is done via the EQUNR field

    Note: Don't be confused by DocType. These are *not* documents, but the payload list is.

    Occur randomly through the life of an asset

    Any new version of any of these events should be considered a completely new event

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    @classmethod
    def _default_version(cls):
        return 1

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                "type": "record",
                "name": "SapEquipmentHistory",
                "fields": [
                    field('Sernr', 'string', doc='Serial number'),
                    field('Equnr', 'string', doc='Equipment Number'),
                    field('Obknr', 'long', doc='Object list number'),
                    field('Docnr', 'string', doc='Business Document Number'),
                    field('Docitm', 'string',
                          doc='Business Document item number'),
                    field(
                        'Datum', [{'type': 'long', 'logicalType': 'date'}], doc='Date'),
                    field('Doctype', 'string', doc='Doctype'),
                    field('Ktext', 'string', doc='Description'),
                    field('Documents', {
                        "type": "array",
                        "items": {
                            "type": "record",
                            "name": "Documents",
                            "fields": [
                                field('Equnr', 'string',
                                      doc='Equipment Number'),
                                field('Instid', 'string',
                                      doc='Instance Ident. in BOR Compat. Persistent Object References'),
                                field(
                                    'Docnam', 'string', doc='Name of document, folder or distribution list'),
                                field('Docdes', 'string',
                                      doc='Short description of contents'),
                                field(
                                    'Docla', 'string', doc='Language in Which Document Is Created'),
                                field(
                                    'Crdat', [{'type': 'long', 'logicalType': 'date'}], doc='Date created'),
                                field(
                                    'Chdat', [{'type': 'long', 'logicalType': 'date'}], doc='Last Changed On'),
                                field('FileExt', 'string',
                                      doc='File extension for PC application')
                            ]
                        }
                    })
                ]
            }
        }

    # Need to find out what fields are optional
    __non_empty_string_fields = ()
    __min_timestamp = datetime(2010, 1, 1, tzinfo=timezone.utc)

    def _validate_data(self):
        self.__validate_master_data(self.data)

    @classmethod
    def __validate_master_data(
            cls, parts,
            # Reduce lookups by providing local references for class functions used in validation
            non_empty_string_fields=__non_empty_string_fields,
            # min_timestamp=__min_timestamp
    ):
        # validate_master_date = cls.__validate_master_data

        for part in parts:
            # non-empty strings (more validation required?)
            assert all(part[field] for field in non_empty_string_fields)


class SapEquipmentHistoryDeliverySet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Delivery

    Event corresponding to the delivery of an asset: Doctype DELI

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryMaintenanceContractSet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Maintenance Contract

    Event corresponding to the creation of the maintenance contract: Doctype MAIN

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryMaterialMovementSet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Material Movement

    Event corresponding to the Movement of the Material: Doctype MOVE

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryInspectionLotSet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Inspection lot

    Event corresponding to the Inspection of the asset: Doctype INLO

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryProductionOrderSet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Production Order

    Event corresponding to the Production Order of the asset: Doctype PROD

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryPhysicalInventorySet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Physical Inventory

    Event corresponding to the Physical Inventory of the asset: Doctype INVE

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryPurchaseOrderSet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Purchase Order

    Event corresponding to the Purchase Order of the asset: Doctype PURO

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryPmOrderSet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - PM Order  # todo - not sure what this is

    Event corresponding to the PM Order of the asset: Doctype PMOD

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryNotificationSet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Notification

    Event corresponding to a Notification about the asset: Doctype NOTI

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryInstallationHistorySet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Installation History

    Event corresponding to an Installation of the asset: Doctype HIST

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapEquipmentHistoryUnknownSet(SapEquipmentHistoryMixin, AssetEvent):
    """SAP Equipment History - Unknown

    Event corresponding to an a history event with an unknown Doctype

    Origin:
    - SAP API: "Equipment History ODATA" for the base data
    - SAP API: "Equipment Document attachment list ODATA" for the attached documents
    """
    pass


class SapWarrantyRecallSet(AssetEvent):
    """SAP Warranty Recall"

    Origin:
    - SAP API: "Warranty recall ODATA"
    """
    @classmethod
    def _default_version(cls):
        return 1

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                'type': 'array',
                'items': {
                    'type': 'record',
                    'name': 'SapWarrantyRecall',
                    'fields': [
                        field('Pnguid', 'string',
                              doc='Internal Number of iPPE Node'),
                        field('Pncnt', 'string', doc='Internal Counter'),
                        field('HPntext', 'string',
                              doc='Text in Warranty Claim Header'),
                        field('Clmno', 'string', doc='Number of Warranty Claim'),
                        field('Clmty', 'string', doc='Category'),
                        field(
                            'Refdt', [{'type': 'long', 'logicalType': 'date'}], doc='Reference Date'),
                        field('Refno', 'string', doc='External Number of Claim'),
                        field('Sernr', 'string', doc='Serial Number'),
                        field('Equnr', 'string', doc='Equipment Number'),
                        field('Parnr', 'string', doc='Partner'),
                        field('Astate', 'string',
                              doc='Processing Status of Warranty Claim'),
                        field(
                            'Abdes', 'string', doc='Description of Processing Status of Warranty Claim'),
                        field('YywtyState', 'string',
                              doc='TOGA: Warranty status'),
                        field('YycifPrio', 'string',
                              doc='TOGA: Priority of corrective action'),
                        field('YycifPriotxt', 'string',
                              doc='TOGA: Priority of corrective action'),
                        field(
                            'Yyroopen', 'string', doc='TOGA: Repair order open date (date the customer complaint ha'),
                        field('Yyroclosed', 'string',
                              doc='TOGA: Repair order closed date'),
                        field('YydueDate', 'string', doc='Due Date'),
                        field('Yysystfir', 'string',
                              doc='TOGA: FI system reimbursement'),
                        field('Yyclmtype', 'string', doc='Claim type'),
                        field('Yyclmtypetxt', 'string',
                              doc='TOGA: Claim type'),
                        field('Yyrepcountry', 'string',
                              doc='TOGA: Repair Country'),
                        field('DocLink', 'string', doc='Documentation Object')
                    ]
                }
            }
        }

    # Need to find out what fields are optional
    __non_empty_string_fields = ()
    __min_timestamp = datetime(2010, 1, 1, tzinfo=timezone.utc)

    def _validate_data(self):
        self.__validate_master_data(self.data)

    @classmethod
    def __validate_master_data(
            cls, parts,
            # Reduce lookups by providing local references for class functions used in validation
            non_empty_string_fields=__non_empty_string_fields,
            # min_timestamp=__min_timestamp
    ):
        # validate_master_date = cls.__validate_master_data

        for part in parts:
            # non-empty strings (more validation required?)
            assert all(part[field] for field in non_empty_string_fields)


class TalendTimDocumentSet(AssetEvent):
    """Talend "tim" Document list

    Complete list of the "tim" documents for this asset from the Talend API

    Rarely (if ever) changes - probably only if a mistake was made in the original

    Any new version of this event is a *complete* replacement for any previously stored version

    Origin:
    - MVP Digital Twin: Talend Services for IOTIC
    """
    @classmethod
    def _default_version(cls):
        return 1

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                'type': 'array',
                'items': {
                    'type': 'record',
                    'name': 'TalendTimDocument',
                    'fields': [
                        field('documentLabel', 'string', doc='Document Label'),
                        field('documentName', 'string', doc='Document Name'),
                        field('documentDescription', 'string',
                              doc='Document Description'),
                        field('documentType', 'string', doc='Document Type'),
                        field('enterDate', 'string', doc='Document Date')
                    ]
                }
            }
        }

    __non_empty_string_fields = ('documentLabel', 'documentName')
    __min_timestamp = datetime(2010, 1, 1, tzinfo=timezone.utc)

    def _validate_data(self):
        self.__validate_master_data(self.data)

    @classmethod
    def __validate_master_data(
            cls, parts,
            # Reduce lookups by providing local references for class functions used in validation
            non_empty_string_fields=__non_empty_string_fields,
            # min_timestamp=__min_timestamp
    ):
        # validate_master_date = cls.__validate_master_data

        for part in parts:
            # non-empty strings (more validation required?)
            assert all(part[field] for field in non_empty_string_fields)


class TalendFirmwareSet(AssetEvent):
    """Talend firmware version number

    Version number of the firmware for the returned serial number. To be merged in with the Stamm data
    in the view

    Will change every time the firmware is updated.

    Any new version of this event is a *complete* replacement for any previously stored version

    Origin:
    - MVP Digital Twin: Talend Services for IOTIC
    """
    @classmethod
    def _default_version(cls):
        return 1

    @classmethod
    def _known_versions(cls):
        return {
            1: {
                'type': 'record',
                'name': 'TalendFirmware',
                'fields': [
                    field('serialNumber', 'string'),
                    field('version', 'string')
                ]
            }
        }

    __non_empty_string_fields = ()
    __min_timestamp = datetime(2010, 1, 1, tzinfo=timezone.utc)

    def _validate_data(self):
        self.__validate_data(self.data)

    @classmethod
    def __validate_data(
            cls, parts,
            # Reduce lookups by providing local references for class functions used in validation
            non_empty_string_fields=__non_empty_string_fields,
            # min_timestamp=__min_timestamp
    ):
        # validate_date = cls.__validate_data

        for part in parts:
            # non-empty strings (more validation required?)
            assert all(part[field] for field in non_empty_string_fields)


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
                        field("WeatherType", "date"),
                        field("Position", "float"),
                        field("WindSpeed", "float"),
                        field("WindDirection", "float"),
                        field("WindGust", "float"),
                        field("Humidity", "string"),
                        field("Visibility", "string"),
                        field("Temperature", "float"),
                        field("FeelsLikeTemperature", "float"),
                        field("MaxUVIndex", "string"),
                        field("PrecipitationProbability", "string")

                        #
                        # field("time", "date"),
                        # field("feels", "float"),
                        # field("gust", "float"),
                        # field("humid", "float"),
                        # field("temp", "float"),
                        # field("visib", "string"),
                        # field("winddir", "string"),
                        # field("windspd", "float"),
                        # field("uv", "float"),
                        # field("type", "string"),
                        # field("prob", "string")
                    ]
            }

        }
}

    def _validate_data(self):
        super()._validate_data()
        assert all(self.data[field_] for field_ in self.__non_empty_string_fields)
