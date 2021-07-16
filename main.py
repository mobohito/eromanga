import os
import sys
import untitled

sys.setrecursionlimit(10000)

import urllib.request
import urllib3

import requests
import ssl

import lxml
from bs4 import *

from PyQt5 import (QtCore,
                   QtGui,
                   QtWidgets,
                   )

from PyQt5.QtWidgets import (QVBoxLayout,
                             QHBoxLayout,
                             QPushButton,
                             QGridLayout,
                             QLabel,
                             QMainWindow,
                             QScrollArea,
                             QRadioButton,
                             QFrame,
                             QCheckBox,
                             QDialog,
                             QListWidget,
                             QListWidgetItem,
                             QWidget,
                             QFileDialog,
                             )
from PyQt5.QtGui import (QPainter,
                         QPalette,
                         QPixmap,
                         QImage,

                         )

from PyQt5.QtCore import (QObject,
                          pyqtSignal,
                          pyqtSlot,
                          QSize,
                          Qt,
                          QUrl,
                          QDir,
                          QFile,
                          QIODevice,
                          )

from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEnginePage)

from PyQt5.QtNetwork import (QNetworkAccessManager, QNetworkRequest)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QMainWindow()
ui = untitled.Ui_MainWindow()
ui.setupUi(MainWindow)

DownloadList = {}


class ListItems():

    def __init__(self, url1):

        if (str(type(url1)) == "<class 'NoneType'>"):
            return

        try:
            item = QListWidgetItem()
            item.setSizeHint(QSize(10, 300))
            ui.listWidget.addItem(item)

            widget = QWidget()

            layout = QHBoxLayout()
            widget.setLayout(layout)

            chk = QCheckBox(widget)
            name = ha.addItem(url1)[0]
            chk.setText(name)
            layout.addWidget(chk)

            res = requests.get(ha.addItem(url1)[1])
            img = QImage.fromData(res.content)

            def calculateRes():
                Magnification = 300 / img.height()
                correctWeight = Magnification * img.width()
                return int(correctWeight), int(300)

            scaledimage = img.scaled(calculateRes()[0], calculateRes()[1])

            label = QLabel(widget)
            label.setPixmap(QPixmap.fromImage(scaledimage))
            label.setAutoFillBackground(True)
            label.resize(calculateRes()[0], calculateRes()[1])

            layout.addWidget(label)

            ui.listWidget.setItemWidget(item, widget)

            def addtoDownloadList_SLOT():

                if (chk.isChecked()):
                    add = {name: url1}
                    DownloadList.update(add)

                elif ((not chk.isChecked()) and (name in DownloadList)):
                    del [DownloadList[name]]


            chk.clicked.connect(lambda void: addtoDownloadList_SLOT())
        except:
            pass


class Warning():
    def __init__(self, warn):
        qdialog = QDialog(ui.centralwidget)
        qdialog.resize(400, 300)

        warning = QLabel(qdialog)
        warning.setText(warn)

        butt = QPushButton(qdialog)
        butt.setText("哦")

        grid = QGridLayout()
        qdialog.setLayout(grid)

        grid.addWidget(warning)
        grid.addWidget(butt)

        butt.clicked.connect(lambda void:
                             qdialog.close())

        qdialog.activateWindow()
        qdialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        qdialog.show()

class htmlAnalysis():
    ssl._create_default_https_context = ssl._create_unverified_context
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) '
                      'Gecko/20100101 Firefox/23.0'}
    def __init__(self):
        pass

    def addItem(self, url):
        try:
            response = requests.get(url)
            if (response.status_code != 200):
                Warning("连接出错")
            req = urllib.request.Request(url, headers=self.headers)

            data = urllib.request.urlopen(req).read().decode('utf-8')

            soup = BeautifulSoup(data, 'lxml')
            Souptitle = soup.findAll(name='div', attrs={"class": "heading"}, limit=2)
            titile = str(Souptitle).removeprefix('[<div'). \
                removeprefix(' '). \
                removeprefix('class="heading">'). \
                removeprefix('\n'). \
                removeprefix('<h3>'). \
                removesuffix('</div>]'). \
                removesuffix('\n'). \
                removesuffix('\n'). \
                removesuffix('</h3>')

            req1 = urllib.request.Request((url + '/1/'), headers=self.headers)
            data1 = urllib.request.urlopen(req1).read().decode('utf-8')
            soup1 = BeautifulSoup(data1, 'lxml')

            SoupImage = str(soup1.findAll(name='img', attrs={"class": "img-responsive"}))

            start = SoupImage.find("src") + 5
            end = SoupImage[start:].find('\"')
            url = SoupImage[start:]
            url = url[:end]
            url = "http://twhentai.com" + url

            return (titile, url)
        except:
            pass

    def allPictureAddr(self, url):
        imageUrlList = []
        i = 1
        url = url
        while (True):
            TempUrl = url
            if (len(url) - url.rindex("/") == 1):
                TempUrl = url + str(i) + "/"

            else:
                TempUrl = url + "/" + str(i) + "/"
            req = urllib.request.Request(TempUrl, headers=self.headers)
            data = urllib.request.urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(data, 'lxml')
            SoupImage = str(soup.findAll(name='img', attrs={"class": "img-responsive"}))

            start = SoupImage.find("src") + 5
            end = SoupImage[start:].find('\"')
            imgurl = SoupImage[start:]
            imgurl = imgurl[:end]
            imgurl = "http://twhentai.com" + imgurl
            if (imgurl in imageUrlList):
                break
            else:
                imageUrlList.append(imgurl)
                i = i+1
        return imageUrlList

class DownloadCore():
    def __init__(self, url, path, num):
        try:
            file = path + "/" +str(num) + ".jpg"
            req = requests.get(url)
            with open(file, "wb") as f:
                f.write(req.content)
        except:
            pass


def addFromUrl():
    if len(ui.UrlLineEdit.text()) != 0 :
        url = ui.UrlLineEdit.text()
        ListItems(url)


def changePathButton_onClicked_SLOT():
    dialog = QFileDialog.getExistingDirectoryUrl(ui.centralwidget, 'Open file')
    print(dialog.path())
    ui.PathEdit.setText(dialog.path())

def startDownloadButton_onClicked_SLOT():
    print("Starting Download")
    for i in DownloadList:
        print(i, DownloadList[i])
        name = i
        url = DownloadList[i]
        path = ui.PathEdit.text() + "/" + name

        dir = QDir()
        dir.setPath(path)
        if not dir.exists():
            dir.mkdir(path)
        downloadList = ha.allPictureAddr(url)
        for i in range(len(downloadList)):
            print(downloadList[i])
            DownloadCore(downloadList[i],path, i)



    Warning("下载完成！")


def searchButton_onClicked_SLOT():
    url = "http://twhentai.com/search/" + ui.SearcgLineEdit.text() + "/"
    print(url)
    view.setUrl(QUrl(url))
    view.resize(1024, 768)
    view.show()

    def urlChanged_SLOT():
        newUrl = view.url()
        if (view.url().url().find("search") == -1):
            view.back()
        if (len(view.url().url()[:len(view.url().url()) - 1]) -
                (view.url().url()[:len(view.url().url()) - 1]).rindex("/")
                == 6):
            ListItems(view.url().url())

    view.urlChanged.connect(urlChanged_SLOT)

#ListItems('http://twhentai.com/hentai_doujin/19289/1/')

path = os.getcwd()
ui.PathEdit.setText(path)

result = requests.get("http://twhentai.com")
print(result.status_code)
if (result.status_code !=200):
    Warning("网络连接错误！")

ha = htmlAnalysis()
view = QWebEngineView()
view.load(QUrl(""))
view.hide()
print(len(DownloadList))
ui.StartDownloadButton.clicked.connect(startDownloadButton_onClicked_SLOT)
ui.SearchButton.clicked.connect(searchButton_onClicked_SLOT)
ui.changePathButton.clicked.connect(changePathButton_onClicked_SLOT)
ui.AddButton.clicked.connect(addFromUrl)

MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
MainWindow.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
MainWindow.show()

sys.exit(app.exec_())
