from bottle import route, run, request, abort

@route('/', method='GET')
def reject():
    abort(400, 'Bad request')

@route('/', method='POST')
def index():
    print request.POST
    return '<b>Ok!</p>'

run(host='0.0.0.0', port=8080)
