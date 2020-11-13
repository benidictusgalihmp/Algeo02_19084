#install Sastrawi dulu

import os
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
    os.chdir('files')
    list_of_files = os.listdir()

    lines=[]
    for file in list_of_files :
        if file.endswith(".txt") :
            f = open(file, "r")
            strings = ""
            for line in f.readlines() :
                strings = strings + line
                strings = strings + " "
            strings = strings.replace('\n','')
            lines.append(strings)
            f.close()
    os.chdir('../')

    return list_of_files, lines

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

#Testing

#testQuery = query untuk testing
testQuery = "Membuat tenda menyebabkan saya sangat lelah"
queryTerms = countTerm(testQuery, testQuery)

#namaFile = list nama file
#kalimatFile = list semua kalimat pada setiap file
namaFile, kalimatFile = getFiles()

#fileTerms = perhitungan term pada kalimatFile 
fileTerms = getFileTerms(kalimatFile, testQuery)

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


for i in range(len(sim)) :
    #namanya isi link
    print(str(i+1) + ". " + namaFile[i])
    print("Tingkat kesamaan: " + str(sim[i]))
    print(kalimatFile[i].split('.')[0] + "...")
    print() 
###

