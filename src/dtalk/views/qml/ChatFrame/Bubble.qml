import QtQuick 2.1
import "../Widgets"
import DTalk 1.0

Item {
    id: container

    property string type
    property string message
    property int padding: 50
    property real maxWidth: 0
    width: message.paintedWidth + background.widthMargin
    height: message.paintedHeight + background.heightMargin

    SimpleCorner {
        id: background
        anchors.fill: parent
        fillColor: container.type == "received" ? Qt.rgba(82/255.0, 52/255.0, 165/255.0, 0.9) : Qt.rgba(1.0, 1.0, 1.0, 1.0)
        cornerDirection:  container.type == "received" ? Qt.LeftEdge : Qt.RightEdge
        shadowDirection: container.type == "received" ? "left" : "right"
        borderMargin: 10

        Item {
            anchors.fill: parent

            LayoutTextArea {
                id: message
                anchors.left: parent.left
                anchors.top: parent.top
                maxWidth: container.maxWidth
                color: container.type == "received" ? Qt.rgba(0.9, 0.9, 0.9, 1.0) : Qt.rgba(82/255.0, 52/255.0, 165/255.0, 0.9)
                wrapMode: Text.Wrap
                textFormat: Text.RichText
                selectByMouse: true
                selectByKeyboard: true
                readOnly: true
                text: container.message
                focus: true
                
                DMessage {
                    id: messageControl
                    document: parent.hackDocument
                    anchors.fill: parent
                }
                
            }
        }

    }

}