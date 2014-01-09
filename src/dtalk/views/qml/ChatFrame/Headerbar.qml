import QtQuick 2.1
import "../Widgets"
import "../scripts/roster.js" as Roster

Rectangle {
	id: container
	
	Column {
		id: info
	    anchors.horizontalCenter: parent.horizontalCenter		
		spacing: 10
		
	    Nickname {
            nickname: Roster.getDisplayName(messageModel.jidInfo())
			anchors.horizontalCenter: parent.horizontalCenter		
	    }
	    
	    Text {
	    	id: signature
	    	text: "这个家伙很懒， 什么都没留下"
			anchors.horizontalCenter: parent.horizontalCenter		
			color: "#cacbcd"
			font.pixelSize: 11
	    }
		
	}
	
	Row { 
		
		id: control
		
		spacing: 26
		anchors.horizontalCenter: parent.horizontalCenter				
		anchors.top: info.bottom
		anchors.topMargin: 10
		
		DButton { source: "qrc:/images/chat/file.png"; anchors.verticalCenter: parent.verticalCenter }
		DButton { source: "qrc:/images/chat/image.png"; anchors.verticalCenter: parent.verticalCenter } 
		DButton { source: "qrc:/images/chat/block.png"; anchors.verticalCenter: parent.verticalCenter } 
		RoundImageButton { source: messageModel.jidInfo().avatar; anchors.verticalCenter: parent.verticalCenter } 
		DButton { source: "qrc:/images/chat/image.png"; anchors.verticalCenter: parent.verticalCenter } 
		DButton { source: "qrc:/images/chat/timer.png"; anchors.verticalCenter: parent.verticalCenter } 
		DButton { source: "qrc:/images/chat/shot.png"; anchors.verticalCenter: parent.verticalCenter } 
		
	}
}