import QtQuick 2.1
import "../Widgets"

Component {
    Item {
        id: wrapper
        width: wrapper.ListView.view.width
        height: wrapper.ListView.view.itemHeight
        
        /* SelectEffect { */
        /*     id: selectEffect */
        /*     anchors.fill: parent */
        /*     visible: true */
        /* } */
        Rectangle {
            id: selectEffect
            radius: 3
            color: Qt.rgba(255 / 255, 192 / 255, 0 / 255, 0.3)
            width: parent.width
            height: parent.height - 6
            anchors.verticalCenter: parent.verticalCenter
            visible: false
        }
        
        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: { selectEffect.visible = true; print("enter") }
            onExited: { selectEffect.visible = false }
            onClicked: {
                wrapper.ListView.view.model.onClicked(index)
            }
            
        }
        
        Rectangle {
            id: iconImage            
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter            
            width: 18; height: 18
            radius: width / 2
            color: "transparent"
            border { width: 2; color: "#fff" }
            
            RoundImage {
                anchors.centerIn: parent
                source: instance.image
                width: 16; height: 16
            }
            
        }
        
        Text {
            id: titleText
            anchors.left: iconImage.right
            anchors.right: totalText.left
            anchors.rightMargin: 5
            anchors.leftMargin: 5
            anchors.verticalCenter: parent.verticalCenter
            text: instance.title
            color: "#ffffff"
            font.pixelSize: 14
			elide: Text.ElideRight
        }
        
        Text {
            id: totalText
            anchors.right: parent.right
            anchors.rightMargin: 10
            text: "(" + instance.total + ")"            
            anchors.verticalCenter: parent.verticalCenter
            font.pixelSize: 14
            color: Qt.rgba(1, 1, 1, 0.4)
        }
    }
}