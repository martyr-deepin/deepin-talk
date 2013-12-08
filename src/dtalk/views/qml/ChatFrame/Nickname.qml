import QtQuick 2.1

Item {
	id: container
	
	property alias nickname: nicknameText.text
	width: onlineStatus.width + nicknameText.paintedWidth + 10; height: nicknameText.paintedHeight
	
	Image { 
		id: onlineStatus
		source: "images/status.png"
		anchors.left: container.left
		anchors.verticalCenter: container.verticalCenter
	}
	
	Text { 
		id: nicknameText
		color: "#dedde2"
		anchors.right: container.right
		anchors.verticalCenter: container.verticalCenter
		text: "小邪兽"
	}
}