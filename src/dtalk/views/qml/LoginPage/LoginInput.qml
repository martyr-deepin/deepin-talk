import QtQuick 2.1
import "../Widgets"

ShadowPanel {
	width: 260; height: 42
	property alias leftImage: leftImg.source
	property alias rightImage: rightImg.source
	property alias echoMode: input.echoMode
    property alias text: input.text
	
	Row {
		anchors.margins: 10
		anchors.fill: parent
		spacing: 5						
		
		Image {
			id: leftImg
			source: "../images/person.png"
			anchors.verticalCenter: parent.verticalCenter
		}
		
		TextInputShadow {
			id: input
			width: 190; 
			anchors.verticalCenter: parent.verticalCenter
			verticalAlignment: Qt.AlignCenter
			clip: true
		}
		
		Image {
			id: rightImg
			source: "../images/arrow.png"
			anchors.verticalCenter: parent.verticalCenter
		}
		
	}
	
}
