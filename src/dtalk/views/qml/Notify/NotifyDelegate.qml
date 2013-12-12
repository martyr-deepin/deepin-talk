import QtQuick 2.1

Component {
    Item {
        id: wrapper
        width: wrapper.ListView.view.width
        height: 18
                
        Image {
            id: iconImage
            anchors.left: parent.left
            anchors.verticalCenter: parent.verticalCenter            
            source: instance.image
            width: 16; height: 16
        }
        
        Text {
            id: titleText
            anchors.left: iconImage.right
            anchors.leftMargin: 5
            anchors.verticalCenter: parent.verticalCenter
            text: instance.title
            color: "#ffffff"
        }
        
        Text {
            id: totalText
            anchors.right: parent.right
            anchors.rightMargin: 5
            text: "(" + instance.total + ")"            
            anchors.verticalCenter: parent.verticalCenter
            color: "#ffffff"
        }
    }
}