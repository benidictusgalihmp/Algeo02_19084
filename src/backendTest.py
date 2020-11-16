#install Sastrawi dulu

import os
from os import name
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopword = StopWordRemoverFactory().create_stop_word_remover()

def lowStemStopSplit(strings) :
# Mereturn kata-kata yang ada di strings setelah dilowercase, distem, dan dihilangkan stopwordsnya
    strings = strings.lower()
    strings = stemmer.stem(strings)
    strings = stopword.remove(strings)
    strings = strings.split()
    return strings

def getFiles() :
# Mereturn semua kalimat pada semua file .txt yang ada di directory files dalam bentuk array
    lines = []
    namaFile = []
    os.chdir('../test')
    for file in os.listdir('../test') :
        if file.endswith(".txt") :
            f = open(file, "r", encoding="utf8")
            strings = ""
            for line in f.readlines() :
                strings = strings + line
                strings = strings + " "
            strings = strings.replace('\n','')

            lines.append(strings)
            namaFile.append(file)

            f.close()
    os.chdir('../src')

    return namaFile, lines

def getKamusData(query) :
#Membuat kamus data berdasarkan file dan query
    buang, kalimat = getFiles()
    concatKalimat = ""
    for i in kalimat :
        concatKalimat = concatKalimat + i + " "

    concatKalimat = lowStemStopSplit(concatKalimat)
    query = lowStemStopSplit(query)

    for i in concatKalimat :
        query.append(i)

    kamusData = []
    for i in query :
        Found = False
        for j in kamusData :
            if i == j :
                Found = True
                break

        if Found == False :
            kamusData.append(i)

    return kamusData

def getFileSum(kalimatFile):
    sum = []
    for kalimat in kalimatFile:
        count = kalimat.split()
        sum.append(len(count))
    return sum

def countTerm(kalimat, query) :
# Mereturn sebuah list dengan perhitungan kemunculan kata setelah dilowcase, distem, dan stopwords dihilangkan
    kamusData = getKamusData(query)
    perhitunganKata = []
    kalimat = lowStemStopSplit(kalimat)
    for i in kamusData :
        kata = [i]
        count = 0
        for j in kalimat :
            if i == j :
                count = count + 1
        kata.append(count)
        perhitunganKata.append(kata)

    return perhitunganKata

def getFileTerms(kalimatFile, query) :
#Mereturn terms dari semua file dalam bentuk array
    fileTerms = []
    for i in kalimatFile :
        fileTerms.append(countTerm(i, query))

    return fileTerms

def getSimilarity(QTerms, DTerms) :
#Mereturn nilai similarity dari terms query dan terms satu dokumen
    Dot = 0
    QLength = 0
    DLength = 0
    for i in range(len(QTerms)) :
        Dot = Dot + QTerms[i][1] * DTerms[i][1]

    for i in range(len(QTerms)) :
        QLength = QLength + (QTerms[i][1] ** 2)
    QLength = QLength ** 0.5

    for i in range(len(DTerms)) :
        DLength = DLength + (DTerms[i][1] ** 2)
    DLength = DLength ** 0.5

    Sim = Dot/(QLength * DLength)

    return Sim

def getAllSim(queryTerms, fileTerms) :
#Mereturn nilai similarity dari terms query dan terms semua dokumen
    simArray = []
    for i in range(len(fileTerms)) :
        simArray.append(getSimilarity(queryTerms, fileTerms[i]))

    return simArray

def getTableValue(queryTerms, fileTerms) :
    printTable = []
    for j in range(len(queryTerms)):
        if (queryTerms[j][1] >= 1):
            printTerms = []
            printTerms.append(queryTerms[j][0])
            printTerms.append(queryTerms[j][1])
            for i in range(len(fileTerms)):
                printTerms.append(fileTerms[i][j][1])
            printTable.append(printTerms)

    return printTable

def getKalimatPertama(kalimatFile) :
    kalimatPertamaFile = []
    for i in kalimatFile :
        kalimatPertamaFile.append(i.split('.')[0])
    return kalimatPertamaFile
