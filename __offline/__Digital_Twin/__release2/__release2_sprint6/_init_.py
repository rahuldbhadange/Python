# Copyright (c) 2018 Rolls-Royce Power Systems AG. All rights reserved.

"""RRPS event definitions.

Any events which are defined in this class as well as any defined in modules which have
been explicitly imported herein will be useable by integrators & followers.
"""

from datetime import datetime, timezone

from ioticlabs.dt.api.event.base import AssetEvent, field


class SAPBomPartSupersessionHistorySet(AssetEvent):
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
