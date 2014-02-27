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
		
		Row {
			anchors.fill: parent
			spacing: 40
			anchors.margins: 40				
            
			Widgets.RoundImageButton {
				id: faceImage
				width: 40; height: 40
				anchors.verticalCenter: parent.verticalCenter
				source: instance.avatar
			}
			
			Rectangle {
				width: username.contentWidth + radius * 2
				height: username.contentHeight + 2
				color: Qt.rgba(61/255.0, 65/255.0, 100/255.0, 0.6)
				anchors.verticalCenter: parent.verticalCenter
				radius: height / 2
				
				Text {
					id: username
					anchors.centerIn: parent
					color: "#fff"
					font.pixelSize: 12
                    text: instance.displayName
				}
				
			}
		}
	}
	
}
