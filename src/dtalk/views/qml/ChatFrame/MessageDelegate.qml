import QtQuick 2.1

Component {
	id: messageDelegate
	
    Item {
        id: wrapper
		width: wrapper.ListView.view.width
		height: messageBox.height + 20
        
        function adjustPosition() {
            wrapper.ListView.view.positionViewAtIndex(wrapper.ListView.view.count - 1, ListView.Contain)
        }
		
		MessageBox { 
			id: messageBox			
			x: instance.type == "received" ? 10 : parent.width - 320
			width: parent.width
			content: instance.body
			type: instance.type
		}
		
		MouseArea {
			anchors.fill: parent
		}
		
		ListView.onAdd: 
			SequentialAnimation {
                ScriptAction { script: adjustPosition() }
				NumberAnimation { target: messageBox; properties: "scale"; from: 0.0; to: 1.0; easing.type: Easing.OutQuad }
                ScriptAction { script: adjustPosition() }
            }
	}
}

