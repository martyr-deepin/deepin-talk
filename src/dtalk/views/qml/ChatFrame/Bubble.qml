import QtQuick 2.1

Item {
	id: container
	
	property string type
	property string message
	property int padding: 20
	
	height: message.paintedHeight + padding
	
	
	BorderImage {
		source: container.type == "received" ? "qrc:/images/chat/message_comming.png" : "qrc:/images/chat/message_reply.png"		
		border { left: 18;  right: 18; top: 27; bottom: 18}		
		horizontalTileMode: BorderImage.Stretch	
		verticalTileMode: BorderImage.Stretch
 		anchors.fill: parent
	}
	
	Text { 
		id: message
		width: parent.width
		anchors.left: container.left
		anchors.top: container.top
		anchors.right: container.right
 		anchors { leftMargin: padding; topMargin: padding / 2; rightMargin: padding / 2; bottomMargin: padding / 2 }
		color: "#afb1b5"
		wrapMode: Text.Wrap
		/* selectByMouse: true */
		textFormat: Text.RichText		
		text: container.message
	}
}