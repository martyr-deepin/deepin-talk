import QtQuick 2.1
import QtQuick.Dialogs 1.0
import QtGraphicalEffects 1.0

import "../scripts/common.js" as Common
import "../Widgets"
import DTalk 1.0

Item {
    id: root
    anchors.fill: parent

    LinearGradient {
        id: linearBack
        y: -Common.titlebarHeight
        width: parent.width; height: 136
        start: Qt.point(0, 0)
        end: Qt.point(parent.width, 0)
        gradient: Gradient {
            GradientStop { position: 0.0; color: Qt.rgba(0.9, 0.9, 0.9, 0.6)}
            GradientStop { position: 0.3; color: Qt.rgba(0.9, 0.9, 0.9, 0.5)}
            GradientStop { position: 0.6; color: Qt.rgba(0.9, 0.9, 0.9, 0.2)}
            GradientStop { position: 1.0; color: Qt.rgba(0.9, 0.9, 0.9, 0.0)}
        }
    }
    
    Rectangle {
        id: sepeator
        width: parent.width; height: 1
        color: Qt.rgba(0.9, 0.9, 0.9, 0.9)
        anchors.top: linearBack.bottom
    }

    Headerbar { id: headerBar; width: parent.width; z: 100 }

    ScrollWidget {
        id: messageScrollArea
        width: parent.width
        anchors.top: sepeator.bottom
        anchors.bottom: messageToolbar.top
        ListView {
            id: messageView
            anchors.fill: parent
            delegate: MessageDelegate { id: messageDelegate }
            model: messageModel
            interactive: false
            clip: true
        }
    }

    Row {
        id: messageToolbar
        anchors.bottom: messageInput.top
        anchors.bottomMargin: 5
        x: parent.x + 5
        spacing: 5
        
        DButton {
            source: "qrc:/images/chat/file.png"
            anchors.verticalCenter: parent.verticalCenter
        }            
        
        DButton {
            source: "qrc:/images/chat/image.png"
            anchors.verticalCenter: parent.verticalCenter
            onClicked: imageFileDialog.open()
            
            FileDialog {
                id: imageFileDialog
                nameFilters: [ "Image files (*.jpg *.png)", "All files (*)" ]
                onAccepted: {
                    messageInput.control.insertImage(imageFileDialog.fileUrl)
                }
            }
        }            
        
        DButton {
            source: "qrc:/images/chat/shot.png"
            anchors.verticalCenter: parent.verticalCenter
        }            
    }
    
    MessageInput {
        id: messageInput
        anchors.bottom: parent.bottom
        width: parent.width; height: 120
    }
    
}
