import QtQuick 2.1
import "../Widgets" as Widgets


Component {
    Item {
        id: wrapper
        width: wrapper.ListView.view.width; height: 58
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                wrapper.ListView.view.model.doClicked(index)
            }
        }
        
        
        Item {
            id: container
            anchors.fill: parent
            property real margins: 10
            
            Widgets.RoundImageButton {
                id: faceImage
                width: 40; height: 40
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: parent.margins
                source: instance.avatar
            }
            
			Rectangle {
                anchors.left: faceImage.right
                anchors.leftMargin: 10
                width: username.width + 10
				height: username.contentHeight + 2
				color: Qt.rgba(61/255.0, 65/255.0, 100/255.0, 0.6)
				anchors.verticalCenter: parent.verticalCenter
				radius: height / 2
				
				Widgets.LayoutText {
					id: username
					color: "#fff"
					font.pixelSize: 12
                    text: instance.displayName
                    maxWidth: container.width - faceImage.width - container.margins * 3
                    anchors.centerIn: parent
				}
            
            }
				
		}
        
    }
    
}