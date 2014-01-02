import QtQuick 2.1

Component {
	id: messageDelegate
	
    Item {
        id: wrapper
		width: wrapper.ListView.view.width
		height: messageBox.height + 20
        
        function adjustPosition() {
            wrapper.ListView.view.positionViewAtIndex(wrapper.ListView.view.count - 1, ListView.Contains)
        }
		
		MessageBox { 
			id: messageBox			
			x: instance.type == "received" ? 10 : parent.width - messageBox.messageWidth - 10
            messageObj: instance
            width: parent.width
            
		}
        
		ListView.onAdd: SequentialAnimation {
            NumberAnimation { target: wrapper; properties: "scale"; from: 0.0; to: 1.0; easing.type: Easing.OutQuad }
            ScriptAction { script: adjustPosition() }            
        }
        
	}
}

