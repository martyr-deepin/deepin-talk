import QtQuick 2.1
import "../Widgets" as Widgets

Widgets.ShadowPanel {
	width: 260; height: 42
	property alias leftImage: leftImg.source
	property alias rightImage: rightImg.source
	property alias echoMode: input.echoMode
    property alias text: input.text
    property alias length: input.length
    property var textInput: input
    property alias inputFocus: input.focus
    signal returnPressed
    signal rightButtonClicked
	
	Row {
		anchors.margins: 10
		anchors.fill: parent
		spacing: 5						
		
		Image {
			id: leftImg
			source: "qrc:/images/common/person.png"
			anchors.verticalCenter: parent.verticalCenter
		}
		
		Widgets.DTextField {
			id: input
			width: 190; 
			anchors.verticalCenter: parent.verticalCenter
			verticalAlignment: Qt.AlignCenter
			clip: true
            focus: true
            Keys.onReturnPressed: returnPressed()
            font.pixelSize: 14
		}
		
		Widgets.DButton {
			id: rightImg
			source: "qrc:/images/common/arrow.png"
			anchors.verticalCenter: parent.verticalCenter
            onClicked: rightButtonClicked()
		}
		
	}
	
}
