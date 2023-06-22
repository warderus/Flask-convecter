from flask import Flask, request, redirect, render_template

import convecter

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/response', methods=['POST', 'GET'])
def response():
    if request.method == 'POST':
        text = request.form['message']
        convecter.write_data_to_file(text)
        convecter.convecter()
        clients = convecter.file_to_text()
    else:
        return redirect('/')
    return render_template('response.html', context=clients)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8090)
