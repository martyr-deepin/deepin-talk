import QtQuick 2.1
import "Widgets"
import "LoginPage"
import "FriendPage"
import "Notify"

DWindow {
	id: root
    
    Item {
        anchors.fill: parent
        signal userLoginFailed(string reason)
        signal dbInitFinished
        
        Component.onCompleted: {
            serverManager.userLoginFailed.connect(userLoginFailed)
            commonManager.dbInitFinished.connect(dbInitFinished)
        }
        
        onUserLoginFailed: {
                loginFrame.isLogging = false
                loginFrame.showErrorTip(reason)
        }
        
        onDbInitFinished: {
            loginFrame.visible = false
            loginFrame.isLogging = false
            talkframeLoader.sourceComponent = talkframeComponent
        }
                
        NotifyBox {}
        
        
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