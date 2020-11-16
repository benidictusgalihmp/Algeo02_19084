from flask import Flask,request,url_for,redirect,render_template
from werkzeug.utils import secure_filename
from backendTest import *

extension = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] ='../test'
app.config["DEBUG"] = True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extension

@app.route('/', methods=['GET','POST'])
def home():
    namaFile, kalimatFile = getFiles()
    if request.method == 'POST' and 'Query' in request.form :
        query = request.form['Query']
        return redirect(url_for('termsFile', query = query))
    elif request.method == 'POST' and 'file' in request.files :
        files = request.files.getlist('file')
        for file in files :
            if allowed_file(file.filename) :
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        namaFile, kalimatFile = getFiles()
        return render_template('main.html', namaFile = namaFile, show = 0)
    else :
        return render_template('main.html', namaFile = namaFile, show = 0)

@app.route('/<query>', methods=['GET', 'POST'])
def termsFile(query):
    namaFile, kalimatFile = getFiles()
    if request.method == 'POST' and 'Query' in request.form :
        query = request.form['Query']
        return redirect(url_for('termsFile', query = query))
    elif request.method == 'POST' and 'file' in request.files :
        files = request.files.getlist('file')
        for file in files :
            if allowed_file(file.filename) :
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        namaFile, kalimatFile = getFiles()
        return render_template('main.html', namaFile = namaFile, show = 0)
    else :
        if len(lowStemStopSplit(query)) == 0 :
            return render_template('main.html', namaFile = namaFile, show = 0)
        else :
            sortedNamaFile = namaFile

            queryTerms = countTerm(query, query)
            #sumFile = jumlah kata pada setiap file
            sumFile = getFileSum(kalimatFile)

            #fileTerms = perhitungan term pada kalimatFile
            fileTerms = getFileTerms(kalimatFile, query)

            #sim = Similarity dari query dengan semua file
            sim = getAllSim(queryTerms, fileTerms)

            #Buat di rank search
            n = len(sim)
            for i in range(n-1):
                for j in range(0, n-i-1):
                    if sim[j] < sim[j+1] :
                        sim[j], sim[j+1] = sim[j+1], sim[j]
                        sortedNamaFile[j], sortedNamaFile[j+1] = sortedNamaFile[j+1], sortedNamaFile[j]
                        kalimatFile[j], kalimatFile[j+1] = kalimatFile[j+1], kalimatFile[j]
                        fileTerms[j], fileTerms[j+1] = fileTerms[j+1], fileTerms[j]
                        sumFile[j], sumFile[j+1] = sumFile[j+1], sumFile[j]
            kalimatPertamaFile = getKalimatPertama(kalimatFile)

            #Buat di tabel
            printTable = getTableValue(queryTerms, fileTerms)

            return render_template('main.html', length = len(sim), sortedNamaFile = sortedNamaFile, namaFile = namaFile, sim = sim, sumFile = sumFile, kalimatPertamaFile = kalimatPertamaFile, printTable = printTable, show = 1)

@app.route('/Perihal')
def perihal():
    return render_template('perihal.html')

if __name__ == '__main__' :
    app.run()
