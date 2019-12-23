from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    return Response('Hello World!')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)




'''werkzeug.serving.run_simple(hostname, port, 
application, use_reloader=False, use_debugger=False, use_evalex=True, 
extra_files=None, reloader_interval=1, reloader_type='auto', 
threaded=False, processes=1, request_handler=None, static_files=None, 
passthrough_errors=False, ssl_context=None)
'''