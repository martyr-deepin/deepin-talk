import QtQuick 2.1
import "Widgets"
import "LoginPage"
import "FriendPage"
import "Notify"

DWindow {
	id: root
    
    Item {
        anchors.fill: parent
        
        Connections {
            /* target: serverManager */
            /* onUserLoginSuccessed: { */
            /*     loginFrame.visible = false */
            /*     loginFrame.isLogging = false */
            /*     talkframeLoader.sourceComponent = talkframeComponent */
            /* } */
            target: commonManager
            onDbInitFinished: { 
                loginFrame.visible = false
                loginFrame.isLogging = false
                talkframeLoader.sourceComponent = talkframeComponent
            }
            
            /* onUserLoginFailed: { */
            /*     loginFrame.isLogging = false */
            /*     loginFrame.showErrorTip(serverManager.loginFailedReason) */
            /* } */
        }
        
        Connections {
            target: serverManager
            onUserLoginFailed: {
                loginFrame.isLogging = false
                loginFrame.showErrorTip(serverManager.loginFailedReason)
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
        
        NotifyBox {}
    }
    

}