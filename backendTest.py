#install Sastrawi dulu

import os
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopword = StopWordRemoverFactory().create_stop_word_remover()

def lowStemStop(strings) :
# Mereturn strings yang sudah dilowercase, distem, dan dihilangkan stopwordsnya
    strings = strings.lower()
    strings = stemmer.stem(strings)
    strings = stopword.remove(strings)
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

def countTerm(kalimat) :
# Mereturn sebuah list dengan perhitungan kemunculan kata setelah dilowcase, distem, dan stopwords dihilangkan
    perhitunganKata = []
    kalimat = lowStemStop(kalimat)
    kalimat = kalimat.split()
    for i in kalimat :
        kata = []
        found = False
        for j in perhitunganKata :
            if i == j[0] :
                found = True
        
        if found == False :
            count = 0
            for k in kalimat :
                if i == k :
                    count = count + 1
            kata.append(i)
            kata.append(count)
            perhitunganKata.append(kata)
    
    return perhitunganKata

#Testing

#namaFile = list nama file
#kalimatFile = list semua kalimat pada setiap file
namaFile, kalimatFile = getFiles()

#fileTerms = perhitungan term pada kalimatFile 
fileTerms = []
for i in kalimatFile :
    fileTerms.append(countTerm(i))

#testQuery = query untuk testing
testQuery = "Apakah saya seorang paman?"
testQuery = countTerm(testQuery)

print(namaFile)
print(kalimatFile)
print(fileTerms)
print(testQuery)

#print kalimat pertama file a
print(kalimatFile[0].split('.')[0])