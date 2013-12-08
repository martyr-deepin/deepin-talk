import QtQuick 2.1
import "../Widgets"

Rectangle {
	id: container
	
	Column {
		id: info
	    anchors.horizontalCenter: parent.horizontalCenter		
		spacing: 10
		
	    Nickname {
	    	id: nickname
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
		
		DButton { source: "images/file.png"; anchors.verticalCenter: parent.verticalCenter }
		DButton { source: "images/image.png"; anchors.verticalCenter: parent.verticalCenter } 
		DButton { source: "images/block.png"; anchors.verticalCenter: parent.verticalCenter } 
		RoundImageButton { source: "../images/face.jpg"; anchors.verticalCenter: parent.verticalCenter } 
		DButton { source: "images/image.png"; anchors.verticalCenter: parent.verticalCenter } 
		DButton { source: "images/timer.png"; anchors.verticalCenter: parent.verticalCenter } 
		DButton { source: "images/shot.png"; anchors.verticalCenter: parent.verticalCenter } 
		
	}
}