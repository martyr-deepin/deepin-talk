import QtQuick 2.0
import QtGraphicalEffects 1.0

Item {
	width: 306 + sideWidth * 2; height: 750	+ sideWidth * 2
    property color blurColor: Qt.rgba(0, 0, 0, 0.3)
    property color borderColor: Qt.rgba(255, 255, 255, 0.33)
	property color blackBorderColor: Qt.rgba(30/255.0, 30/255.0, 30/255.0, 0.6)
	property real blurWidth: 10
	property real rectRadius: 5
	property real sideWidth: blurWidth + rectRadius
	property rect vaildRect: Qt.rect(sideWidth, sideWidth, width - sideWidth * 2, height - sideWidth * 2)
	
    RectangularGlow {
        id: effect
        anchors.fill: rect
        glowRadius: blurWidth
        spread: 0.2
        color: blurColor
        cornerRadius: rect.radius + glowRadius
    }
	
	ResizeArea {
		anchors.fill: parent
		window: windowView
		frame: rect
	}

    Rectangle {
        id: rect
		x: sideWidth; y: sideWidth
        width: Math.round(parent.width - sideWidth * 2 )
        height: Math.round(parent.height - sideWidth * 2)
        radius: rectRadius		
		anchors.centerIn: parent		
		antialiasing: true
		color: "transparent"
		smooth: true
		
		
		Rectangle {
			id: backgound
			
			Image {
				anchors.fill: parent
				source: "../images/bg.png"
			}
			
			/* Rectangle { */
			/* 	anchors.fill: parent */
			/* 	color: Qt.rgba(0.9, 0.9, 0.9, 0.2) */
			/* } */
						
			anchors.fill: parent
			color: "transparent"
			antialiasing: true
			smooth: true
			
			Rectangle {
				border { width: 1; color: blackBorderColor }
				anchors.fill: parent
				color: "transparent"
				radius: rectRadius
			}
			
			Rectangle {
				id: innerRect
				anchors.margins: 1
				border { width: 1; color: borderColor }
				anchors.fill: parent
				color: "transparent"
				radius: rectRadius
			}
		}
		
		RoundItem {
			target: backgound
			radius: rectRadius
		}
    }
}
