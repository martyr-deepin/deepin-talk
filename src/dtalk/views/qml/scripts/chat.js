/* This script file handles the chat logic */

var chatSrc = "../ChatFrame/ChatWindow.qml"
var component = Qt.createComponent(chatSrc)

function startNewChat() 
{
	if (component.status == Component.Ready) {
		var dynamicObject = component.createObject()
	}
	
}

