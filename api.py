from os import name
import flask
from flask import Flask,request,url_for,redirect,render_template
from flask import app
from werkzeug.utils import html
from backendTest import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        variable = request.form['Query']
        return redirect(url_for('termsFile', name = variable))
    else:
        return render_template('main.html')

@app.route('/query', methods=['GET'])
def termsFile(name):
    queryTerms = countTerm(name, name)

    #namaFile = list nama file
    #kalimatFile = list semua kalimat pada setiap file
    namaFile, kalimatFile = getFiles()

    #sumFile = jumlah kata pada setiap file
    sumFile = getFileSum(kalimatFile)

    #fileTerms = perhitungan term pada kalimatFile 
    fileTerms = getFileTerms(kalimatFile, name)

    #sim = Similarity dari query dengan semua file
    sim = getAllSim(queryTerms, fileTerms)

    #Buat di rank searchnya nanti
    n = len(sim) 
    for i in range(n-1): 
        for j in range(0, n-i-1):  
            if sim[j] < sim[j+1] : 
                sim[j], sim[j+1] = sim[j+1], sim[j]
                namaFile[j], namaFile[j+1] = namaFile[j+1], namaFile[j]
                kalimatFile[j], kalimatFile[j+1] = kalimatFile[j+1], kalimatFile[j]
                fileTerms[j], fileTerms[j+1] = fileTerms[j+1], fileTerms[j]
                sumFile[j], sumFile[j+1] = sumFile[j+1], sumFile[j]
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
    return render_template('main.html')

app.run()