import QtQuick 2.1


Item {
	id: root
	property alias text: name.text
	property alias source: face.source
	property real spacing: 20
	height: spacing + face.width + name.width
	property real faceWidth: 110
	property real faceHeight: 110
	
	Column {
		anchors.centerIn: parent		
		spacing: root.spacing
		
		RoundImageButton {
			id: face
			source: "image/face.jpg"
			width: faceWidth; height: faceHeight
			borderWidth: 4
			radius: width/2
			anchors.horizontalCenter: parent.horizontalCenter
		}
				
		Text {
			id: name
			anchors.horizontalCenter: parent.horizontalCenter
			color: "#fff"
			text: "小邪兽"
			font.pixelSize: 22
		}
		
	}
}