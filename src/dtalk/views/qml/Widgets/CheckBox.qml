import QtQuick 2.1

Item {
    id: root
	width: box.width + rowSpacing + label.contentWidth
	height: 30
	property real rowSpacing: 5
	property alias text: label.text
    property alias checked: check.visible
	signal clicked (bool status)
	
		
	Row {
		anchors.fill: parent
		spacing: rowSpacing
		ShadowPanel {
			id: box
			anchors.verticalCenter: parent.verticalCenter
			width: 18; height: 18
			
			Image {
				id: check
				anchors.centerIn: parent
				anchors.horizontalCenterOffset: 2
				source: "qrc:/images/common/check.png"
			}
		}
		
		DText {
			id: label
			anchors.verticalCenter: parent.verticalCenter
		}
	}
	
	MouseArea {
		anchors.fill: parent
		hoverEnabled: true
		onClicked: {
			check.visible = !check.visible
			root.clicked(check.visible)
		}
	}
}