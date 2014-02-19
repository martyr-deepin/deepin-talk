import QtQuick 2.1
import "../Widgets" as Widgets

Component {
	id: messageDelegate
	
    Item {
        id: wrapper
		width: wrapper.ListView.view.width
		height: messageBox.height + 20
        
        function adjustPosition() {
            wrapper.ListView.view.positionViewAtIndex(wrapper.ListView.view.count - 1, ListView.Contains)
        }
		
        Item {
	        id: messageBox
			x: model.type == "received" ? 10 : parent.width - messageBox.messageWidth - 10
            /* instance: instance ? undefined : instance */
            width: parent.width
	        height: Math.max(messageBubble.height, personInfo.height)
            property real messageWidth: messageBubble.width + personInfo.width
	
	        Bubble {
		        id: messageBubble
		        message: model.body
		        anchors.left: model.type == "received" ? personInfo.right : messageBox.left
                maxWidth: parent.width * 0.66
		        y: 10
                type: model.type
	        }
		
	        Item {
		        id: personInfo
		        y: 10
		        width: 60; height: 50 + 15
		        anchors.left: model.type == "received" ? messageBox.left : messageBubble.right
		        anchors.leftMargin: model.type == "received" ? 0 : 10
		        Column {
                    spacing: 5
            
			        Widgets.RoundImageButton { 
				        source: model.type == "received" ? messageModel.jidInfo.avatar : commonManager.ownerInfo.avatar;
                        smooth: true; 
				        anchors.horizontalCenter: parent.horizontalCenter
				        width: 50; height: 50
				    }
            
                    Widgets.GlowText {
                        text: model.published
                        font.pixelSize: 10
				        anchors.horizontalCenter: parent.horizontalCenter
                
                    }
		        }
			
	        }
        }
            
        
		ListView.onAdd: SequentialAnimation {
            NumberAnimation { target: wrapper; properties: "scale"; from: 0.0; to: 1.0; easing.type: Easing.OutQuad }
            ScriptAction { script: adjustPosition() }            
        }
        
	}
}

