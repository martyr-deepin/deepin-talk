import QtQuick 2.1
import "../Widgets" as Widgets
import DTalk 1.0

Item {
    id: container

    property string type
    property string message
    property int padding: 8
    property real maxWidth: 0
    width: textArea.width + padding * 3
    height: textArea.height + padding * 2

    BorderImage {
        id: background
        anchors.fill: parent
        source: container.type == "received" ? "qrc:/images/chat/received.png" : "qrc:/images/chat/sended.png"
		horizontalTileMode: BorderImage.Stretch	
		verticalTileMode: BorderImage.Stretch
		border { left: 18;  right: 18; top: 27; bottom: 18}		

        
        Item {
            anchors.leftMargin: container.type == "received" ? padding * 2 : padding
            anchors.rightMargin: container.type == "received" ? padding : padding * 2
            anchors.topMargin: padding
            anchors.bottomMargin: padding
            anchors.fill: parent

            Widgets.LayoutTextArea {
                id: textArea
                anchors.left: parent.left
                anchors.top: parent.top
                minHeight: 43 - padding * 2
                minWidth: 80 - padding * 3
                maxWidth: container.maxWidth
                color: container.type == "received" ? Qt.rgba(0.9, 0.9, 0.9, 1.0) : Qt.rgba(82/255.0, 52/255.0, 165/255.0, 0.9)
                wrapMode: Text.Wrap
                /* verticalAlignment: Text.AlignVCenter */
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