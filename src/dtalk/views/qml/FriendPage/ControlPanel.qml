import QtQuick 2.1

Item {
	height: 38

	Rectangle {
		width: parent.width; height: 1
		anchors.top: parent.top
		color: Qt.rgba(0.1, 0.1, 0.1, 0.2)
	}
	
	Image {
		source: "qrc:/images/common/logo.png"
		anchors.verticalCenter: parent.verticalCenter
		anchors.left: parent.left
		anchors.leftMargin: 10		
	}
	
	Row {
		anchors.verticalCenter: parent.verticalCenter
		anchors.right: parent.right
		anchors.rightMargin: 10		
		spacing: 10
		Image {
			source: "qrc:/images/common/setting.png"
		}
		
		Image {
			source: "qrc:/images/common/message.png"
		}
	}
}