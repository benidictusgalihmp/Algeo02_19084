from flask import Flask,request,url_for,redirect,render_template
from werkzeug.utils import secure_filename
from backendTest import *

namaFile, kalimatFile = getFiles()

app = Flask(__name__, template_folder = 'templates', static_folder = '../test')
app.config['UPLOAD_FOLDER'] ='../test'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}
app.config["DEBUG"] = True

@app.route('/', methods=['GET','POST'])
def home():
    namaFile, kalimatFile = getFiles()
    if request.method == 'POST' and 'Query' in request.form :
        query = request.form['Query']
        return redirect(url_for('termsFile', query = query))
    elif request.method == 'POST' and 'file' in request.files :
        files = request.files.getlist('file')
        for file in files :
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        namaFile, kalimatFile = getFiles()
        return render_template('main.html', namaFile = namaFile)
    else :
        return render_template('main.html', namaFile = namaFile)

@app.route('/<query>', methods=['GET', 'POST'])
def termsFile(query):
    namaFile, kalimatFile = getFiles()
    if request.method == 'POST' and 'Query' in request.form :
        query = request.form['Query']
        return redirect(url_for('termsFile', query = query))
    elif request.method == 'POST' and 'file' in request.files :
        files = request.files.getlist('file')
        for file in files :
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        namaFile, kalimatFile = getFiles()
        return render_template('main.html', namaFile = namaFile)
    else :
        if len(lowStemStopSplit(query)) == 0 :
            return render_template('main.html', namaFile = namaFile)
        else :
            sortedNamaFile = namaFile

            queryTerms = countTerm(query, query)
            #sumFile = jumlah kata pada setiap file
            sumFile = getFileSum(kalimatFile)

            #fileTerms = perhitungan term pada kalimatFile 
            fileTerms = getFileTerms(kalimatFile, query)

            #sim = Similarity dari query dengan semua file
            sim = getAllSim(queryTerms, fileTerms)

            #Buat di rank searchnya nanti
            n = len(sim) 
            for i in range(n-1): 
                for j in range(0, n-i-1):  
                    if sim[j] < sim[j+1] : 
                        sim[j], sim[j+1] = sim[j+1], sim[j]
                        sortedNamaFile[j], sortedNamaFile[j+1] = sortedNamaFile[j+1], sortedNamaFile[j]
                        kalimatFile[j], kalimatFile[j+1] = kalimatFile[j+1], kalimatFile[j]
                        fileTerms[j], fileTerms[j+1] = fileTerms[j+1], fileTerms[j]
                        sumFile[j], sumFile[j+1] = sumFile[j+1], sumFile[j]

            kalimatPertamaFile = []
            for i in kalimatFile :
                kalimatPertamaFile.append(i.split('.')[0])

            printTable = []
            for j in range(len(queryTerms)):
                if (queryTerms[j][1] >= 1):
                    printTerms = []
                    printTerms.append(queryTerms[j][0])
                    printTerms.append(queryTerms[j][1])
                    for i in range(n):
                        printTerms.append(fileTerms[i][j][1])
                    printTable.append(printTerms)
            for i in range(len(printTable)):
                print(printTable[i])
            return render_template('main.html', sortedNamaFile = sortedNamaFile, namaFile = namaFile, sumFile = sumFile, sim = sim, kalimatPertamaFile = kalimatPertamaFile, printTable = printTable)

if __name__ == '__main__' :
    app.run()