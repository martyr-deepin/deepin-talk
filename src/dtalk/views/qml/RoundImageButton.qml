import QtQuick 2.1
import QtGraphicalEffects 1.0

Item {
	id: container
	
	property alias source: image.source
	property real radius: width/2
	property real borderWidth: 3
	signal clicked
	width: 80; height: 80
	
	RoundImage {
		id: image
		width: parent.width
		height: parent.height
		radius: parent.width/2
	}
		
    Rectangle {
		id: roundBorder
		anchors.fill: parent
		border { width: borderWidth; color: "#ebeef3"}
		color: "transparent"
		radius: container.width/2
		antialiasing: true
		smooth: true
	}
	
	states: [
		State {
			name: "hovered"
			PropertyChanges { target: roundBorder ; border.color: "#46a6f1" }
		}
	]
	
	transitions: Transition {
		ColorAnimation { target: roundBorder; duration: 300 }
	}
	
	MouseArea {
		id: mouseArea
		anchors.fill: parent
		hoverEnabled: true
		onEntered: container.state = "hovered"
		onExited: container.state = ""
		onReleased: { container.state = mouseArea.containsMouse ? "hovered" : ""}
		onClicked: container.clicked()
	}
	
}