import QtQuick 2.1
import QtGraphicalEffects 1.0
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
        
        Headerbar { width: parent.width }
        
        ScrollWidget {
            width: parent.width
            anchors.top: sepeator.bottom
            anchors.bottom: messageBox.top
            ListView {
                anchors.fill: parent
            }
        }
        
        Rectangle {
            id: messageBox
            width: parent.width; height: 120
            anchors.bottom: parent.bottom
            color: "green"
        }
    }
}