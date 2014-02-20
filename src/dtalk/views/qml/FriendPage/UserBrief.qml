import QtQuick 2.1
import "../Widgets"
import "../scripts/common.js" as Common

Item {
	id: root
	height: 176
	property string username: commonManager.ownerInfo.displayName
	property url faceSource: commonManager.ownerInfo.avatar
	property url statusSource: "qrc:/images/status/online.png"
	property string statusMessage: "这个家伙很懒，什么都没留下!什么都没留下!什么都没留下!什么都没留下!"
	property int displayMode: 0
	property real messageWidth: displayMode == 0 ? root.width * 0.8 : root.width * 0.6
	
	function toggleMode() {
		displayMode = displayMode == 0 ? 1 : 0
		root.state = root.state == "columnMode" ? "rowMode" : "columnMode"
	}
	
	state: "columnMode"
	
	MouseArea {
		anchors.fill: parent
		onClicked: toggleMode()
	}
	
    states: [
        State {
            name: "rowMode"
            ParentChange { target: face; x: 0; y: 0; parent: faceContainer }
			PropertyChanges { target: face; width: 76; height: 76 }
			PropertyChanges { target: root; height: 106 }
			PropertyChanges { target: rowContentContainer; opacity: 1.0; visible: true }
			PropertyChanges { target: columnContentContainer; opacity: 0.0; visible: false }
        },
		
        State {
            name: "columnMode"
			PropertyChanges { target: root; height: 176 }			
			PropertyChanges { target: columnContentContainer; opacity: 1.0; visible: true }
			PropertyChanges { target: rowContentContainer; opacity: 0.0; visible: false }
        }
    ]
	
    transitions: [
        Transition {
			SequentialAnimation {
				ParentAnimation {
					NumberAnimation { properties: "x,y"; duration: 500; easing.type: Easing.InOutQuad }
					NumberAnimation {properties: "width,height"; duration: 500; easing.type: Easing.InOutQuad }					
				}
				NumberAnimation { properties: "opacity"; duration: 300; }
			}
        }
    ]
	
	Image {
		anchors.fill: parent
		anchors.topMargin: 0 - Common.titlebarHeight
		source: "qrc:/images/common/mask.png"
	}	
	
	Rectangle {
		height: 1
		width: parent.width
		anchors.bottom: parent.bottom
		color: Qt.rgba(0.9, 0.9, 0.9, 0.6)
	}
	
	
	Column {
		id: columnContainer
		visible: displayMode == 0 ? true : false
		anchors.fill: parent
		anchors.topMargin: 10
		spacing: 10
		
		
		Item {
			width: 90; height: 90				
			RoundImageButton {
				id: face
				source: faceSource
				borderWidth: 4
				radius: width/2
				anchors.top: parent.top
				width: 90; height: 90				
			}
			anchors.horizontalCenter: parent.horizontalCenter			
		}
		
		Column {
			id: columnContentContainer
			anchors.horizontalCenter: parent.horizontalCenter			
			spacing: parent.spacing
			
			Row {
				spacing: 5
				anchors.horizontalCenter: parent.horizontalCenter
				
				Image {
					id: statusImage
					source: statusSource
					width: 10; height: 10
					anchors.verticalCenter: parent.verticalCenter
				}
				
				Text {
					id: nameText
					text: username
					color: "#fff"
					anchors.verticalCenter: parent.verticalCenter
				}
			}
			
			Text {
				id: statusText
				anchors.horizontalCenter: parent.horizontalCenter
				text: statusMessage
				color: Qt.rgba(0.9, 0.9, 0.9, 0.7)
				font.pixelSize: 12
				width: messageWidth
				elide: Text.ElideRight
				horizontalAlignment: Qt.AlignHCenter				
			}
		}
	}
	
	Row {
		id: rowContainer
		anchors.fill: parent
		anchors.leftMargin: 20
		anchors.rightMargin: 20
		spacing: 16
		visible: displayMode == 1 ? true : false
		clip: true
		
		Item {
			id: faceContainer
			anchors.verticalCenter: parent.verticalCenter
			anchors.verticalCenterOffset: -8
			width: 76; height: 76
		}
		
		Column {
			id: rowContentContainer
			opacity: 0.0
			anchors.verticalCenter: parent.verticalCenter
			spacing: 5
			Row {
				spacing: 5
				Image {
					id: statusImage2
					source: statusSource
					anchors.verticalCenter: parent.verticalCenter
					width: 10; height: 10
				}
				
				Text {
					id: nameText2
					text: username
					color: "#fff"
					anchors.verticalCenter: parent.verticalCenter
				}
			}
			
			Text {
				id: statusText2
				anchors.horizontalCenter: parent.horizontalCenter
				text: statusMessage
				color: Qt.rgba(0.9, 0.9, 0.9, 0.7)
				font.pixelSize: 12
				width: messageWidth
				elide: Text.ElideRight

			}
		}
	}
}