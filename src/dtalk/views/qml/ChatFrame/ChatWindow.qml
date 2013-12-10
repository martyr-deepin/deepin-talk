import QtQuick 2.1
import QtGraphicalEffects 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0
import "../Widgets"
import "../scripts/common.js" as Common

DWindow {
    id: root
	width: 600; height: 620
    
    Item {
       anchors.fill: parent
       
		LinearGradient {
            id: linearBack
            y: -Common.titlebarHeight
			width: parent.width; height: 136
			start: Qt.point(0, 0)
			end: Qt.point(parent.width, 0)
			gradient: Gradient {
				GradientStop { position: 0.0; color: Qt.rgba(0.9, 0.9, 0.9, 0.6)}
				GradientStop { position: 0.3; color: Qt.rgba(0.9, 0.9, 0.9, 0.5)}
				GradientStop { position: 0.6; color: Qt.rgba(0.9, 0.9, 0.9, 0.2)}
				GradientStop { position: 1.0; color: Qt.rgba(0.9, 0.9, 0.9, 0.0)}
			}		
		}
		Rectangle {
			id: sepeator
			width: parent.width; height: 1
			color: Qt.rgba(0.9, 0.9, 0.9, 0.9)
            anchors.top: linearBack.bottom
		}
        
        Headerbar { width: parent.width; z: 100 }
        
        ScrollWidget {
            width: parent.width
            anchors.top: sepeator.bottom
            anchors.bottom: messageBox.top
            ListView {
                id: messageView
                anchors.fill: parent
			    delegate: MessageDelegate {}
			    model: messageModel
			    interactive: false
			    clip: true
            }
        }
        
        DTextArea {
            id: messageBox
            width: parent.width; height: 120
            anchors.bottom: parent.bottom
            /* textFormat: TextEdit.RichText */
			property int tempType: 0
            focus: true
            
            
            Keys.onPressed: {
                if ((event.key == Qt.Key_Return) && (event.modifiers & Qt.ControlModifier)) {
                    if (messageBox.text != "") {
                        messageModel.postMessage(messageBox.text)
                        messageBox.text = ""
                        event.accepted = true
                    }
                }
            }            
            
            Rectangle { 
                anchors.top: parent.top; 
                width: parent.width; height: 1
                color: Qt.rgba(0.3, 0.3, 0.3, 0.6)
            }
            
            Rectangle {
                anchors.fill: parent
                color: Qt.rgba(0.9, 0.9, 0.9, 0.5)
                radius: 5
                z: -100
            }
        }        
        
    }
}