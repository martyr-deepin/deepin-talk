import QtQuick 2.1

Item {
	id:container
	property string type
	property string content
	height: messageBubble.height 
	
	Bubble {
		id: messageBubble
		message: container.content
		anchors.left: container.type == "received" ? personInfo.right : container.left
		width: 250
		y: 10
        type: container.type
	}
		
	Rectangle {
		id: personInfo
		y: 10
		width: 60
		anchors.left: container.type == "received" ? container.left : messageBubble.right
		anchors.leftMargin: container.type == "received" ? 0 : 10
		Column {
			Image { 
				source: "images/person.png"; smooth: true; 
				anchors.horizontalCenter: parent.horizontalCenter
				width: 50; height: 50
				}
		}
			
	}

}