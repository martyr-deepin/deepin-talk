import QtQuick 2.1
import "Widgets"
import "LoginPage"
import "FriendPage"

DWindow {
	id: root
    
    Item {
        anchors.fill: parent
        
        Connections {
            target: serverManager
            onUserLoginSuccessed: {
                loginFrame.visible = false
                loginFrame.isLogging = false
                talkframeLoader.sourceComponent = talkframeComponent
            }
        }
        
        Component {
            id: talkframeComponent
            TalkFrame { }
        }
	    
        
	    LoginFrame {
            id: loginFrame
		    anchors.fill: parent
	    }
        
        Loader {
            id: talkframeLoader
		    anchors.fill: parent
        }
        
    }
}