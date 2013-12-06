import QtQuick 2.1

MainPanel {
	id: root
    
    Connections {
        target: serverManager
        onUserLoginSuccessed: {
            loginFrame.visible = false
            loginFrame.isLogging = false
        }
    }
	
	Item {
		anchors.margins: root.sideWidth + 1
		anchors.fill: parent
		
		Titlebar {
			id: titlebar
			width: parent.width; height: 30
			anchors.top: parent.top
			DragArea {
				anchors.fill: parent
				window: windowView
			}
	
			
		}
		
		Item {
			anchors.top: titlebar.bottom
			width: parent.width
			height: parent.height - titlebar.height
			
			LoginFrame {
                id: loginFrame
				anchors.fill: parent
			}
            
			TalkFrame {
                id: talkFrame
                visible: !loginFrame.visible
				anchors.fill: parent
			}
		}

	}
}