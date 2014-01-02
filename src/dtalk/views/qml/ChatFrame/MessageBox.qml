import QtQuick 2.1
import "../Widgets"
import QtGraphicalEffects 1.0

Item {
	id:container
    property var messageObj
	height: Math.max(messageBubble.height, personInfo.height)
    property real messageWidth: messageBubble.width + personInfo.width
	
	Bubble {
		id: messageBubble
		message: messageObj.body
		anchors.left: messageObj.type == "received" ? personInfo.right : container.left
        maxWidth: parent.width * 0.66
		y: 10
        type: messageObj.type
	}
		
	Item {
		id: personInfo
		y: 10
		width: 60; height: 50 + 15
		anchors.left: messageObj.type == "received" ? container.left : messageBubble.right
		anchors.leftMargin: messageObj.type == "received" ? 0 : 10
		Column {
            spacing: 5
            
			RoundImageButton { 
				source: "qrc:/images/common/face.jpg"; smooth: true; 
				anchors.horizontalCenter: parent.horizontalCenter
				width: 50; height: 50
				}
            
            TextShadow {
                text: messageObj.created
                font.pixelSize: 10
				anchors.horizontalCenter: parent.horizontalCenter
                
            }
		}
			
	}

}