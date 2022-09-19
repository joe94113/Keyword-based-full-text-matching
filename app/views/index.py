from flask import render_template
from flask import request
import pandas as pd
import json
import re
from app.methods.porterStemmer import PorterStemmer

class Views:
    def index():
        search = request.args.get('search')
        jsonFile = Views.getJsonData()
        xmlFile = Views.getXmlData()
        jsonData = [];
        xmlData = [];
        jsonLog = {
            'word': 0,
            'sentence': 0,
        }
        xmlLog = {
            'word': 0,
            'sentence': 0,
        }
        # print(xmlData)
        if(search):
            search = search.strip()
            checkInJson = False
            checkInXml = False
            # data = [x for x in data if search in x['text']]
            for d in jsonFile:
                sentences = Views.textToSentence(d['text'])
                # Find and replace string values in list
                strs = []
                for sentence in sentences:
                    originalText = [x.replace(' ', '') for x in sentence.split(' ')]
                    text = [x.strip().replace(' ', '').rstrip('.') for x in sentence.split(' ')]
                    # print(text)
                    checkInSentence = False
                    sentenceIndex = 0
                    for ids, w in enumerate(text):
                        sentenceIndex += 1
                        check = Views.checkWordMatch(search, w)
                        if check:
                            checkInJson = True
                            checkInSentence = True
                            jsonLog['word'] += 1
                            strs.append('<span style="color: red">' + originalText[ids] + '</span>')
                        else:
                            if ids == len(text) - 1 and originalText[ids].endswith('.') == False:
                                # print(originalText[ids])
                                strs.append(originalText[ids] + '.')
                            else:
                                strs.append(originalText[ids])
                    if checkInSentence:
                        jsonLog['sentence'] += 1
                        # use span to border the sentence
                        # print(f'strsLen: {len(strs)}, count: {sentenceIndex}, strs: {strs}')
                        strs.append('</span>')
                        strs.insert(len(strs) - sentenceIndex - 1, '<span class="border border-danger">')
                        checkInSentence = False
                    # print(strs)
                    # print(strs)
                if checkInJson:
                    d['text'] = strs
                    d['text'] = " ".join(str(x) for x in d['text'])
                    jsonData.append(d)
                    checkInJson = False

            for d in xmlFile:
                sentences = Views.textToSentence(d['description'])
                # print(sentences)
                for sentence in sentences:
                    originalText = [x.replace(' ', '') for x in sentence.split(' ')]
                    text = [x.strip().replace(' ', '').rstrip('.') for x in sentence.split(' ')]
                    print(sentence)
                    checkInSentence = False
                    sentenceIndex = 0
                    for ids, w in enumerate(text):
                        sentenceIndex += 1
                        check = Views.checkWordMatch(search, w)
                        if check:
                            checkInXml = True
                            checkInSentence = True
                            xmlLog['word'] += 1
                            strs.append('<span style="color: red">' + originalText[ids] + '</span>')
                        else:
                            if ids == len(text) - 1 and originalText[ids].endswith('.') == False:
                                # print(originalText[ids])
                                strs.append(originalText[ids] + '.')
                            else:
                                strs.append(originalText[ids])
                    if checkInSentence:
                        xmlLog['sentence'] += 1
                        # print(f'strsLen: {len(strs)}, count: {sentenceIndex}, strs: {strs}')
                        strs.append('</span>')
                        strs.insert(len(strs) - sentenceIndex - 1, '<span class="border border-danger">')
                        checkInSentence = False
                if checkInXml:
                    d['description'] = strs
                    d['description'] = " ".join(str(x) for x in d['description'])
                    xmlData.append(d)
                    checkInXml = False
        else:
            jsonData = Views.getJsonData()
            xmlData = Views.getXmlData()
        return render_template('index.html', jsonData=jsonData, jsonLog=jsonLog, xmlData=xmlData, xmlLog=xmlLog, search=search)

    def getJsonData():
        with open("./app/public/file/data.json", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def getXmlData():
        df = pd.read_xml("./app/public/file/data.xml")
        dfJson = df.to_json(orient="records")
        data = json.loads(dfJson)
        return data
    
    def checkWordMatch(search, text):
        p = PorterStemmer();
        search = p.stem(search.lower(), 0, len(search)-1)
        text = p.stem(text.lower(), 0, len(text)-1)
        # print(search, text)
        if search == text:
            return True
        else:
            return False

    def textToSentence(text):
        non_fragments = re.compile(r'$|\d+($|:\d+.*\d+.*$)')
        full_text = "".join([line for line in text if not non_fragments.match(line)])
        sentences = full_text.split('. ')
        return sentences