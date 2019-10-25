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
