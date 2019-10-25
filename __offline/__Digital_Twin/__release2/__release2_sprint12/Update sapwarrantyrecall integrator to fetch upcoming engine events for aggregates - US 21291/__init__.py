class SapWarrantyRecallSet(AssetEvent):
    """SAP Warranty Recall"

    Origin:
    - SAP API: "Warranty recall ODATA"
    """
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
                    'name': 'SapWarrantyRecall',
                    'fields': [
                        field('Pnguid', 'string', doc='Internal Number of iPPE Node'),
                        field('Pncnt', 'string', doc='Internal Counter'),
                        field('HPntext', 'string', doc='Text in Warranty Claim Header'),
                        field('Clmno', 'string', doc='Number of Warranty Claim'),
                        field('Clmty', 'string', doc='Category'),
                        field('Refdt', [{'type': 'long', 'logicalType': 'date'}], doc='Reference Date'),
                        field('Refno', 'string', doc='External Number of Claim'),
                        field('Sernr', 'string', doc='Serial Number'),
                        field('Equnr', 'string', doc='Equipment Number'),
                        field('Parnr', 'string', doc='Partner'),
                        field('Astate', 'string', doc='Processing Status of Warranty Claim'),
                        field('Abdes', 'string', doc='Description of Processing Status of Warranty Claim'),
                        field('YywtyState', 'string', doc='TOGA: Warranty status'),
                        field('YycifPrio', 'string', doc='TOGA: Priority of corrective action'),
                        field('YycifPriotxt', 'string', doc='TOGA: Priority of corrective action'),
                        field('Yyroopen', 'string', doc='TOGA: Repair order open date (date the customer complaint ha'),
                        field('Yyroclosed', 'string', doc='TOGA: Repair order closed date'),
                        field('YydueDate', 'string', doc='Due Date'),
                        field('Yysystfir', 'string', doc='TOGA: FI system reimbursement'),
                        field('Yyclmtype', 'string', doc='Claim type'),
                        field('Yyclmtypetxt', 'string', doc='TOGA: Claim type'),
                        field('Yyrepcountry', 'string', doc='TOGA: Repair Country'),
                        field('DocLink', 'string', doc='Documentation Object')
                    ]
                }
            },
            2: {
                'type': 'array',
                'items': {
                    'type': 'record',
                    'name': 'SapWarrantyRecall',
                    'fields': [
                        field('Pnguid', 'string', doc='Internal Number of iPPE Node'),
                        field('Pncnt', 'string', doc='Internal Counter'),
                        field('HPntext', 'string', doc='Text in Warranty Claim Header'),
                        field('Clmno', 'string', doc='Number of Warranty Claim'),
                        field('Clmty', 'string', doc='Category'),
                        field('Refdt', [{'type': 'long', 'logicalType': 'date'}], doc='Reference Date'),
                        field('Refno', 'string', doc='External Number of Claim'),
                        field('Sernr', 'string', doc='Serial Number'),
                        field('Equnr', 'string', doc='Equipment Number'),
                        field('Parnr', 'string', doc='Partner'),
                        field('Astate', 'string', doc='Processing Status of Warranty Claim'),
                        field('Abdes', 'string', doc='Description of Processing Status of Warranty Claim'),
                        field('YywtyState', 'string', doc='TOGA: Warranty status'),
                        field('YycifPrio', 'string', doc='TOGA: Priority of corrective action'),
                        field('YycifPriotxt', 'string', doc='TOGA: Priority of corrective action'),
                        field('Yyroopen', 'string', doc='TOGA: Repair order open date (date the customer complaint ha'),
                        field('Yyroclosed', 'string', doc='TOGA: Repair order closed date'),
                        field('YydueDate', 'string', doc='Due Date'),
                        field('Yysystfir', 'string', doc='TOGA: FI system reimbursement'),
                        field('Yyclmtype', 'string', doc='Claim type'),
                        field('Yyclmtypetxt', 'string', doc='TOGA: Claim type'),
                        field('Yyrepcountry', 'string', doc='TOGA: Repair Country'),
                        field('DocLink', 'string', doc='Documentation Object'),
                        field('AssetType', 'string', doc='The type of asset (ENG or SYS)')
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
