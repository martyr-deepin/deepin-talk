import QtQuick 2.1
import "../Widgets"
import DTalk 1.0

DTextArea {
    id: messageBox
    /* textFormat: TextEdit.RichText */
    property int tempType: 0
    focus: true
    /* canPaste: false */
    selectByMouse: true
    selectByKeyboard: true
    property alias control: messageControl

    DMessage {
        id: messageControl
        document: messageBox.textDocument
        anchors.fill: parent
    }

    Keys.onPressed: {
        if ((event.key == Qt.Key_V) && (event.modifiers & Qt.ControlModifier)) {
            messageControl.insertFromClipboard()
            event.accepted = true
        }
    }
    
    Keys.onReturnPressed: {
        if (event.modifiers & Qt.ControlModifier) {
            messageControl.insertHtml("<br>")
            
        } else {
            if (messageBox.text != "") {
                messageModel.postMessage(messageBox.text)
                messageBox.text = ""
                event.accepted = true
            }
        }
    }


    Rectangle {
        anchors.top: parent.top;
        width: parent.width; height: 1
        color: Qt.rgba(0.3, 0.3, 0.3, 0.6)
    }

    Rectangle {
        anchors.fill: parent
        color: Qt.rgba(0.9, 0.9, 0.9, 0.5)
        radius: 5
        z: -100
    }
}
