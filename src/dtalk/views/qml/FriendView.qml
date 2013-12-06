import QtQuick 2.1
import "js/roster.js" as Roster

ListView {
	delegate: friendsDelegate
	clip: true
    
    
	property Component friendsDelegate: Component {
		Item {
			id: wrapper
			width: wrapper.ListView.view.width; height: 58

			
			Row {
				anchors.fill: parent
				spacing: 40
				anchors.margins: 40				
				
				RoundImageButton {
					id: faceImage
					width: 40; height: 40
					anchors.verticalCenter: parent.verticalCenter
					source: model.instance.avatar
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
						text: Roster.getDisplayName(model.instance)
					}
					
				}
			}
		}
		
	}
}