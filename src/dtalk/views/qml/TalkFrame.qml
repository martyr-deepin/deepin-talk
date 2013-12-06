import QtQuick 2.1
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0
import "js/roster.js" as Roster


Item {
    id: root
    
	UserBrief {
		id: userBrief
		width: parent.width
		anchors.horizontalCenter: parent.horizontalCenter
	}
    
        
    Connections {
        target: serverManager
        onUserLoginSuccessed: {
            print("end")
            var friendModel = modelManager.getModel("friend")
            var ownerObj = friendModel.getSelf()
            userBrief.faceSource = ownerObj.avatar
            userBrief.username = Roster.getDisplayName(ownerObj)
        }
    }
	
	Rectangle {
		id: splitRect
		width: parent.width; height: 3
		anchors.top: userBrief.bottom
		gradient: Gradient {
			GradientStop { position: 0.0; color: Qt.rgba(0, 0, 0, 0.5)}
			GradientStop { position: 0.5; color: Qt.rgba(0, 0, 0, 0.3)}
			GradientStop { position: 0.7; color: Qt.rgba(0, 0, 0, 0.2)}
			GradientStop { position: 1.0; color: Qt.rgba(0, 0, 0, 0.1)}
		}		
		z: 100
	}
    
	FriendView { 
        id: friendView
		width: parent.width
		anchors.top: userBrief.bottom
		anchors.bottom: controlPanel.top
        
        Component.onCompleted: {
            var _model = modelManager.getModel("friend")            
            friendView.model = _model
        }
	}
	
	/* TabView {  */
	/* 	width: parent.width */
	/* 	anchors.top: userBrief.bottom */
	/* 	anchors.bottom: controlPanel.top */
    /*     Tab { title: "friend" ; FriendView { id: friendView } } */
    /*     Tab { title: "group" ; Item {}} */
    /*     Tab { title: "recent" ; Item {}} */
    /*     Tab { title: "search" ; Item {}} */
	/* 	frameVisible: false */
	/* 	style: tabViewStyle */
	/* } */
	
	ControlPanel {
		id: controlPanel
		width: parent.width
		anchors.bottom: parent.bottom
	}
	
	function getTabImage(name) {
		return "image/tab/" + name + ".png"
	}
	
    property Component tabViewStyle: TabViewStyle {
        tabOverlap: 0
        tabsMovable: false
        tab: Item {
            property int totalOverlap: tabOverlap * (control.count - 1)
            implicitWidth: styleData.availableWidth / control.count
            implicitHeight: 40
			
			Rectangle {
				anchors.fill: parent
				id: tabBack
				color: styleData.selected ? "transparent" : Qt.rgba(0.9, 0.9, 0.9, 0.3)

			}
            Image {
				id: tabImage
				source: getTabImage(styleData.title)
                anchors.centerIn: parent
				width: 25; height: 23
				smooth: true
				antialiasing: true
            }
			
			states: State {
				name: "largeImage"; when: styleData.hovered
				PropertyChanges { target: tabImage; width: 29; height: 26 }
			}
			
			transitions: Transition {
				NumberAnimation { properties: "width,height"; duration: 50; easing.type: Easing.Linear }
			}
			
        }
    }
	
		
}