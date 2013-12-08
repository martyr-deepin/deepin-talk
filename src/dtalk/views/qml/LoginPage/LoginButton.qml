import QtQuick 2.1
import "../Widgets"

Item {
	id: container
	signal clicked
	width: img.width; height: img.height
    property alias isLogging: busyIndicator.on
    
	
	Image {
		id: img
		anchors.centerIn: parent
		source: "../images/login.png"
		opacity: 0.5
		antialiasing: true
		smooth: true
		visible: !busyIndicator.on
	}
	
	BusyIndicator {
		anchors.centerIn: parent
		id: busyIndicator
	}
	
	states: [
		State {
			name: "hovered"
			PropertyChanges { target: img ; opacity: 1.0 }
		}
	]
	
	transitions: Transition {
		NumberAnimation { properties: "opacity"; duration: 300 }
	}
	
	MouseArea {
		id: mouseArea
		anchors.fill: img
		hoverEnabled: true
		onEntered: container.state = "hovered"
		onExited: container.state = ""
		onReleased: { container.state = mouseArea.containsMouse ? "hovered" : ""}
		onClicked: {
			container.clicked()
		}
	}
}