    @classmethod
    def __call_data(cls, endpoint, usr, pwd, timeout):

        http_error_msg = ''
        data = None

        try:
            resp = requests.get(endpoint, auth=(usr, pwd), verify=False, timeout=timeout)
            log.error("Response status: %s", resp.status_code)

            if resp.status_code == requests.codes['ok']:
                results = resp.json()
                try:
                    data = results['d']['results']
                # Strip date string values and convert to epoch longs
                    for item in data:
                        item['Refdt'] = int(re.findall(r'\d+', item['Refdt'])[0])
                except ValueError as ex:
                    log.error(ex)
            elif 400 <= resp.status_code < 500:
                http_error_msg = '%s Client Error: %s for url: %s' % (resp.status_code, resp.reason, resp.url)
            elif 500 <= resp.status_code < 600:
                http_error_msg = '%s Server Error: %s for url: %s' % (resp.status_code, resp.reason, resp.url)

            if http_error_msg:
                from requests import HTTPError
                raise HTTPError(http_error_msg, response=resp)

            log.error("Endpoint response failed: %s", resp.status_code)

        except requests.exceptions.RequestException as ex:
            log.error(ex)

        return data
